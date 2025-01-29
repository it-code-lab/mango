import matplotlib.pyplot as plt
from collections import defaultdict

from motion_automation import MotionAutomation

class TimelineEditor:
    def __init__(self):
        self.timeline = []
        self.undo_stack = []
        self.redo_stack = []
        self.event_groups = defaultdict(list)
        self.keyframes = defaultdict(list)

    def add_keyframe(self, timestamp, event, character):
        """Add a keyframe for animation control."""
        self.keyframes[character].append({"timestamp": timestamp, "event": event})
        self.keyframes[character] = sorted(self.keyframes[character], key=lambda x: x["timestamp"])

    def get_keyframes(self, character):
        """Retrieve keyframes for a character."""
        return self.keyframes.get(character, [])

    def sync_with_motion(self, motion_type, character, duration):
        """Auto-generate keyframes based on motion type."""
        positions = MotionAutomation().apply_motion(character, motion_type, duration, save_as_gif=False)
        for i, pos in enumerate(positions):
            self.add_keyframe(i * (duration / len(positions)), {"position": pos}, character)

    def display_timeline(self):
        """Display all timeline events."""
        for character, keyframes in self.keyframes.items():
            print(f"Timeline for {character}:")
            for kf in keyframes:
                print(f"  {kf['timestamp']}s -> {kf['event']}")
                
    def add_event(self, timestamp, event, group=None):
        """Add an event to the timeline."""
        self.undo_stack.append(("remove", timestamp, event, group))
        self.redo_stack.clear()
        self.timeline.append({"timestamp": timestamp, "event": event})
        self.timeline.sort(key=lambda x: x['timestamp'])  # Keep events in order
        if group:
            self.event_groups[group].append({"timestamp": timestamp, "event": event})
        self.timeline.sort(key=lambda x: x['timestamp'])

    def remove_event(self, timestamp):
        """Remove an event from the timeline by timestamp."""
        for event in self.timeline:
            if event["timestamp"] == timestamp:
                self.undo_stack.append(("add", event["timestamp"], event["event"], None))
                self.redo_stack.clear()
                self.timeline.remove(event)
                break

    def group_events(self, group_name, events):
        """Group related events together for better organization."""
        self.undo_stack.append(("ungroup", group_name, events))
        self.redo_stack.clear()
        for event in events:
            self.event_groups[group_name].append(event)

    def ungroup_events(self, group_name):
        """Remove a group from the timeline."""
        if group_name in self.event_groups:
            events = self.event_groups.pop(group_name)
            self.undo_stack.append(("group", group_name, events))
            self.redo_stack.clear()

    def undo(self):
        """Undo the last action."""
        if not self.undo_stack:
            print("No actions to undo.")
            return

        action = self.undo_stack.pop()
        self.redo_stack.append(action)

        if action[0] == "remove":
            self.timeline.append({"timestamp": action[1], "event": action[2]})
        elif action[0] == "add":
            self.timeline = [e for e in self.timeline if e["timestamp"] != action[1]]
        elif action[0] == "ungroup":
            for event in action[2]:
                self.event_groups[action[1]].remove(event)
        elif action[0] == "group":
            self.event_groups[action[1]] = action[2]

    def redo(self):
        """Redo the last undone action."""
        if not self.redo_stack:
            print("No actions to redo.")
            return

        action = self.redo_stack.pop()
        self.undo_stack.append(action)

        if action[0] == "remove":
            self.timeline = [e for e in self.timeline if e["timestamp"] != action[1]]
        elif action[0] == "add":
            self.timeline.append({"timestamp": action[1], "event": action[2]})
        elif action[0] == "ungroup":
            self.event_groups[action[1]] = action[2]
        elif action[0] == "group":
            for event in action[2]:
                self.event_groups[action[1]].append(event)

    def display_timeline(self, zoom_start=None, zoom_end=None):
        """Display the timeline with optional zoom levels."""
        timestamps = [event["timestamp"] for event in self.timeline]
        events = [event["event"] for event in self.timeline]

        if zoom_start is not None and zoom_end is not None:
            filtered_indices = [i for i, t in enumerate(timestamps) if zoom_start <= t <= zoom_end]
            timestamps = [timestamps[i] for i in filtered_indices]
            events = [events[i] for i in filtered_indices]

        plt.figure(figsize=(10, 2))
        plt.scatter(timestamps, [1] * len(timestamps), c='b')
        for i, event in enumerate(events):
            plt.text(timestamps[i], 1.1, event, ha='center')
        plt.title("Timeline")
        plt.xlabel("Timestamp")
        plt.yticks([])
        plt.show()

    def sync_with_audio(self, audio_length, audio_events):
        """Synchronize timeline events with an audio track."""
        print(f"Audio Length: {audio_length} seconds")
        print("Audio Events:")
        for event in audio_events:
            print(f"  {event}")

# Example Usage
if __name__ == "__main__":
    timeline = TimelineEditor()

    # Add events
    timeline.add_event(1, "Scene starts")
    timeline.add_event(5, "Character enters")
    timeline.add_event(10, "Dialogue starts")

    # Group events
    timeline.group_events("Intro", [
        {"timestamp": 1, "event": "Scene starts"},
        {"timestamp": 5, "event": "Character enters"}
    ])

    # Display timeline
    timeline.display_timeline()

    # Undo and Redo
    timeline.undo()
    timeline.redo()

    # Zoomed timeline display
    timeline.display_timeline(zoom_start=0, zoom_end=6)

    # Sync with audio
    timeline.sync_with_audio(30, [
        {"time": 0, "description": "Background music starts"},
        {"time": 5, "description": "Character dialogue"},
        {"time": 15, "description": "Scene transition"}
    ])
