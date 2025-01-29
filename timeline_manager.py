from PyQt6.QtWidgets import QGraphicsTextItem

class TimelineManager:
    def __init__(self, timeline_scene):
        self.timeline_scene = timeline_scene

    def drop_event(self, event, timeline_list):
        """Drop an animation onto the timeline."""
        selected_event = timeline_list.currentItem()
        if not selected_event:
            return

        text = selected_event.text()
        timeline_item = QGraphicsTextItem(text)
        timeline_item.setPos(50, 10)  # Default timeline position
        self.timeline_scene.addItem(timeline_item)
