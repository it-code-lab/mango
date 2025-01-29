import os
import numpy as np
import matplotlib.pyplot as plt
import time
from PIL import Image, ImageDraw  


class MotionAutomation:
    def __init__(self):
        self.preset_animations = {
            "walk": self._walk_animation,
            "jump": self._jump_animation,
            "bounce": self._bounce_animation,
            "zigzag": self._zigzag_motion
        }

    def apply_motion_old(self, character, motion_type, duration=2, preview=False, save_as_gif=True):
        """Apply motion to a character with optional real-time preview."""
        if motion_type in self.preset_animations:
            motion_function = self.preset_animations[motion_type]
            positions = motion_function(duration)
            
            if preview:
                self._preview_motion(positions, motion_type)

                return positions
            if save_as_gif:
                output_file = f"output/motion/{character}_{motion_type}.gif"
                os.makedirs("output/motion", exist_ok=True)
                self._save_motion_as_gif(positions, output_file)
                return output_file
        else:
            raise ValueError("Unsupported motion type")

    def apply_motion(self, character, motion_type, duration=2, save_as_gif=True):
        """Apply motion to a character and optionally save it as a GIF."""
        positions = self.preset_animations[motion_type](duration)

        if save_as_gif:
            output_file = f"output/motion/{character}_{motion_type}.gif"
            os.makedirs("output/motion", exist_ok=True)
            self._save_motion_as_gif(positions, output_file)
            return output_file

        return positions

    def _save_motion_as_gif(self, positions, output_file="output/motion_animation.gif", image_size=(400, 400)):
        """Save the character motion as an animated GIF."""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        frames = []

        for pos in positions:
            img = Image.new("RGB", image_size, "white")
            draw = ImageDraw.Draw(img)
            x, y = int(pos[0] * 20), int(image_size[1] - pos[1] * 20)  # Scale positions
            draw.ellipse((x-10, y-10, x+10, y+10), fill="blue")  # Character representation
            frames.append(img)

        # Save as GIF
        frames[0].save(output_file, save_all=True, append_images=frames[1:], duration=50, loop=0)
        return output_file

    def _walk_animation(self, duration):
        """Simulate a walking motion (linear movement)."""
        t = np.linspace(0, duration, num=30)
        x = np.linspace(0, 10, num=30)
        y = np.sin(4 * np.pi * t) * 0.5
        return list(zip(x, y))

    def _jump_animation(self, duration):
        """Simulate a jumping motion with gravity effect."""
        t = np.linspace(0, duration, num=30)
        y = -4 * (t - duration / 2) ** 2 + duration
        x = np.linspace(0, 5, num=30)
        return list(zip(x, y))

    def _bounce_animation(self, duration):
        """Simulate a bouncing motion."""
        t = np.linspace(0, duration, num=30)
        y = np.abs(np.sin(3 * np.pi * t) * 3)
        x = np.linspace(0, 5, num=30)
        return list(zip(x, y))
    
    def _zigzag_motion(self, duration):
        """Simulate a zigzag motion pattern."""
        t = np.linspace(0, duration, num=30)
        x = np.linspace(0, 10, num=30)
        y = np.sin(3 * np.pi * x / 10) * 2
        return list(zip(x, y))

    def _preview_motion(self, positions, motion_type):
        """Render a real-time preview of the motion."""
        plt.figure(figsize=(6, 4))
        plt.title(f"Motion Preview: {motion_type}")
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        
        for pos in positions:
            plt.scatter(pos[0], pos[1], c='b')
            plt.pause(0.05)
        
        plt.show()

# Example Usage
if __name__ == "__main__":
    motion = MotionAutomation()
    
    print("Applying Walking Motion")
    motion_positions = motion.apply_motion("Character1", "walk", preview=True)
    print("Motion Path:", motion_positions)
    
    print("Applying Jumping Motion")
    motion_positions = motion.apply_motion("Character1", "jump", preview=True)
    print("Motion Path:", motion_positions)
    
    print("Applying Bouncing Motion")
    motion_positions = motion.apply_motion("Character1", "bounce", preview=True)
    print("Motion Path:", motion_positions)
    
    print("Applying Zigzag Motion")
    motion_positions = motion.apply_motion("Character1", "zigzag", preview=True)
    print("Motion Path:", motion_positions)
