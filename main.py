import sys
from PyQt6.QtWidgets import QApplication,QFileDialog, QMainWindow
from ui_setup import setup_ui
from asset_manager import AssetManager
from scene_generator import SceneGenerator
from timeline_manager import TimelineManager
from motion_automation import MotionAutomation
from audio_integration import AudioIntegration
from timeline_editor import TimelineEditor

import os
import cv2
import numpy as np
import ffmpeg
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget,
    QHBoxLayout, QListWidget, QFrame, QSplitter, QGraphicsView, QGraphicsScene
)
from PyQt6.QtGui import QPixmap, QImage, QIcon, QAction
from PyQt6.QtCore import Qt
from scene_generator import SceneGenerator
from motion_automation import MotionAutomation
from audio_integration import AudioIntegration
from timeline_editor import TimelineEditor
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem
from PyQt6.QtGui import QPixmap
from PIL import Image
from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QVBoxLayout, QSplitter
from PyQt6.QtWidgets import QSizePolicy

class AnimationTool(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize components
        self.scene_generator = SceneGenerator()
        self.motion_automation = MotionAutomation()
        self.audio_integration = AudioIntegration()
        self.timeline_editor = TimelineEditor()

        self.asset_manager = AssetManager(self.scene_generator, None)  # Preview scene set in setup_ui
        self.timeline_manager = TimelineManager(None)  # Set later in setup_ui

        # Setup UI
        setup_ui(self)

    def new_project(self):
        """Start a new project."""
        print("New project started!")

    def load_project(self):
        """Load an existing project."""
        project_file, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "JSON Files (*.json)")
        if project_file:
            print(f"Loaded project: {project_file}")

    def save_project(self):
        """Save the current project."""
        project_file, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "JSON Files (*.json)")
        if project_file:
            print(f"Project saved: {project_file}")

    def export_video(self):
        """Export the animation as an MP4 video."""
        export_file, _ = QFileDialog.getSaveFileName(self, "Export Video", "", "MP4 Video (*.mp4)")
        if export_file:
            command = f"ffmpeg -framerate 30 -i output/scenes/%04d.png -i output/audio/final_audio.mp3 -c:v libx264 -pix_fmt yuv420p {export_file}"
            os.system(command)
            print(f"Video exported: {export_file}")

    def populate_asset_categories(self):
        """List asset categories (Backgrounds, Characters, Props, Audio) in the library."""
        self.asset_list.clear()
        asset_folders = ["backgrounds", "characters", "props", "audio"]
        for folder in asset_folders:
            if os.path.exists(os.path.join(self.scene_generator.asset_library_path, folder)):
                self.asset_list.addItem(folder)

    def load_asset_files(self, item):
        """Show actual files inside the selected asset category."""
        category = item.text()
        asset_path = os.path.join(self.scene_generator.asset_library_path, category)
        
        self.asset_list.clear()  # ✅ Clear the list and show actual assets
        self.asset_list.addItem(".. (Back)")  # ✅ Allow going back to categories

        for file in os.listdir(asset_path):
            if file.endswith((".png", ".jpg", ".gif")):  # ✅ Show only images
                self.asset_list.addItem(file)

    def dropEvent(self, event):
        """Drop an animation onto the timeline."""
        selected_event = self.timeline_list.currentItem()
        if not selected_event:
            return

        text = selected_event.text()
        timeline_item = QGraphicsTextItem(text)
        timeline_item.setPos(50, 10)  # Default timeline position
        self.timeline_scene.addItem(timeline_item)

    def dragEnterEvent(self, event):
        """Enable dragging assets into the scene."""
        event.accept()

    def dropEvent(self, event):
        """Drop asset into the scene."""
        selected_item = self.asset_list.currentItem()
        if not selected_item:
            return

        asset_category = selected_item.text()
        assets = self.scene_generator.get_assets_by_category(asset_category)

        if assets:
            asset_path = os.path.join("assets", asset_category, assets[0])
            pixmap = QPixmap(asset_path)
            item = QGraphicsPixmapItem(pixmap)
            item.setPos(100, 100)  # Default position
            self.preview_scene.addItem(item)

            print(f"Added {assets[0]} to scene")

    def asset_selected(self, item):
        """Preview selected asset before adding it to the scene."""
        category = item.text()
        assets = self.scene_generator.get_assets_by_category(category)

        if not assets:
            print(f"No assets available in {category}")
            return

        asset_path = os.path.join("assets", category, assets[0])  # Load first asset as preview
        pixmap = QPixmap(asset_path)
        self.preview_label.setPixmap(pixmap)

    def add_timeline_event(self, event_text, timestamp):
        """Add an event to the timeline visually."""
        event_item = QGraphicsTextItem(f"{timestamp}s: {event_text}")
        event_item.setPos(timestamp * 10, 10)  # Adjust spacing
        self.timeline_scene.addItem(event_item)

    def asset_selected(self, item):
        """Handle asset selection from the list."""
        print(f"Selected Asset: {item.text()}")

    def new_project(self):
        """Start a new project."""
        print("New project started!")

    def generate_scene(self):
        """Generate a scene and display it in the Animation Preview."""
        try:
            scene_path = self.scene_generator.generate_scene("NewScene", "cartoon")
            if os.path.exists(scene_path):
                print(f"Generated Scene: {scene_path}")
                self.show_image(scene_path)  # ✅ Display Scene in Preview
            else:
                print("Error: Scene was not generated.")
        except Exception as e:
            print(f"Error generating scene: {e}")


    def add_motion(self):
        """Move character inside the scene."""
        selected_item = self.preview_scene.items()[0]  # Get first character/item
        if not isinstance(selected_item, QGraphicsPixmapItem):
            print("No character selected for motion")
            return

        # Define motion path
        positions = [(100, 100), (200, 100), (300, 100), (400, 100)]

        def move_character(step=0):
            if step < len(positions):
                selected_item.setPos(*positions[step])
                QTimer.singleShot(500, lambda: move_character(step + 1))  # Move every 500ms

        move_character()

    def show_image(self, image_path):
        """Display an image in the UI preview panel using QGraphicsView."""
        if not os.path.exists(image_path):
            print(f"Error: Image file {image_path} does not exist.")
            return

        # Remove ICC profile to prevent libpng warning
        try:
            img = Image.open(image_path)
            img = img.convert("RGB")  # Convert to RGB to remove profile
            img.save(image_path, "PNG", icc_profile=None)  # Remove ICC profile
        except Exception as e:
            print(f"Warning: Could not remove ICC profile from {image_path} - {e}")

        # Display in QGraphicsView
        pixmap = QPixmap(image_path)
        self.preview_scene.clear()  # Clear previous preview
        item = QGraphicsPixmapItem(pixmap)
        self.preview_scene.addItem(item)

    def add_audio(self):
        """Generate and add audio to the scene."""
        audio_file = self.audio_integration.generate_tts_audio("This is an animated voice!")
        print(f"Generated Audio: {audio_file}")

    def preview_animation_old(self):
        """Real-time preview of animation."""
        video_path = "output/preview.mp4"
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Real-Time Preview", frame)
            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()

    def preview_animation(self):
        """Real-time preview of animation using QMovie (for GIFs)"""
        gif_path = "output/motion/Character_walk.gif"  # Change to your generated GIF file

        if not os.path.exists(gif_path):
            print("No preview available. Generate animation first.")
            return

        self.movie = QMovie(gif_path)
        self.preview_label.setMovie(self.movie)
        self.movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimationTool()
    window.show()
    sys.exit(app.exec())
