#!/usr/bin/env python3
"""
Convert SKILL.md files to command .md files

Flow:
  skills/rrr/SKILL.md → commands/rrr.md
  
Structure:
  SKILL.md:
    ---
    name: rrr
    description: Create session retrospective...
    ---
    # Content here...
    
  command.md:
    ---
    description: Create session retrospective...
    ---
    **EXECUTE NOW:**
    # Content here...
"""

import os
import re
from pathlib import Path

def parse_skill(skill_path: Path) -> tuple[str, str]:
    """Extract description and content from SKILL.md"""
    content = skill_path.read_text()
    
    # Split by frontmatter delimiters
    parts = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    
    if len(parts) >= 3:
        frontmatter = parts[1]
        body = '---'.join(parts[2:]).strip()
        
        # Extract description
        desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
        description = desc_match.group(1) if desc_match else "No description"
        
        return description, body
    
    return "No description", content

def create_command(description: str, body: str) -> str:
    """Generate command markdown"""
    return f"""---
description: {description}
---

**EXECUTE NOW:**

{body}
"""

def main():
    script_dir = Path(__file__).parent
    skills_dir = script_dir.parent / "skills"
    commands_dir = script_dir.parent / "commands"
    
    commands_dir.mkdir(exist_ok=True)
    
    count = 0
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                description, body = parse_skill(skill_file)
                command_content = create_command(description, body)
                
                command_file = commands_dir / f"{skill_dir.name}.md"
                command_file.write_text(command_content)
                
                print(f"✓ {skill_dir.name}")
                count += 1
    
    print(f"\nDone! {count} commands created.")

if __name__ == "__main__":
    main()
