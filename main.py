import sys
import os
import cv2
import numpy as np
import ffmpeg
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage
from scene_generator import SceneGenerator
from motion_automation import MotionAutomation
from audio_integration import AudioIntegration
from timeline_editor import TimelineEditor
from PIL import Image


class AnimationTool(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Animation Tool - Advanced UI")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize components
        self.scene_generator = SceneGenerator()
        self.motion_automation = MotionAutomation()
        self.audio_integration = AudioIntegration()
        self.timeline_editor = TimelineEditor()

        # Layout setup
        layout = QVBoxLayout()

        # Add buttons
        self.scene_btn = QPushButton("Generate Scene")
        self.scene_btn.clicked.connect(self.generate_scene)
        layout.addWidget(self.scene_btn)

        self.motion_btn = QPushButton("Add Motion")
        self.motion_btn.clicked.connect(self.add_motion)
        layout.addWidget(self.motion_btn)

        self.audio_btn = QPushButton("Add Audio")
        self.audio_btn.clicked.connect(self.add_audio)
        layout.addWidget(self.audio_btn)

        self.preview_btn = QPushButton("Preview Animation")
        self.preview_btn.clicked.connect(self.preview_animation)
        layout.addWidget(self.preview_btn)

        self.export_btn = QPushButton("Export Video")
        self.export_btn.clicked.connect(self.export_video)
        layout.addWidget(self.export_btn)

        # Image preview label
        self.preview_label = QLabel(self)
        layout.addWidget(self.preview_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_scene(self):
        """Generate a scene and display it in the preview window."""
        scene_path = self.scene_generator.generate_scene("TestScene", "cartoon")
        self.show_image(scene_path)

    def add_motion(self):
        """Apply motion to the scene and display the new animation."""
        motion_path = self.motion_automation.apply_motion("Character", "walk", save_as_gif=True)
        self.show_image(motion_path)

    def add_audio(self):
        """Generate and add audio to the scene."""
        audio_file = self.audio_integration.generate_tts_audio("Hello, this is a test narration.")
        print(f"Audio Generated: {audio_file}")

    def preview_animation(self):
        """Real-time preview of animation using OpenCV."""
        video_path = "output/preview.mp4"

        if not os.path.exists(video_path):
            print("No preview available. Generate scenes and motions first.")
            return

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

    def export_video(self):
        """Export the animation as a video."""
        export_file, _ = QFileDialog.getSaveFileName(self, "Export Video", "", "MP4 Video (*.mp4);;AVI Video (*.avi)")
        if export_file:
            command = f"ffmpeg -framerate 30 -i output/scenes/%04d.png -i output/audio/final_audio.mp3 -c:v libx264 -pix_fmt yuv420p {export_file}"
            os.system(command)
            print(f"Exported Video: {export_file}")

    def show_image(self, image_path):
        """Display an image in the UI. If it's a GIF, convert the first frame to display."""
        if image_path.endswith(".gif"):
            try:
                gif = Image.open(image_path)
                gif_frame = gif.convert("RGB")  # Convert first frame to RGB
                gif_frame.save("output/motion_preview.png")  # Save as PNG
                image_path = "output/motion_preview.png"  # Update path to PNG version
            except Exception as e:
                print(f"Error processing GIF: {e}")
                return
        
        # Load image with OpenCV
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image {image_path}")
            return

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.preview_label.setPixmap(QPixmap.fromImage(q_img))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimationTool()
    window.show()
    sys.exit(app.exec())
