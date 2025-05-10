import tkinter as tk
from PIL import Image, ImageTk  # Pillow is needed for JPG images
import threading
import sys

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

        time_frame = tk.Frame(master, bg="white", bd=2, relief="ridge")
        time_frame.place(x=self.width - 160, y=10)

        # Día
        self.day_label = tk.Label(
            time_frame,
            text="",
            font=("Helvetica", 11, "bold"),
            bg="white",
            fg="#2E8B57",  # SeaGreen
            justify="center",
            anchor="center"
        )
        self.day_label.pack(padx=10, pady=(5, 0))

        # Hora
        self.time_label = tk.Label(
            time_frame,
            text="",
            font=("Helvetica", 13, "bold"),
            bg="white",
            fg="#006400",  # DarkGreen
            justify="center",
            anchor="center"
        )
        self.time_label.pack(padx=10, pady=(0, 5))

        self.visitor_threads = visitor_threads

        self.visitor_items = {}  # Dictionary to store each visitor's dot
        
        # Flag to track when all visitors have left
        self.all_visitors_exited = False
        # Time when all visitors exited
        self.exit_time = None

        self.update_gui()
        
        # Start checking if all visitors have exited
        self.check_all_visitors_exited()

    def update_gui(self):
        for visitor in self.visitor_threads:
            # Only filter visitors who haven't entered yet
            if not visitor.entered:
                continue

            vid = visitor.visitor_id
            x, y = visitor.coords
            
            if vid not in self.visitor_items:
                dot = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
                self.visitor_items[vid] = dot
            else:
                # Update the dot's position on the canvas
                self.canvas.coords(self.visitor_items[vid], x - 5, y - 5, x + 5, y + 5)
                
                # Change color if visitor is leaving/not running
                if not visitor.running:
                    self.canvas.itemconfig(self.visitor_items[vid], fill="blue")
                else:
                    self.canvas.itemconfig(self.visitor_items[vid], fill="red")
                
        # Schedule the next update after 100 milliseconds
        self.master.after(100, self.update_gui)
        self.time_label.config(text=self.time_manager.get_current_time())
        self.day_label.config(text=self.time_manager.get_current_day())
    
    def check_all_visitors_exited(self):
        """Check if all visitors have exited the park and close if they have"""
        # Skip check if we haven't closed the park yet
        if int(self.time_manager.get_current_time().split(":")[0]) < 22:
            self.master.after(5000, self.check_all_visitors_exited)
            return
            
        # Count visitors still running
        active_visitors = sum(1 for visitor in self.visitor_threads if visitor.running)
        
        # If all visitors have exited but we haven't set the flag yet
        if active_visitors == 0 and not self.all_visitors_exited:
            self.all_visitors_exited = True
            self.exit_time = self.time_manager.get_current_time()
            print(f"All visitors have exited the park at {self.exit_time}. Simulation will end in 20 seconds.")
            
            # Schedule the final shutdown after 20 seconds
            self.master.after(20000, self.shutdown_simulation)
            return
            
        # If there are still visitors, check again in 2 seconds
        if not self.all_visitors_exited:
            self.master.after(2000, self.check_all_visitors_exited)
    
    def shutdown_simulation(self):
        """Shutdown the simulation after all visitors have exited"""
        print(f"Closing simulation after 20-second delay. Final time: {self.time_manager.get_current_time()}")
        self.master.destroy()

def start_gui(visitor_threads, time_manager):
    root = tk.Tk()
    root.title("Retiro Park Simulation")
    gui = ParkGUI(root, visitor_threads, time_manager)
    root.mainloop()

