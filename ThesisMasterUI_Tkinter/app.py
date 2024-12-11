import customtkinter as ctk
from MainScreen import main_screen
from utils import show_log

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

if __name__ == "__main__":
    try:
        show_log.print_with_timestep("App initialize")
        ms = main_screen.MainScreen()
        ms.resizable(False, False)
        ms.attributes("-topmost", True)
        show_log.print_with_timestep("App start")
        ms.mainloop()
    except Exception as e:
        show_log.print_with_timestep(e)
    finally:
        show_log.print_with_timestep("App Goodbye User <3!!")


