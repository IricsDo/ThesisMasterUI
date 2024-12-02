import customtkinter as ctk
from MainScreen import main_screen
import os
import threading
import time
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

if __name__ == "__main__":
    ms = main_screen.MainScreen()
    ms.resizable(False, False)
    ms.attributes("-topmost", True)
    ms.mainloop()

