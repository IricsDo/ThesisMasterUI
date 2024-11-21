import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


def open_directory_dialog():
    directory_path = filedialog.askdirectory(
        title="Select a Directory",
    )
    if directory_path:
        print(f"Selected directory: {directory_path}")


class CircleToCircle:
    def __init__(self, canvas, x, y, r, color="black"):
        """Initialize a Circle on the canvas with center (x, y), radius r, and specified color."""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color

        # Draw the circle
        self.id = self.canvas.create_oval(
            x - r, y - r, x + r, y + r, fill=color, outline=""
        )

        # Placeholder for text inside the circle
        self.text_id = None

    def add_text(self, text, font=("Arial", 16), text_color="white"):
        """Add text to the center of the circle."""
        if self.text_id is None:
            self.text_id = self.canvas.create_text(
                self.x, self.y, text=text, font=font, fill=text_color
            )
        else:
            self.canvas.itemconfig(self.text_id, text=text, font=font, fill=text_color)

    def move(self, dx, dy):
        """Move the circle and its text by dx and dy."""
        self.canvas.move(self.id, dx, dy)
        if self.text_id:
            self.canvas.move(self.text_id, dx, dy)
        # Update the center position
        self.x += dx
        self.y += dy

    def draw_line_to(
        self,
        other_circle,
        color="black",
        width=2,
        label=None,
        label_font=("Carlito", 12, "bold"),
        label_color="black",
    ):
        """Draw a line from the right edge of this circle to the left edge of another circle, with optional label."""
        # Start point: right edge of the first circle
        start_x = self.x + self.r
        start_y = self.y

        # End point: left edge of the second circle
        end_x = other_circle.x - other_circle.r
        end_y = other_circle.y

        # Draw the line
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=width)

        # Calculate the midpoint of the line
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        # Offset the text slightly above the line
        text_offset = -30  # Adjust this value to control the distance above the line

        # Add label text above the line midpoint if a label is provided
        if label:
            self.canvas.create_text(
                mid_x,
                mid_y + text_offset,
                text=label,
                font=label_font,
                fill=label_color,
            )


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Thesis Master UI")
        self.geometry(f"{660}x{300}")

        # configure grid layout (1x3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.create_in_out()
        self.create_setting()
        self.create_status()

    def create_in_out(self):
        # create in/out folder frame with widgets
        self.in_out_frame = ctk.CTkFrame(self, height=75, corner_radius=0)
        self.in_out_frame.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.in_out_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.in_entry = ctk.CTkEntry(
            self.in_out_frame, placeholder_text="This entry must not empty"
        )
        self.in_entry.grid(row=0, column=0, columnspan=5, padx=2, pady=2, sticky="nsew")
        self.in_entry.configure(state="readonly")

        self.out_entry = ctk.CTkEntry(
            self.in_out_frame, placeholder_text="This entry must not empty"
        )
        self.out_entry.grid(
            row=1, column=0, columnspan=5, padx=2, pady=2, sticky="nsew"
        )
        self.out_entry.configure(state="readonly")

        self.in_button = ctk.CTkButton(
            self.in_out_frame,
            corner_radius=4,
            text="Input Directory",
            command=open_directory_dialog,
        )
        self.in_button.grid(row=0, column=5, padx=2, pady=2, sticky="nsew")

        self.out_button = ctk.CTkButton(
            self.in_out_frame,
            corner_radius=4,
            text="Output Directory",
            command=open_directory_dialog,
        )
        self.out_button.grid(row=1, column=5, padx=2, pady=2, sticky="nsew")

    def create_setting(self):
        # create setting frame with widgets
        self.setting_frame = ctk.CTkFrame(self, height=120, corner_radius=0)
        self.setting_frame.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.setting_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.para_frame = ctk.CTkFrame(self.setting_frame, height=120, corner_radius=0)
        self.para_frame.grid(
            row=0, column=0, columnspan=3, padx=2, pady=2, sticky="nsew"
        )
        self.para_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.para_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.type_label = ctk.CTkLabel(
            self.para_frame, text="Type map:", fg_color="transparent"
        )
        self.type_label.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.epochs_label = ctk.CTkLabel(
            self.para_frame, text="Epochs", fg_color="transparent"
        )
        self.epochs_label.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkLabel1 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel1", fg_color="transparent"
        )
        self.CTkLabel1.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkLabel2 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel2", fg_color="transparent"
        )
        self.CTkLabel2.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")

        self.type_entry = ctk.CTkEntry(self.para_frame, placeholder_text="The atomic")
        self.type_entry.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.epoch_entry = ctk.CTkEntry(
            self.para_frame, placeholder_text="Number of loop"
        )
        self.epoch_entry.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry1 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry1")
        self.CTkEntry1.grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry2 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry2")
        self.CTkEntry2.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")

        self.opt_frame = ctk.CTkFrame(self.setting_frame, height=120, corner_radius=0)
        self.opt_frame.grid(row=0, column=3, padx=2, pady=2, sticky="nsew")
        self.opt_frame.grid_rowconfigure((0, 1, 2, 4), weight=1)

        self.log_checkbox = ctk.CTkCheckBox(self.opt_frame, text="Show log")
        self.log_checkbox.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.log_checkbox.grid_anchor = "center"
        self.auto_checkbox = ctk.CTkCheckBox(self.opt_frame, text="Auto close")
        self.auto_checkbox.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.auto_checkbox.grid_anchor = "center"
        self.verbose_checkbox = ctk.CTkCheckBox(self.opt_frame, text="Enable verbose")
        self.verbose_checkbox.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.verbose_checkbox.grid_anchor = "center"
        self.CTkCheckBox1 = ctk.CTkCheckBox(self.opt_frame, text="CTkCheckBox1")
        self.CTkCheckBox1.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox1.grid_anchor = "center"

        self.start_frame = ctk.CTkFrame(self.setting_frame, height=120, corner_radius=0)
        self.start_frame.grid(row=0, column=4, padx=2, pady=2)
        self.start_frame.grid_rowconfigure((0, 1), weight=1)

        self.start_button = ctk.CTkButton(
            self.start_frame, text="Start", anchor="center", corner_radius=4
        )
        self.start_button.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkButton1 = ctk.CTkButton(
            self.start_frame, text="Clear", anchor="center", corner_radius=4
        )
        self.CTkButton1.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")

    def create_status(self):
        # create status frame with widgets
        self.status_frame = ctk.CTkFrame(self, height=106, corner_radius=0)
        self.status_frame.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.status_frame.grid_columnconfigure(
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1
        )

        r_circle = 32
        x_base = 48
        height_base = 106
        connection_line_distance = 80

        self.canvas = ctk.CTkCanvas(
            self.status_frame,
            width=r_circle,
            height=height_base,
            highlightthickness=0,
            bg="#2b2b2b",
        )
        self.canvas.grid(row=0, column=0, columnspan=11, sticky="nsew")

        color_text_in_circle = "black"
        color_circle = "green"
        color_connection_line = "red"
        color_text_on_line = "yellow"

        circle1 = CircleToCircle(
            self.canvas, x=x_base, y=height_base / 2, r=r_circle, color=color_circle
        )
        circle2 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 2 + connection_line_distance,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        circle1.add_text(
            "1", font=("Helvetica", 20, "bold"), text_color=color_text_in_circle
        )
        circle2.add_text(
            "2", font=("Helvetica", 20, "bold"), text_color=color_text_in_circle
        )

        circle1.draw_line_to(
            circle2,
            color=color_connection_line,
            width=8,
            label="Checking ...",
            label_color=color_text_on_line,
        )

        circle3 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 4 + connection_line_distance * 2,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        circle4 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 6 + connection_line_distance * 3,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        circle3.add_text(
            "3", font=("Helvetica", 20, "bold"), text_color=color_text_in_circle
        )
        circle4.add_text(
            "4", font=("Helvetica", 20, "bold"), text_color=color_text_in_circle
        )

        circle2.draw_line_to(
            circle3,
            color=color_connection_line,
            width=8,
            label="Scanning ...",
            label_color=color_text_on_line,
        )
        circle3.draw_line_to(
            circle4,
            color=color_connection_line,
            width=8,
            label="Combining ...",
            label_color=color_text_on_line,
        )

        circle5 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 8 + connection_line_distance * 4,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        circle6 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 10 + connection_line_distance * 5,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        circle5.add_text(
            "5", font=("Helvetica", 20, "bold"), text_color=color_text_in_circle
        )
        circle6.add_text(
            "6", font=("Helvetica", 20, "bold"), text_color=color_text_in_circle
        )

        circle4.draw_line_to(
            circle5,
            color=color_connection_line,
            width=8,
            label="Training ...",
            label_color=color_text_on_line,
        )
        circle5.draw_line_to(
            circle6,
            color=color_connection_line,
            width=8,
            label="Evaluating ...",
            label_color=color_text_on_line,
        )


if __name__ == "__main__":
    app = App()
    app.resizable(False, False)
    app.mainloop()
