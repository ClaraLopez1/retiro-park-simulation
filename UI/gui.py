import tkinter as tk
from PIL import Image, ImageTk  # Pillow is needed for JPG images
import threading

import Time_manager as time_manager


class ParkGUI:
    def __init__(self, master, visitor_threads, time_manager):
        self.master = master
        self.time_manager = time_manager
        # Load the JPG image using PIL
        pil_image = Image.open("UI/retiro.jpg")
        self.bg_image = ImageTk.PhotoImage(pil_image)

        # Set the canvas size to match the image dimensions
        self.width = self.bg_image.width()
        self.height = self.bg_image.height()

        # Create the canvas using the image dimensions
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        # Draw the background image at the top-left corner
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.time_label = tk.Label(master, font=("Arial", 14), bg="white")
        self.time_label.place(x=10, y=10)
        self.day_label = tk.Label(master, font=("Arial", 12), bg="white", fg="blue")
        self.day_label.place(x=10, y=40)

        self.visitor_threads = visitor_threads

        self.visitor_items = {}  # Dictionary to store each visitor's dot

        self.update_gui()

    def update_gui(self):
        for visitor in self.visitor_threads:
            vid = visitor.visitor_id
            # Get the visitor's current coordinates (assumed to be a tuple)
            x, y = visitor.coords
            # Convert to integers (in case they're floats)
            # x, y = int(x), int(y)
            if vid not in self.visitor_items:
                # Create a new dot (oval) for the visitor if it doesn't exist
                dot = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
                self.visitor_items[vid] = dot
            else:
                # Update the dot's position on the canvas
                self.canvas.coords(self.visitor_items[vid], x - 5, y - 5, x + 5, y + 5)
        # Schedule the next update after 100 milliseconds
        self.master.after(100, self.update_gui)
        self.time_label.config(text=f"Time: {self.time_manager.get_current_time()}")
        self.day_label.config(text=f"Day: {self.time_manager.get_current_day()}")


def start_gui(visitor_threads, time_manager):
    root = tk.Tk()
    root.title("Retiro Park Simulation")
    gui = ParkGUI(root, visitor_threads, time_manager)
    root.mainloop()

