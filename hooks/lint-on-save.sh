#!/usr/bin/env bash
# PostToolUse hook: remind user to lint when an ADL archetype file has been saved.
#
# Claude Code pipes the tool-use JSON on stdin. We parse it, check whether the
# tool was Write or Edit on a *.adl file, and if so emit a one-line system-context
# note suggesting a lint run. Non-blocking; output is injected as additional
# context in the conversation.

set -euo pipefail

# Read the hook payload from stdin
payload="$(cat)"

# Extract tool name and target file path using jq if available, otherwise fall
# back to grep/sed. jq is present on most dev boxes; the fallback keeps the hook
# working on minimal systems.
if command -v jq >/dev/null 2>&1; then
  # `|| printf ''` swallows jq parse errors (malformed payloads) so the hook
  # stays non-blocking under `set -euo pipefail`.
  tool_name="$(printf '%s' "$payload" | jq -r '.tool_name // empty' 2>/dev/null || printf '')"
  file_path="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // empty' 2>/dev/null || printf '')"
else
  tool_name="$(printf '%s' "$payload" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
  file_path="$(printf '%s' "$payload" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
fi

# Only react to Write/Edit on .adl files
case "$tool_name" in
  Write|Edit) ;;
  *) exit 0 ;;
esac

case "$file_path" in
  *.adl) ;;
  *) exit 0 ;;
esac

# Emit the reminder to stdout — Claude Code injects this as additional
# conversation context.
printf 'ADL file modified: %s. Consider running `/archetype-lint %s` before committing — structural issues caught now are cheaper than at review time.\n' "$file_path" "$file_path"
