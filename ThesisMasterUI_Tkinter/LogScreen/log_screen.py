import customtkinter as ctk
from tkinter import messagebox
from utils.show_log import print_with_timestep


class LoggerUI(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Window settings
        self.title("Logger UI")

        width = 640
        height = 360
        scaleFactor = 1.25
        screen_width = int(self.winfo_screenwidth() * scaleFactor)

        # Calculate position coordinates
        x = screen_width - width - 180
        y = 0

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set the window geometry
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Call the method to build the UI
        self.build_ui()

        self.resizable(False, False)
        # self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.hide_window()

    def set_icon(self, icon_photo):
        self.icon_photo = icon_photo
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, self.icon_photo))

    def on_close(self):
        """Handle the event when the X button is pressed."""
        # Display a message or ignore the close event
        messagebox.showinfo("Action Denied", "Can not close this window")

    def build_ui(self):
        """Build the UI components."""
        # Main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Logger",
            font=("Helvetica", 20, "bold"),
            text_color=("blue", "#00BFFF"),
        )
        self.title_label.pack(pady=10)

        # Textbox for the logger
        self.textbox = ctk.CTkTextbox(
            self.main_frame, width=600, height=300, corner_radius=10
        )
        self.textbox.configure(
            state="disabled", spacing1=2, spacing2=5, spacing3=2
        )  # This makes the textbox read-only
        self.textbox._textbox.configure(
            font=("Consolas", 14)
        )  # Use the `_textbox` attribute
        self.textbox.pack(pady=0, padx=0)

    def add_log(self, log_text):
        """Add logs to the textbox."""
        self.textbox.configure(state="normal")
        self.textbox.insert("end", log_text)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def clear_log(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")

    def hide_window(self):
        """Hide the window."""
        self.withdraw()  # Makes the window invisible

    def show_window(self):
        """Show the window."""
        self.deiconify()  # Makes the window visible

    def close_window(self):
        """Quit the application."""
        self.destroy()
