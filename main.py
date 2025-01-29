import sys
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

class AnimationTool(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Animation Tool - Professional UI")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize components
        self.scene_generator = SceneGenerator()
        self.motion_automation = MotionAutomation()
        self.audio_integration = AudioIntegration()
        self.timeline_editor = TimelineEditor()

        # Set up the UI Layout
        self.setup_ui()

    def setup_ui(self):
        """Setup the main UI layout similar to Animaker."""
        
        # ====== Toolbar (Top) ======
        toolbar = self.menuBar()
        file_menu = toolbar.addMenu("File")

        new_action = QAction(QIcon(), "New Project", self)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)

        open_action = QAction(QIcon(), "Open Project", self)
        open_action.triggered.connect(self.load_project)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon(), "Save Project", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        export_action = QAction(QIcon(), "Export Video", self)
        export_action.triggered.connect(self.export_video)
        file_menu.addAction(export_action)

        # ====== Main Layout ======
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # ====== Left Panel (Assets) ======
        self.asset_list = QListWidget()
        self.asset_list.addItems(["Backgrounds", "Characters", "Props", "Audio"])
        self.asset_list.itemClicked.connect(self.asset_selected)

        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Assets Library"))
        left_panel.addWidget(self.asset_list)

        left_frame = QFrame()
        left_frame.setLayout(left_panel)
        left_frame.setFrameShape(QFrame.Shape.StyledPanel)

        # ====== Center Panel (Live Preview) ======
        self.preview_label = QLabel("Live Preview")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("border: 2px solid black;")

        preview_scene = QGraphicsScene()
        self.preview_view = QGraphicsView(preview_scene)

        center_layout = QVBoxLayout()
        center_layout.addWidget(QLabel("Animation Preview"))
        center_layout.addWidget(self.preview_view)

        center_frame = QFrame()
        center_frame.setLayout(center_layout)
        center_frame.setFrameShape(QFrame.Shape.StyledPanel)

        # ====== Bottom Panel (Timeline) ======
        self.timeline_label = QLabel("Timeline Editor")
        self.timeline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timeline_list = QListWidget()
        self.timeline_list.addItems(["Scene Start", "Character Entry", "Motion Applied"])

        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(QLabel("Animation Timeline"))
        bottom_layout.addWidget(self.timeline_list)

        bottom_frame = QFrame()
        bottom_frame.setLayout(bottom_layout)
        bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)

        # ====== Splitter (Allows resizing of panels) ======
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_frame)
        splitter.addWidget(center_frame)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter)

        # ====== Bottom Timeline ======
        main_layout.addWidget(bottom_frame)

        # ====== Buttons Panel ======
        button_panel = QVBoxLayout()

        self.scene_btn = QPushButton("Generate Scene")
        self.scene_btn.clicked.connect(self.generate_scene)
        button_panel.addWidget(self.scene_btn)

        self.motion_btn = QPushButton("Add Motion")
        self.motion_btn.clicked.connect(self.add_motion)
        button_panel.addWidget(self.motion_btn)

        self.audio_btn = QPushButton("Add Audio")
        self.audio_btn.clicked.connect(self.add_audio)
        button_panel.addWidget(self.audio_btn)

        self.preview_btn = QPushButton("Preview Animation")
        self.preview_btn.clicked.connect(self.preview_animation)
        button_panel.addWidget(self.preview_btn)

        self.export_btn = QPushButton("Export Video")
        self.export_btn.clicked.connect(self.export_video)
        button_panel.addWidget(self.export_btn)

        main_layout.addLayout(button_panel)

        # ====== Bottom Panel (Timeline) ======
        self.timeline_scene = QGraphicsScene()
        self.timeline_view = QGraphicsView(self.timeline_scene)

        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(QLabel("Animation Timeline"))
        bottom_layout.addWidget(self.timeline_view)

        bottom_frame = QFrame()
        bottom_frame.setLayout(bottom_layout)
        bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)
        
        main_layout.addWidget(bottom_frame)

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

    def generate_scene(self):
        """Generate a scene and display it in the preview window."""
        scene_path = self.scene_generator.generate_scene("NewScene", "cartoon")
        self.show_image(scene_path)

    def add_motion(self):
        """Apply motion to the scene."""
        motion_path = self.motion_automation.apply_motion("Character", "walk", save_as_gif=True)
        self.show_image(motion_path)

    def show_image(self, image_path):
        """Display an image in the UI preview panel, ensuring no ICC profile issues."""
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

        # Display the image
        pixmap = QPixmap(image_path)
        self.preview_label.setPixmap(pixmap)

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

    def export_video(self):
        """Export the animation as an MP4 video."""
        export_file, _ = QFileDialog.getSaveFileName(self, "Export Video", "", "MP4 Video (*.mp4)")

        if export_file:
            command = f"ffmpeg -framerate 30 -i output/scenes/%04d.png -i output/audio/final_audio.mp3 -c:v libx264 -pix_fmt yuv420p {export_file}"
            os.system(command)
            print(f"Video exported: {export_file}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimationTool()
    window.show()
    sys.exit(app.exec())
