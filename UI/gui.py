import tkinter as tk
from PIL import Image, ImageTk  # Pillow is needed for JPG images
import os


class ParkGUI:
    def __init__(self, master, visitor_threads, time_manager):
        self.master = master
        self.time_manager = time_manager

        # Load and display background image of the park
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

        # Create a styled button to manually exit the simulation
        exit_button = tk.Button(
            master,
            text="Close Simulation",
            command=self.exit_application,
            bg="blue",
            fg="green",
            font=("Arial", 15, "bold"),
            padx=15,
            pady=8,
            relief="raised",
            bd=3,
            activebackground="red",
            activeforeground="blue"
        )
        exit_button.place(x=0, y=0)

        # Display current simulation day and time
        time_frame = tk.Frame(master, bg="white", bd=2, relief="ridge")
        time_frame.place(x=self.width - 160, y=10)

        # Day
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

        # Time
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
        # Start the main update loop
        self.update_gui()
        # Start checking if all visitors have exited
        self.check_all_visitors_exited()
    
    def exit_application(self):
        """Forcibly exit the application using os._exit()"""
        print("Exiting application...")
        try:
            # Try normal shutdown first
            self.master.quit()
            self.master.destroy()
        except:
            pass
        # Force immediate termination
        os._exit(0)

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
                
                # Change color if visitor is leaving
                if not visitor.running:
                    self.canvas.itemconfig(self.visitor_items[vid], fill="blue")
                else:
                    self.canvas.itemconfig(self.visitor_items[vid], fill="red")
                
        # Schedule the next update after 100 milliseconds
        self.master.after(100, self.update_gui)

        # Refresh time and day labels
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
            print(f"All visitors have exited the park at {self.exit_time}.")
            # Schedule application exit after 5 seconds
            self.master.after(5000, self.stop_simulation)
            return
            
        # If there are still visitors, check again in 2 seconds
        if not self.all_visitors_exited:
            self.master.after(2000, self.check_all_visitors_exited)
    
    def stop_simulation(self):
        """Stop the time manager and close the application"""
        print("All visitors have exited. Stopping simulation...")
        self.time_manager.running = False
        self.exit_application()

def start_gui(visitor_threads, time_manager):
    """Entrypoint to launch the Tkinter GUI loop"""
    root = tk.Tk()
    root.title("Retiro Park Simulation")
    gui = ParkGUI(root, visitor_threads, time_manager)
    root.mainloop()

