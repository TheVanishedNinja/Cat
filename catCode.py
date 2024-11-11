import tkinter as tk
from PIL import Image, ImageTk
import random

class AnimatedPet:
    def __init__(self):
        # Initialize main tkinter window
        self.window = tk.Tk()
        self.window.overrideredirect(True)  # Frameless window
        self.window.wm_attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.config(bg='black')

        # Position in bottom-right corner on taskbar
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Adjust the position
        self.x_position = screen_width - 110
        self.y_position = screen_height - 105  

        # Set geometry with adjusted position
        self.window.geometry(f'100x100+{self.x_position}+{self.y_position}')  

        # Load all animations as lists of frames
        self.animations = {
            "walking_right": self.load_gif_frames('CatGifs/WalkRight.gif'),
            "walking_left": self.load_gif_frames('CatGifs/WalkLeft.gif'),
            "idle": self.load_gif_frames('CatGifs/Idle.gif'),
            "biscuits": self.load_gif_frames('CatGifs/Biscuits.gif'),
            "ear_twitch": self.load_gif_frames('CatGifs/EarTwitch.gif'),
            "blink": self.load_gif_frames('CatGifs/Blink.gif'),
            "head_tilt": self.load_gif_frames('CatGifs/HeadTilt.gif'),
            "sleeping": self.load_gif_frames('CatGifs/Snooze.gif'),
            "tail_twitch": self.load_gif_frames('CatGifs/TailTwitch.gif'),
        }

        # Load static images
        self.pick_up_image = ImageTk.PhotoImage(Image.open('CatGifs/PickUp.png').convert("RGBA"))
        self.still_image = ImageTk.PhotoImage(Image.open('CatGifs/Still.png').convert("RGBA"))

        # Initial animation setup
        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_delay = 100  # Milliseconds between frames

        # Repeat control for specific animations
        self.repeat_count = 0
        self.max_repeats = 2  # Repeat count for walking and sleeping animations

        # Placeholder for displaying the image
        self.label = tk.Label(self.window, bg='black')
        self.label.pack()

        # Drag-and-drop variables
        self.is_dragging = False
        self.current_position = (self.x_position, self.y_position)

        # Bind mouse events for dragging
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<ButtonRelease-1>", self.end_drag)

        # Start the update loop
        self.update_animation()
        self.window.mainloop()

    def load_gif_frames(self, gif_path):
        """Loads all frames of a GIF and returns them as a list of PhotoImages."""
        frames = []
        with Image.open(gif_path) as img:
            for frame in range(img.n_frames):
                img.seek(frame)
                frame_image = ImageTk.PhotoImage(img.copy().convert("RGBA"))
                frames.append(frame_image)
        return frames

    def update_animation(self):
        # If dragging, suspend all animations
        if self.is_dragging:
            return

        # Get the frames for the current animation
        frames = self.animations[self.current_animation]
        self.label.configure(image=frames[self.frame_index])
        
        # Advance to the next frame and wrap around
        self.frame_index = (self.frame_index + 1) % len(frames)
        
        # Check if we reached the end of the current animation
        if self.frame_index == 0:
            if self.current_animation in ["walking_right", "walking_left", "sleeping"]:
                self.repeat_count += 1
                if self.repeat_count >= self.max_repeats:
                    # Reset repeat count and switch to a new animation
                    self.repeat_count = 0
                    self.current_animation = random.choice(list(self.animations.keys()))
            else:
                # For other animations, switch immediately to a new animation
                self.current_animation = random.choice(list(self.animations.keys()))

        # Movement logic for walking animations
        screen_width = self.window.winfo_screenwidth()
        if self.current_animation == "walking_right":
            self.x_position += 4
            if self.x_position > screen_width - 100:  # Ensure it stays within bounds
                self.x_position = screen_width - 100
        elif self.current_animation == "walking_left":
            self.x_position -= 4
            if self.x_position < 0:  # Ensure it stays within bounds
                self.x_position = 0
        
        # Update window position
        self.window.geometry(f'100x100+{self.x_position}+{self.y_position}')

        # Schedule next frame update
        self.window.after(self.animation_delay, self.update_animation)

    def start_drag(self, event):
        """Start dragging the pet and stop animations."""
        self.is_dragging = True
        self.label.configure(image=self.pick_up_image)  # Show PickUp image
        # Center on cursor immediately and prevent initial jump
        self.x_position = event.x_root - 60
        self.y_position = event.y_root - 15
        self.window.geometry(f'100x100+{self.x_position}+{self.y_position}')

    def on_drag(self, event):
        """Drag the pet along with the cursor."""
        if self.is_dragging:
            self.window.geometry(f'100x100+{event.x_root-60}+{event.y_root-15}')  # Center on cursor

    def end_drag(self, event):
        """End the drag action and start the floating effect."""
        self.is_dragging = False
        self.label.configure(image=self.still_image)  # Show Still image upon drop
        # Set new position to the current drop location
        self.x_position = event.x_root - 50
        self.y_position = event.y_root - 15
        self.window.geometry(f'100x100+{self.x_position}+{self.y_position}')
        self.window.after(500, self.float_down)  # Delay before floating down

    def float_down(self):
        """Animate floating down to the current position."""
        target_y = self.window.winfo_screenheight() - 105  # Original bottom position
        step_y = (target_y - self.y_position) // 10  # Divides the descent into steps

        def move_down():
            nonlocal step_y
            if abs(self.y_position - target_y) > abs(step_y):
                self.y_position += step_y
                self.window.geometry(f'100x100+{self.x_position}+{self.y_position}')
                self.window.after(50, move_down)
            else:
                # Snap to target position and reset animation
                self.y_position = target_y
                self.window.geometry(f'100x100+{self.x_position}+{self.y_position}')
                self.current_animation = "idle"  # Reset to idle
                self.update_animation()  # Resume animations

        move_down()  # Start moving down

# Run the AnimatedPet
AnimatedPet()