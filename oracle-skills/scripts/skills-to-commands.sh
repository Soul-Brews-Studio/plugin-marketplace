#!/bin/bash
# Convert skills/ to commands/ with executable instructions

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/../skills"
COMMANDS_DIR="$SCRIPT_DIR/../commands"

mkdir -p "$COMMANDS_DIR"

for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    skill_file="$skill_dir/SKILL.md"
    command_file="$COMMANDS_DIR/$skill_name.md"
    
    if [[ -f "$skill_file" ]]; then
        # Extract description from frontmatter
        desc=$(grep "^description:" "$skill_file" | head -1 | sed 's/description: //')
        
        # Extract content after frontmatter (everything after second ---)
        content=$(awk 'BEGIN{p=0} /^---$/{p++;next} p>=2{print}' "$skill_file")
        
        # Create command file
        cat > "$command_file" << EOF
---
description: $desc
---

**EXECUTE NOW:**

$content
EOF
        echo "Created: $skill_name.md"
    fi
done

echo "Done! $(ls "$COMMANDS_DIR" | wc -l | tr -d ' ') commands created."
