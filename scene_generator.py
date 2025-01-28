from PIL import Image, ImageDraw

def generate_scene(scene_name):
    """Generate a basic scene background based on the scene name."""
    img = Image.new('RGB', (1920, 1080), color=(135, 206, 235))  # Default sky blue
    draw = ImageDraw.Draw(img)
    draw.text((50, 50), f"Scene: {scene_name}", fill=(0, 0, 0))
    img.save(f"{scene_name.lower().replace(' ', '_')}.png")
    return f"{scene_name.lower().replace(' ', '_')}.png"