import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QListWidget, QGraphicsPixmapItem

class AssetManager:
    def __init__(self, scene_generator, preview_scene):
        self.scene_generator = scene_generator
        self.preview_scene = preview_scene

    def populate_asset_categories(self, asset_list):
        """List asset categories in the library."""
        asset_list.clear()
        asset_folders = ["backgrounds", "characters", "props", "audio"]
        for folder in asset_folders:
            if os.path.exists(os.path.join(self.scene_generator.asset_library_path, folder)):
                asset_list.addItem(folder)

    def load_asset_files(self, asset_list, item):
        """Show actual files inside the selected asset category."""
        category = item.text()
        asset_path = os.path.join(self.scene_generator.asset_library_path, category)

        asset_list.clear()
        asset_list.addItem(".. (Back)")

        for file in os.listdir(asset_path):
            if file.endswith((".png", ".jpg", ".gif")):
                asset_list.addItem(file)

    def drop_asset_to_scene(self, asset_list):
        """Drop an asset into the animation preview scene."""
        selected_item = asset_list.currentItem()
        if not selected_item:
            return

        asset_name = selected_item.text()
        category = asset_list.item(0).text()

        if asset_name == ".. (Back)":
            self.populate_asset_categories(asset_list)
            return

        asset_path = os.path.join(self.scene_generator.asset_library_path, category, asset_name)

        if os.path.exists(asset_path):
            pixmap = QPixmap(asset_path)
            item = QGraphicsPixmapItem(pixmap)
            item.setPos(100, 100)
            self.preview_scene.addItem(item)
