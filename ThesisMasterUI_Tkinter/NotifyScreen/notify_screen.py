import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from enum import Enum


class TypeNotify(Enum):
    INFOR = 1
    WARNING = 2
    ERROR = 3
    COUNT = 4


MAP_ICON = {1: "information.png", 2: "warning.png", 3: "error.png"}
MAP_COLOR = {1: "blue", 2: "yellow", 3: "red"}


class NotifyScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.text_body = None
        self.type_notify = None

        # Create the main window
        self.title("Notification")
        self.configure(bg="black")

        width = 450
        height = 150
        scaleFactor= 1.25
        screen_width = int(self.winfo_screenwidth() * scaleFactor)
        screen_height = self.winfo_screenheight()

        # Calculate position coordinates
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the window geometry
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.resizable(False, False)
        self.overrideredirect(True)
        self.attributes("-topmost", True)

    def set_icon(self, icon_photo):
        self.icon_photo = icon_photo
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, self.icon_photo)) 

    def set_content(self, text_body : str):
        self.text_body = text_body

    def set_type(self, type_notify: TypeNotify):
        self.type_notify = type_notify

    def create_screen(self):
        # Create a frame for the notification
        frame = ctk.CTkFrame(
            self, width=self.winfo_width(), height=self.winfo_height(), corner_radius=8
        )
        frame.pack(pady=4, padx=4, fill="both", expand=True)

        # Header section with gradient-style text
        header = ctk.CTkLabel(
            frame, text="System Notify", font=("Helvetica", 24, "bold")
        )
        header.configure(text_color="skyblue")
        header.pack(anchor="n", pady=5)
        header.configure(fg_color="transparent")  # Transparent background

        image_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "images"
        )

        icon_image = Image.open(
            os.path.join(image_path, MAP_ICON[self.type_notify.value])
        )
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.icon_label = tk.Label(frame, image=icon_photo, bg="#212121")
        self.icon_label.image = icon_photo  # Keep a reference to prevent garbage collection
        self.icon_label.place(x=10, y=50)

        # Error message label
        self.message_label = ctk.CTkLabel(
            frame,
            text=self.text_body,
            font=("Helvetica", 20, "bold"),
            text_color=MAP_COLOR[self.type_notify.value],
        )
        self.message_label.pack(anchor="n", padx=0, pady=10)

        # Close button
        close_button = ctk.CTkButton(
            frame,
            text="Close",
            fg_color="skyblue",
            text_color="black",
            width=80,
            font=("Helvetica", 12, "bold"),
            command=self.hide_window,
        )
        close_button.pack(side="right", padx=10, pady=10)

    def hide_window(self):
        self.text_body = None
        self.type_notify = None

        """Hide the window."""
        self.withdraw()  # Makes the window invisible

    def show_window(self, text_body : str, type_notify : TypeNotify):
        self.set_content(text_body)
        self.set_type(type_notify)
        self.create_screen()
        """Show the window."""
        self.deiconify()  # Makes the window visible

    def close_window(self):
        """Quit the application."""
        self.destroy()
