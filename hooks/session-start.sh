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
  echo "Available: /archetype-search, /archetype-explain, /archetype-lint, /archetype-review, /template-search, /template-explain, /aql-designer, /format-data, /guide, /terminology, /type-spec, /adl-idiom, /archetype-fix-syntax, /archetype-translate"
fi
