import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from enum import Enum


# Initialize the customtkinter application
ctk.set_appearance_mode("Dark")  # Dark mode to match the image
ctk.set_default_color_theme("blue")

class TypeNotify(Enum):
    INFOR = 1
    WARNING = 2
    ERROR = 3
    COUNT = 4

MAP_ICON = {1: "information.png", 2: "warning.png", 3: "error.png"}
MAP_COLOR = {1: "blue", 2: "yellow", 3: "red"}

class App(ctk.CTk):
    def __init__(self, text_body : str, type_notify: TypeNotify = TypeNotify.INFOR):
        super().__init__()

        self.type_notify = type_notify
        self.text_body = text_body
        # Create the main window
        self.title("Notification")
        self.configure(bg="black")
        self.create_screen()

        width = 450
        height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position coordinates
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the window geometry
        self.geometry(f"{width}x{height}+{x}+{y}")

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

        icon_image = Image.open(os.path.join(image_path, MAP_ICON[self.type_notify.value]))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label = tk.Label(frame, image=icon_photo, bg="#2b2b2b")
        icon_label.image = icon_photo  # Keep a reference to prevent garbage collection
        icon_label.place(x=10, y=50)

        # Error message label
        message_label = ctk.CTkLabel(
            frame,
            text=self.text_body,
            font=("Helvetica", 20, "bold"),
            text_color=MAP_COLOR[self.type_notify.value],
        )
        message_label.pack(anchor="n", padx=0, pady=10)

        # Close button
        close_button = ctk.CTkButton(
            frame,
            text="Close",
            fg_color="skyblue",
            text_color="black",
            width=80,
            font=("Helvetica", 12, "bold"),
            command=self.destroy,
        )
        close_button.pack(side="right", padx=10, pady=10)


if __name__ == "__main__":
    app = App(text_body= "This is example notify", type_notify = TypeNotify.ERROR)
    app.resizable(False, False)
    app.overrideredirect(True)
    app.attributes("-topmost", True)
    app.update()
    app.attributes("-topmost", False)
    app.mainloop()
