import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class LoggerUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Logger UI")

        width = 640
        height = 360
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position coordinates
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set the window geometry
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Call the method to build the UI
        self.build_ui()

    def on_close(self):
        """Handle the event when the X button is pressed."""
        # Display a message or ignore the close event
        messagebox.showinfo("Action Denied", "The X button is disabled.")

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
        self.textbox._textbox.configure(
            font=("Consolas", 14)
        )  # Use the `_textbox` attribute
        self.textbox.pack(pady=0, padx=0)

        # Add example text
        sample_text = (
            "Example tessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssxt\n"
            * 10
        )  # Repeat "Example text" 10 times
        self.add_log(sample_text)

    def add_log(self, log_text):
        """Add logs to the textbox."""
        self.textbox.configure(state="normal")
        self.textbox.insert("end", log_text)
        self.textbox.configure(state="disabled", spacing1=2, spacing2=5, spacing3=2)

    def hide_window(self):
        """Hide the window."""
        self.withdraw()  # Makes the window invisible

    def show_window(self):
        """Show the window."""
        self.deiconify()  # Makes the window visible

    def close_window(self):
        """Quit the application."""
        self.destroy()


# Run the application
if __name__ == "__main__":
    app = LoggerUI()
    app.resizable(False, False)
    app.attributes("-topmost", True)
    app.update()
    app.attributes("-topmost", False)
    app.mainloop()
