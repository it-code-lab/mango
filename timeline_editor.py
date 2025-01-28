class Timeline:
    def __init__(self):
        self.events = []

    def add_event(self, timestamp, event):
        self.events.append({"timestamp": timestamp, "event": event})

    def display(self):
        for event in sorted(self.events, key=lambda x: x['timestamp']):
            print(f"{event['timestamp']}: {event['event']}")
