import re

def parse_script(script):
    """Parse a script written in natural language to identify scenes, characters, and actions."""
    commands = []
    lines = script.split('\n')
    for line in lines:
        match = re.match(r"Scene:\s*(.+)", line, re.IGNORECASE)
        if match:
            commands.append({"type": "scene", "name": match.group(1).strip()})
        match = re.match(r"Character:\s*(.+) enters from (.+)", line, re.IGNORECASE)
        if match:
            commands.append({"type": "character", "name": match.group(1).strip(), "action": "enter", "from": match.group(2).strip()})
        match = re.match(r"Action:\s*(.+)", line, re.IGNORECASE)
        if match:
            commands.append({"type": "action", "description": match.group(1).strip()})
    return commands