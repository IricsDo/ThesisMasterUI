import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("dark-blue")

class CircleToCircle:
    def __init__(self, canvas, x, y, r, color="black"):
        """Initialize a Circle on the canvas with center (x, y), radius r, and specified color."""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        
        # Draw the circle
        self.id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
        
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

    def draw_line_to(self, other_circle, color="black", width=2, label=None, label_font=("Arial", 12), label_color="black"):
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
        text_offset = -10  # Adjust this value to control the distance above the line

        # Add label text above the line midpoint if a label is provided
        if label:
            self.canvas.create_text(mid_x, mid_y + text_offset, text=label, font=label_font, fill=label_color)

class CircleButton(ctk.CTkFrame):
    def __init__(self, parent, x, y, r, text, command=None):
        super().__init__(parent, width=2*r, height=2*r, fg_color="transparent")
        self.canvas = tk.Canvas(self, width=2*r, height=2*r, highlightthickness=0, bg="transparent")
        self.canvas.pack()
        
        # Draw the circle
        self.circle = self.canvas.create_oval(0, 0, 2*r, 2*r, fill="skyblue", outline="")
        
        # Add text to the center of the circle
        self.text = self.canvas.create_text(r, r, text=text, font=("Helvetica", 12, "bold"), fill="white")
        
        # Store the command to run on click
        self.command = command
        
        # Bind click event
        self.canvas.tag_bind(self.circle, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.text, "<Button-1>", self.on_click)
        
    def on_click(self, event):
        if self.command:
            self.command()

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

        self.in_entry = ctk.CTkEntry(self.in_out_frame, placeholder_text="CTkEntry")
        self.in_entry.grid(row=0, column=0, columnspan=5, padx=2, pady=2, sticky="nsew")
       
        self.out_entry = ctk.CTkEntry(self.in_out_frame, placeholder_text="CTkEntry")
        self.out_entry.grid(row=1, column=0, columnspan=5, padx=2, pady=2, sticky="nsew")

        self.in_button = ctk.CTkButton(self.in_out_frame, corner_radius=4)
        self.in_button.grid(row=0, column=5, padx=2, pady=2, sticky="nsew")

        self.out_button = ctk.CTkButton(self.in_out_frame, corner_radius=4)
        self.out_button.grid(row=1, column=5, padx=2, pady=2, sticky="nsew")

    def create_setting(self):
        # create setting frame with widgets
        self.setting_frame = ctk.CTkFrame(self, height=120, corner_radius=0)
        self.setting_frame.grid(row=1, column= 0, padx=2, pady=2, sticky="nsew")
        self.setting_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.para_frame = ctk.CTkFrame(self.setting_frame , height=120, corner_radius=0)
        self.para_frame.grid(row=0, column=0, columnspan=3, padx=2, pady=2, sticky="nsew")
        self.para_frame.grid_columnconfigure((0, 1), weight=1)
        self.para_frame.grid_rowconfigure((0, 1), weight=1)
        self.type_label = ctk.CTkLabel(self.para_frame, text="CTkLabel", fg_color="transparent")
        self.type_label.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.epoch_label = ctk.CTkLabel(self.para_frame, text="CTkLabel", fg_color="transparent")
        self.epoch_label.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.type_entry = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry")
        self.type_entry.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.epoch_entry = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry")
        self.epoch_entry.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")

        self.opt_frame = ctk.CTkFrame(self.setting_frame , height=120, corner_radius=0)
        self.opt_frame.grid(row=0, column=3, padx=2, pady=2, sticky="nsew")
        self.opt_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.log_checkbox = ctk.CTkCheckBox(self.opt_frame, text="CTkCheckBox")
        self.log_checkbox.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.log_checkbox.grid_anchor = "center"
        self.auto_checkbox = ctk.CTkCheckBox(self.opt_frame, text="CTkCheckBox")
        self.auto_checkbox.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.auto_checkbox.grid_anchor = "center"
        self.verbose_checkbox = ctk.CTkCheckBox(self.opt_frame, text="CTkCheckBox")
        self.verbose_checkbox.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.verbose_checkbox.grid_anchor = "center"

        self.start_frame = ctk.CTkFrame(self.setting_frame , height=120, corner_radius=0)
        self.start_frame.grid(row=0, column=4, padx=2, pady=2)
        self.start_button = ctk.CTkButton(self.start_frame, height=80, width=160, anchor="center", corner_radius=8)
        self.start_button.place(relx=0.5, rely=0.5, anchor='center')

    def create_status(self):
        # create status frame with widgets
        self.status_frame = ctk.CTkFrame(self, height= 106, corner_radius=0)
        self.status_frame.grid(row=2, column=0, padx= 2, pady= 2, sticky="nsew")
        self.status_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        r_circle = 32
        x_base = 64
        self.canvas = ctk.CTkCanvas(self.status_frame, width= 32, height= 106, highlightthickness=0, bg="#2b2b2b")
        self.canvas.grid(row=0, column=0, columnspan=11, sticky="nsew")

        circle1 = CircleToCircle(self.canvas, x=x_base, y= 106/2, r=r_circle, color="green")
        circle2 = CircleToCircle(self.canvas, x=x_base + 32*2 + 72, y= 106/2, r=r_circle, color="green")
        circle1.add_text("1", font=("Helvetica", 20, "bold"), text_color="yellow")
        circle2.add_text("2", font=("Helvetica", 20, "bold"), text_color="yellow")

        circle1.draw_line_to(circle2, color="red", width=8, label="Distance", label_font=("Helvetica", 12, "italic"), label_color="purple")

        circle3 = CircleToCircle(self.canvas, x=x_base + 32*4 + 72*2, y= 106/2, r=r_circle, color="green")
        circle4 = CircleToCircle(self.canvas, x=x_base + 32*6 + 72*3, y= 106/2, r=r_circle, color="green")
        circle3.add_text("3", font=("Helvetica", 20, "bold"), text_color="yellow")
        circle4.add_text("4", font=("Helvetica", 20, "bold"), text_color="yellow")

        circle2.draw_line_to(circle3, color="red", width=8, label="Distance", label_font=("Helvetica", 12, "italic"), label_color="purple")
        circle3.draw_line_to(circle4, color="red", width=8, label="Distance", label_font=("Helvetica", 12, "italic"), label_color="purple")


        circle5 = CircleToCircle(self.canvas, x=x_base + 32*8 + 72*4, y= 106/2, r=r_circle, color="green")
        circle6 = CircleToCircle(self.canvas, x=x_base + 32*10 + 72*5, y= 106/2, r=r_circle, color="green")
        circle5.add_text("5", font=("Helvetica", 20, "bold"), text_color="yellow")
        circle6.add_text("6", font=("Helvetica", 20, "bold"), text_color="yellow")

        circle4.draw_line_to(circle5, color="red", width=8, label="Distance", label_font=("Helvetica", 12, "italic"), label_color="purple")
        circle5.draw_line_to(circle6, color="red", width=8, label="Distance", label_font=("Helvetica", 12, "italic"), label_color="purple")

if __name__ == "__main__":
    app = App()
    app.mainloop()