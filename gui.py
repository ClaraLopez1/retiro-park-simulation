import tkinter as tk
from PIL import Image, ImageTk  # Pillow is needed for JPG images
import threading
from datetime import datetime

class ParkGUI:
    def __init__(self, master, visitor_threads, time_manager):
        self.master = master
        self.time_manager = time_manager
        self.visitor_threads = visitor_threads

        # Load the JPG image using PIL
        pil_image = Image.open("retiro.jpg")  # Replace with your JPG filename
        self.bg_image = ImageTk.PhotoImage(pil_image)

        # Set the canvas size to match the image dimensions
        self.width = self.bg_image.width()
        self.height = self.bg_image.height()

        # Create the canvas using the image dimensions
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        # Draw the background image at the top-left corner
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Create time display frame
        time_frame = tk.Frame(master, bg="white")
        time_frame.place(x=self.width - 200, y=10)

        # Create day display
        self.day_label = tk.Label(
            time_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="blue"
        )
        self.day_label.pack()

        # Create time display
        self.time_label = tk.Label(
            time_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black"
        )
        self.time_label.pack()

        # Create time scale display
        self.scale_label = tk.Label(
            time_frame,
            text=self.time_manager.get_time_scale_description(),
            font=("Arial", 10),
            bg="white",
            fg="gray"
        )
        self.scale_label.pack()

        self.visitor_items = {}  # Dictionary to store each visitor's dot

        # Start the update loops
        self.update_time()
        self.update_visitors()

    def update_time(self):
        """Update the time display every 100ms."""
        try:
            # Get current time and day
            current_time = self.time_manager.get_current_time()
            current_day = self.time_manager.get_current_day()
            
            # Update day display
            self.day_label.config(text=current_day)
            
            # Update time display
            time_str = current_time.strftime("%I:%M %p")
            time_of_day = self.time_manager.get_time_of_day().capitalize()
            self.time_label.config(text=f"{time_str}\n{time_of_day}")
            
        except Exception as e:
            print(f"Error updating time display: {e}")
            
        # Schedule next update
        self.master.after(100, self.update_time)

    def update_visitors(self):
        """Update visitor positions every 100ms."""
        try:
            for visitor in self.visitor_threads:
                vid = visitor.visitor_id
                x, y = visitor.coords
                x, y = int(x), int(y)
                
                if vid not in self.visitor_items:
                    dot = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
                    self.visitor_items[vid] = dot
                else:
                    self.canvas.coords(self.visitor_items[vid], x-5, y-5, x+5, y+5)
                    
        except Exception as e:
            print(f"Error updating visitor positions: {e}")
            
        # Schedule next update
        self.master.after(100, self.update_visitors)

def start_gui(visitor_threads, time_manager):
    root = tk.Tk()
    root.title("Retiro Park Simulation")
    gui = ParkGUI(root, visitor_threads, time_manager)
    root.mainloop()
