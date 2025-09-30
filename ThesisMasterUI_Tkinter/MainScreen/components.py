class CircleToCircle:
    def __init__(self, canvas, x, y, r, color="black"):
        """Initialize a Circle on the canvas with center (x, y), radius r, and specified color."""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.line = None
        self.text_line = None

        # Draw the circle
        self.circle = self.canvas.create_oval(
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
        self.canvas.move(self.circle, dx, dy)
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
        self.line = self.canvas.create_line(
            start_x, start_y, end_x, end_y, fill=color, width=width
        )

        # Calculate the midpoint of the line
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        # Offset the text slightly above the line
        text_offset = -30  # Adjust this value to control the distance above the line

        # Add label text above the line midpoint if a label is provided
        if label:
            self.text_line = self.canvas.create_text(
                mid_x,
                mid_y + text_offset,
                text=label,
                font=label_font,
                fill=label_color,
            )

    def set_color_circle(self, color):
        if self.circle:
            self.canvas.itemconfig(self.circle, fill=color)

    def set_color_line(self, color):
        if self.line:
            self.canvas.itemconfig(self.line, fill=color)

    def set_color_text_line(self, color):
        if self.text_line:
            self.canvas.itemconfig(self.text_line, fill=color)
