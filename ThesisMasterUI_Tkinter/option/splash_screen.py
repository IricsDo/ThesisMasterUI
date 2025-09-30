import customtkinter as ctk
import os
import threading
import time
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class SplashScreen:
    def __init__(self, root):
        self.root = root

        self.root.title("Splash Screen")
        self.root.geometry("550x300")
        self.root.overrideredirect(True)

        self.image_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "images"
        )
        logo_image = ctk.CTkImage(
            Image.open(os.path.join(self.image_path, "ai_512.png"))
        )

        ctk.CTkLabel(
            self.root,
            text=" CustomTkinter",
            image=logo_image,
            compound="left",
            font=("Poppins", 63, "bold"),
            text_color="white",
        ).pack(padx=10, pady=100, anchor="center")

        self.get_started_button = ctk.CTkButton(
            self.root,
            text="Get Started",
            font=("IBM Plex Sans", 20),
            corner_radius=0,
            height=40,
            width=40,
            command=self.get_started,
        )
        self.get_started_button.pack(side="top", ipadx=10)

        self.text = ctk.CTkLabel(
            self.root,
            text="Please wait...The First launch of the app may take longer...",
            font=("IBM Plex Sans", 15),
        )
        self.progressbar = ctk.CTkProgressBar(
            self.root,
            orientation="horizontal",
            width=300,
            mode="determinate",
            determinate_speed=0.35,
            fg_color="white",
            height=8,
            progress_color="#1ED765",
            corner_radius=0,
        )

        self.center_window(self.root)

    def get_started(self):
        self.get_started_button.pack_forget()
        self.progressbar.pack(side="bottom", fill="x")
        self.text.pack(side="bottom", anchor="center")
        self.thread = threading.Thread(target=self.loading)
        self.thread.start()
        self.progressbar.set(0)
        self.progressbar.start()

    def loading(self):
        time.sleep(3)  # Simulate loading time
        self.root.after(0, self.update_ui)

    def update_ui(self):
        self.text.configure(text="")
        self.text.configure(
            text="Please wait.....The First launch of the app may take longer..."
        )
        self.progressbar.stop()
        self.progressbar.set(100)
        self.root.after(500, self.open_new_window)

    def open_new_window(self):
        # Hide the splash screen
        self.root.withdraw()

        # Create and launch the main application window
        win = ctk.CTk()
        win.geometry("1000x600")
        main_label = ctk.CTkLabel(
            win, text="Welcome to the Main Window!", font=("monospace", 50)
        )
        main_label.pack(pady=50)
        win.mainloop()
        # Once the main window is closed, destroy the splash screen
        self.root.destroy()

    def center_window(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry("{}x{}+{}+{}".format(width, height, x, y))


if __name__ == "__main__":
    root = ctk.CTk(fg_color="#222")
    SplashScreen(root)
    root.mainloop()
