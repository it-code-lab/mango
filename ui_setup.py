from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsView,
    QGraphicsScene, QListWidget, QFrame, QSplitter, QSizePolicy, QMenuBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QIcon, QAction

def setup_ui(self):
    """Sets up the main UI components for the animation tool."""

    # ====== Toolbar (Top) ======
    toolbar = self.menuBar()
    file_menu = toolbar.addMenu("File")

    new_action = QAction("New Project", self)
    new_action.triggered.connect(self.new_project)  # ✅ Now exists in main.py
    file_menu.addAction(new_action)

    open_action = QAction("Open Project", self)
    open_action.triggered.connect(self.load_project)  # ✅ Now exists in main.py
    file_menu.addAction(open_action)

    save_action = QAction("Save Project", self)
    save_action.triggered.connect(self.save_project)  # ✅ Now exists in main.py
    file_menu.addAction(save_action)

    export_action = QAction("Export Video", self)
    export_action.triggered.connect(self.export_video)  # ✅ Now exists in main.py
    file_menu.addAction(export_action)

    # ====== Left Panel (Assets Library) ======
    self.asset_list = QListWidget()
    self.asset_list.itemClicked.connect(self.asset_selected)

    left_panel = QVBoxLayout()
    left_panel.addWidget(QLabel("Assets Library"))
    left_panel.addWidget(self.asset_list)

    left_frame = QFrame()
    left_frame.setLayout(left_panel)
    left_frame.setFrameShape(QFrame.Shape.StyledPanel)

    # ====== Center Panel (Animation Preview) ======
    self.preview_scene = QGraphicsScene()
    self.preview_view = QGraphicsView(self.preview_scene)
    self.preview_view.setMinimumSize(600, 400)
    self.preview_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    preview_splitter = QSplitter()
    preview_splitter.addWidget(self.preview_view)

    center_panel = QVBoxLayout()
    center_panel.addWidget(QLabel("Animation Preview"))
    center_panel.addWidget(preview_splitter)

    center_frame = QFrame()
    center_frame.setLayout(center_panel)
    center_frame.setFrameShape(QFrame.Shape.StyledPanel)

    # ====== Right Panel (Animation Timeline) ======
    self.timeline_scene = QGraphicsScene()
    self.timeline_view = QGraphicsView(self.timeline_scene)

    timeline_layout = QVBoxLayout()
    timeline_layout.addWidget(QLabel("Animation Timeline"))
    timeline_layout.addWidget(self.timeline_view)

    timeline_frame = QFrame()
    timeline_frame.setLayout(timeline_layout)
    timeline_frame.setFrameShape(QFrame.Shape.StyledPanel)

    # ====== Control Buttons ======
    self.scene_btn = QPushButton("Generate Scene")
    self.scene_btn.clicked.connect(self.generate_scene)

    self.motion_btn = QPushButton("Add Motion")
    self.motion_btn.clicked.connect(self.add_motion)

    self.audio_btn = QPushButton("Add Audio")
    self.audio_btn.clicked.connect(self.add_audio)

    self.preview_btn = QPushButton("Preview Animation")
    self.preview_btn.clicked.connect(self.preview_animation)

    self.export_btn = QPushButton("Export Video")
    self.export_btn.clicked.connect(self.export_video)

    button_layout = QVBoxLayout()
    button_layout.addWidget(self.scene_btn)
    button_layout.addWidget(self.motion_btn)
    button_layout.addWidget(self.audio_btn)
    button_layout.addWidget(self.preview_btn)
    button_layout.addWidget(self.export_btn)

    button_frame = QFrame()
    button_frame.setLayout(button_layout)

    # ====== Combine All Layouts ======
    main_layout = QHBoxLayout()
    main_layout.addWidget(left_frame)
    main_layout.addWidget(center_frame)
    main_layout.addWidget(timeline_frame)
    main_layout.addWidget(button_frame)

    container = QWidget()
    container.setLayout(main_layout)
    self.setCentralWidget(container)
