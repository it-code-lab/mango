from PIL import Image, ImageDraw
import os

class SceneGenerator:
    def __init__(self, asset_library_path="assets"):
        self.asset_library_path = asset_library_path
        if not os.path.exists(self.asset_library_path):
            os.makedirs(self.asset_library_path)

    def get_assets_by_category(self, category):
        """Retrieve assets from a specific category in the library."""
        category_path = os.path.join(self.asset_library_path, category)
        if not os.path.exists(category_path):
            return []
        return [f for f in os.listdir(category_path) if f.endswith('.png') or f.endswith('.gif')]

    def list_all_assets(self):
        """List all assets in the library by category."""
        categories = os.listdir(self.asset_library_path)
        all_assets = {}
        for category in categories:
            category_path = os.path.join(self.asset_library_path, category)
            if os.path.isdir(category_path):
                all_assets[category] = self.get_assets_by_category(category)
        return all_assets
    
    def generate_scene(self, scene_name, style="realistic", resolution=(1920, 1080), layers=None):
        """Generate a layered scene and save it."""
        scene_dir = "output/scenes"
        os.makedirs(scene_dir, exist_ok=True)

        # Select default background
        backgrounds = self.get_assets_by_category("backgrounds")
        bg_path = os.path.join(self.asset_library_path, "backgrounds", backgrounds[0]) if backgrounds else None

        if bg_path and os.path.exists(bg_path):
            base_scene = Image.open(bg_path).convert("RGBA")
        else:
            print("Warning: No background found. Using default color.")
            base_scene = Image.new('RGBA', resolution, color=self._get_background_color(style))

        # Add layers (Foreground, Midground, Background)
        if layers:
            for layer in layers:
                layer_path = os.path.join(self.asset_library_path, layer['category'], layer['name'])
                if os.path.exists(layer_path):
                    layer_img = Image.open(layer_path).convert("RGBA")
                    base_scene.paste(layer_img, layer.get("position", (0, 0)), mask=layer_img)

        file_name = os.path.join(scene_dir, f"{scene_name.lower().replace(' ', '_')}_{style}.png")
        base_scene.save(file_name)
        return file_name


    def add_layer(self, base_scene_path, layer_image_path, position=(0, 0)):
        """Add a layer (foreground or mid-ground) to the base scene."""
        base_scene = Image.open(base_scene_path).convert("RGBA")
        layer = Image.open(layer_image_path).convert("RGBA")
        base_scene.paste(layer, position, mask=layer)

        # Save the updated scene
        updated_scene_path = base_scene_path.replace(".png", "_with_layer.png")
        base_scene.save(updated_scene_path)
        return updated_scene_path

    def scale_scene(self, scene_path, resolution):
        """Scale the scene to the specified resolution."""
        scene = Image.open(scene_path)
        scaled_scene = scene.resize(resolution, Image.Resampling.LANCZOS)

        # Save the scaled scene
        scaled_scene_path = scene_path.replace(".png", f"_{resolution[0]}x{resolution[1]}.png")
        scaled_scene.save(scaled_scene_path)
        return scaled_scene_path

    def get_assets(self):
        """List available assets from the asset library."""
        return {category: self.get_assets_by_category(category) for category in os.listdir(self.asset_library_path) if os.path.isdir(os.path.join(self.asset_library_path, category))}

    def add_asset_to_scene(self, base_scene_path, asset_category, asset_name, position=(0, 0)):
        """Add an asset from the library to the base scene."""
        asset_path = os.path.join(self.asset_library_path, asset_category, asset_name)
        if not os.path.exists(asset_path):
            raise FileNotFoundError(f"Asset '{asset_name}' not found in category '{asset_category}'.")

        return self.add_layer(base_scene_path, asset_path, position)

    def _get_background_color(self, style):
        """Determine the background color based on the style."""
        styles = {
            "realistic": (135, 206, 235),  # Sky blue
            "cartoon": (255, 255, 200),   # Light yellow
            "minimalistic": (240, 240, 240)  # Light grey
        }
        return styles.get(style, (255, 255, 255))  # Default to white

    def animate_scene(self, base_scene_path, animation_type, output_path="animated_scene.gif"):
        """Add basic animation to the scene (e.g., moving clouds)."""
        base_scene = Image.open(base_scene_path)
        frames = []

        if animation_type == "moving_clouds":
            for offset in range(0, base_scene.width, 50):
                frame = base_scene.copy()
                draw = ImageDraw.Draw(frame)
                draw.ellipse((offset, 50, offset + 100, 150), fill=(255, 255, 255))  # Simulated cloud
                frames.append(frame)

        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=100, loop=0)
        return output_path

# Example Usage
if __name__ == "__main__":
    generator = SceneGenerator()

    # Generate a scene
    scene_path = generator.generate_scene("Forest", style="cartoon", resolution=(1920, 1080))
    print(f"Generated Scene: {scene_path}")

    # Add a layer
    layer_path = generator.add_layer(scene_path, "assets/props/tree.png", position=(300, 400))
    print(f"Scene with Layer: {layer_path}")

    # Scale the scene
    scaled_path = generator.scale_scene(scene_path, (1280, 720))
    print(f"Scaled Scene: {scaled_path}")

    # List assets
    assets = generator.get_assets()
    print("Available Assets:", assets)

    # Add an asset
    updated_scene = generator.add_asset_to_scene(scene_path, "props", "tree.png", position=(100, 100))
    print(f"Scene with Asset: {updated_scene}")

    # Animate the scene
    animated_scene = generator.animate_scene(scene_path, "moving_clouds")
    print(f"Animated Scene: {animated_scene}")
