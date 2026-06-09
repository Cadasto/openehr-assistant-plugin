#!/usr/bin/env bash
# SessionStart hook: detect openEHR resources in the workspace and display context

set -euo pipefail

found=()

# Check for openEHR project config
if [ -f ".openehr-project.json" ]; then
  found+=("project config: .openehr-project.json")
fi

# Count ADL files (archetypes)
adl_count=$(find . -name "*.adl" -not -path "./.git/*" 2>/dev/null | wc -l)
if [ "$adl_count" -gt 0 ]; then
  found+=("archetypes: ${adl_count} .adl files")
fi

# Count OET files (templates)
oet_count=$(find . -name "*.oet" -not -path "./.git/*" 2>/dev/null | wc -l)
if [ "$oet_count" -gt 0 ]; then
  found+=("templates: ${oet_count} .oet files")
fi

# Count OPT files (operational templates)
opt_count=$(find . -name "*.opt" -not -path "./.git/*" 2>/dev/null | wc -l)
if [ "$opt_count" -gt 0 ]; then
  found+=("operational templates: ${opt_count} .opt files")
fi

# Only print if openEHR resources were found
if [ ${#found[@]} -gt 0 ]; then
  echo "openEHR workspace detected:"
  for item in "${found[@]}"; do
    echo "  - ${item}"
  done
  echo ""
  echo "Commands: /ckm-search, /openehr-explain, /semantic-diff, /archetype-fix-syntax, /archetype-impact, /template-from-form"
  echo "Skills (auto, or describe the task): archetype-authoring (incl. review + rationale + translate), archetype-lint, template-authoring, composition-builder, aql-authoring, demographic-modeling, openehr-assistant (guides)"
fi
