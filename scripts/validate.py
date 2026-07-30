#!/usr/bin/env python3
"""Validate this plugin's manifests and skill/agent/command frontmatter.

This is a single-plugin repository (the plugin lives at the repo root), supporting
both Claude Code (``.claude-plugin/plugin.json``) and Cursor (``.cursor-plugin/plugin.json``).
Checks: manifest validity, required fields, cross-manifest agreement, declared component
paths (incl. the bundled ``.mcp.json``), and SKILL.md / agent / command frontmatter.

Usage: python3 scripts/validate.py   (from the repo root)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []

PLUGIN_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
# Component-path fields a manifest may declare (Cursor lists them explicitly).
MANIFEST_PATH_FIELDS = ("logo", "rules", "skills", "agents", "commands", "hooks", "mcpServers")
# Fields that must agree across the Claude and Cursor manifests.
SYNCED_FIELDS = ("name", "version", "description", "author")


def err(msg):
    errors.append(msg)


def load_json(path: Path, label: str):
    try:
        return json.loads(path.read_text())
    except Exception as e:
        err(f"{path.relative_to(ROOT)}: cannot parse JSON ({label}): {e}")
        return None


def validate_skills():
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        return
    for skill_dir in sorted(d for d in skills_dir.iterdir() if d.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        rel = skill_md.relative_to(ROOT)
        if not skill_md.is_file():
            err(f"{rel}: missing SKILL.md")
            continue
        m = re.match(r"\A---\n(.*?)\n---\n", skill_md.read_text(), re.DOTALL)
        if not m:
            err(f"{rel}: missing YAML frontmatter")
            continue
        front = m.group(1)
        for field in ("name", "description"):
            if not re.search(rf"^{field}:", front, re.MULTILINE):
                err(f"{rel}: frontmatter missing '{field}'")
        fm_name = re.search(r"^name:\s*(\S+)", front, re.MULTILINE)
        if fm_name and fm_name.group(1) != skill_dir.name:
            err(f"{rel}: frontmatter name '{fm_name.group(1)}' != directory '{skill_dir.name}'")


def validate_md_components(subdir: str, *, require_name: bool):
    """Validate flat .md components (agents/, commands/): frontmatter present with the
    required fields, and any `name` matches the filename stem. Non-recursive, so any nested
    material is intentionally skipped (shared command references live in top-level references/)."""
    comp_dir = ROOT / subdir
    if not comp_dir.is_dir():
        return
    for md in sorted(comp_dir.glob("*.md")):
        rel = md.relative_to(ROOT)
        m = re.match(r"\A---\n(.*?)\n---\n", md.read_text(), re.DOTALL)
        if not m:
            err(f"{rel}: missing YAML frontmatter")
            continue
        front = m.group(1)
        for field in (("name", "description") if require_name else ("description",)):
            if not re.search(rf"^{field}:", front, re.MULTILINE):
                err(f"{rel}: frontmatter missing '{field}'")
        fm_name = re.search(r"^name:\s*(\S+)", front, re.MULTILINE)
        if fm_name and fm_name.group(1) != md.stem:
            err(f"{rel}: frontmatter name '{fm_name.group(1)}' != filename '{md.stem}'")


def validate_agent_mcp_namespaces(plugin_name: str | None):
    """Agent ``tools:`` entries are matched literally against live tool ids, and the id of an
    MCP tool depends on how the server was mounted: ``mcp__<server>__<tool>`` for a project or
    user ``.mcp.json``, ``mcp__plugin_<plugin>_<server>__<tool>`` for a plugin's own bundled
    ``.mcp.json``. A non-matching entry is dropped silently, and an agent whose whole ``tools:``
    list resolves to nothing is refused ("would be spawned with zero tools"). So every MCP tool
    an agent needs must be listed under both namespaces; this check enforces that pairing.
    (Skills/commands use ``allowed-tools``, which only pre-approves permissions — a miss there
    costs a prompt, not access — so it is deliberately not checked here.)"""
    agents_dir = ROOT / "agents"
    if not agents_dir.is_dir() or not plugin_name:
        return
    mcp_config = ROOT / ".mcp.json"
    if not mcp_config.is_file():
        return
    data = load_json(mcp_config, "MCP config") or {}
    servers = list((data.get("mcpServers") or {}).keys())
    if not servers:
        return

    for md in sorted(agents_dir.glob("*.md")):
        rel = md.relative_to(ROOT)
        m = re.match(r"\A---\n(.*?)\n---\n", md.read_text(), re.DOTALL)
        if not m:
            continue
        entries = set(re.findall(r"^\s*-\s*(mcp__\S+)", m.group(1), re.MULTILINE))
        for server in servers:
            bare_prefix = f"mcp__{server}__"
            scoped_prefix = f"mcp__plugin_{plugin_name}_{server}__"
            bare = {e[len(bare_prefix):] for e in entries if e.startswith(bare_prefix)}
            scoped = {e[len(scoped_prefix):] for e in entries if e.startswith(scoped_prefix)}
            for tool in sorted(bare - scoped):
                err(f"{rel}: tools lists '{bare_prefix}{tool}' without the plugin-mount form "
                    f"'{scoped_prefix}{tool}' (agent loses MCP access under a bundled-plugin mount)")
            for tool in sorted(scoped - bare):
                err(f"{rel}: tools lists '{scoped_prefix}{tool}' without the plain-mount form "
                    f"'{bare_prefix}{tool}' (agent loses MCP access under a project/user .mcp.json)")


def validate_manifest_paths(manifest: dict, label: str):
    for field in MANIFEST_PATH_FIELDS:
        value = manifest.get(field)
        if value is None:
            continue
        paths = [value] if isinstance(value, str) else value if isinstance(value, list) else []
        for path_value in paths:
            if not isinstance(path_value, str) or path_value.startswith(("http://", "https://")):
                continue
            resolved = (ROOT / path_value).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                err(f"{label}: {field} path '{path_value}' escapes the plugin directory")
                continue
            if not resolved.exists():
                err(f"{label}: {field} references missing path '{path_value}'")


def validate_json_file(path: Path, label: str):
    if path.is_file():
        load_json(path, label)
    return path.is_file()


def main():
    manifests = {}
    for subdir, label in ((".claude-plugin", "Claude manifest"), (".cursor-plugin", "Cursor manifest")):
        manifest_path = ROOT / subdir / "plugin.json"
        if not manifest_path.is_file():
            err(f"missing {manifest_path.relative_to(ROOT)}")
            continue
        data = load_json(manifest_path, label)
        if data is None:
            continue
        manifests[subdir] = data

        name = data.get("name")
        if not name or not PLUGIN_NAME_RE.match(name):
            err(f"{label}: 'name' must be lowercase alphanumerics, hyphens, and periods")
        for field in ("name", "version", "description"):
            if not data.get(field):
                err(f"{label}: required field '{field}' is missing or empty")
        validate_manifest_paths(data, label)

    # Cross-manifest agreement (dual-host parity).
    if len(manifests) == 2:
        claude, cursor = manifests[".claude-plugin"], manifests[".cursor-plugin"]
        for field in SYNCED_FIELDS:
            if claude.get(field) != cursor.get(field):
                err(f"manifests disagree on '{field}': "
                    f"claude={claude.get(field)!r} cursor={cursor.get(field)!r}")

    # Bundled MCP config + hook configs must be valid JSON when present.
    validate_json_file(ROOT / ".mcp.json", "MCP config")
    validate_json_file(ROOT / "hooks" / "hooks.json", "Claude hooks")
    validate_json_file(ROOT / "hooks" / "cursor-hooks.json", "Cursor hooks")

    validate_skills()
    validate_md_components("agents", require_name=True)
    validate_md_components("commands", require_name=False)
    validate_agent_mcp_namespaces(manifests.get(".claude-plugin", {}).get("name"))


if __name__ == "__main__":
    main()
    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK: manifests, dual-host parity, MCP config, component paths, skills, agents, "
          "agent MCP namespace pairing, and commands are valid")
