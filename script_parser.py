import re
import json

class ScriptParser:
    def __init__(self):
        self.commands = []
        self.errors = []

    def parse_script(self, script, language='en'):
        """Parse a script written in natural language to identify scenes, characters, and actions."""
        self.commands = []
        self.errors = []

        # Add support for multilingual parsing if needed (e.g., translation logic can go here)
        if language != 'en':
            script = self._translate_script(script, language)

        lines = script.split('\n')
        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                # Match Scene
                match = re.match(r"Scene:\s*(.+)(\s*\((.+)\))?", line, re.IGNORECASE)
                if match:
                    scene_name = match.group(1).strip()
                    metadata = match.group(3) or ""
                    self.commands.append({"type": "scene", "name": scene_name, "metadata": self._parse_metadata(metadata)})
                    continue

                # Match Character Entry
                match = re.match(r"Character:\s*(.+) enters from (.+)", line, re.IGNORECASE)
                if match:
                    character_name = match.group(1).strip()
                    entry_point = match.group(2).strip()
                    self.commands.append({"type": "character", "name": character_name, "action": "enter", "from": entry_point})
                    continue

                # Match Action
                match = re.match(r"Action:\s*(.+)(\s*->\s*Repeat (\d+) times)?", line, re.IGNORECASE)
                if match:
                    action_description = match.group(1).strip()
                    repeat_count = int(match.group(3)) if match.group(3) else 1
                    self.commands.append({"type": "action", "description": action_description, "repeat": repeat_count})
                    continue

                # Match Conditional Actions
                match = re.match(r"If:\s*(.+), then Action:\s*(.+)", line, re.IGNORECASE)
                if match:
                    condition = match.group(1).strip()
                    action = match.group(2).strip()
                    self.commands.append({"type": "conditional_action", "condition": condition, "action": action})
                    continue

                # Match Simultaneous Events
                match = re.match(r"Simultaneous:\s*(.+)", line, re.IGNORECASE)
                if match:
                    actions = [a.strip() for a in match.group(1).split(',')]
                    self.commands.append({"type": "simultaneous", "actions": actions})
                    continue

                # If no matches, add to errors
                self.errors.append(f"Unrecognized command on line {line_number}: {line}")

            except Exception as e:
                self.errors.append(f"Error processing line {line_number}: {line}. Error: {str(e)}")

        return self.commands

    def _parse_metadata(self, metadata):
        """Parse inline metadata in parentheses."""
        metadata_dict = {}
        if metadata:
            items = metadata.split(',')
            for item in items:
                try:
                    key, value = map(str.strip, item.split(':'))
                    metadata_dict[key.lower()] = value
                except ValueError:
                    self.errors.append(f"Malformed metadata: {item}")
        return metadata_dict

    def _translate_script(self, script, language):
        """Translate script to English from another language."""
        # Placeholder for actual translation logic (e.g., use an API like Google Translate)
        return script

    def export_parsed_script(self, format="json"):
        """Export the parsed script in the specified format (JSON or XML)."""
        if format.lower() == "json":
            return json.dumps(self.commands, indent=4)
        elif format.lower() == "xml":
            return self._convert_to_xml(self.commands)
        else:
            raise ValueError("Unsupported format. Use 'json' or 'xml'.")

    def _convert_to_xml(self, commands):
        """Convert commands list to XML format."""
        xml = "<Script>\n"
        for command in commands:
            xml += f"  <{command['type']}>\n"
            for key, value in command.items():
                if key != "type":
                    xml += f"    <{key}>{value}</{key}>\n"
            xml += f"  </{command['type']}>\n"
        xml += "</Script>"
        return xml

    def get_errors(self):
        """Return any errors encountered during parsing."""
        return self.errors

# Example Usage
if __name__ == "__main__":
    parser = ScriptParser()

    # Sample Script
    sample_script = """
    Scene: Battlefield (Duration: 15s, Style: Realistic)
    Character: Soldier enters from right
    Action: Shoot -> Repeat 3 times
    If: Enemy appears, then Action: Take cover
    Simultaneous: Soldier shoots, Enemy fires back
    """

    parsed_commands = parser.parse_script(sample_script)
    print("Parsed Commands:")
    print(json.dumps(parsed_commands, indent=4))

    # Export as JSON
    json_output = parser.export_parsed_script(format="json")
    print("\nExported JSON:")
    print(json_output)

    # Export as XML
    xml_output = parser.export_parsed_script(format="xml")
    print("\nExported XML:")
    print(xml_output)

    # Print Errors (if any)
    errors = parser.get_errors()
    if errors:
        print("\nErrors:")
        print("\n".join(errors))
