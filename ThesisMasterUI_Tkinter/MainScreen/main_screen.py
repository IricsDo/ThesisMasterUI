import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from threading import Thread, Lock, Event
import time
from LogScreen import log_screen 
from tkinter import messagebox
from NotifyScreen import notify_screen
from NotifyScreen.notify_screen import TypeNotify
from PIL import Image, ImageTk
import os
from MainScreen.components import CircleToCircle

class MainScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Thesis Master UI")
        width = 780
        height = 320
        scaleFactor= 1.25
        screen_width = int(self.winfo_screenwidth() * scaleFactor)
        screen_height = self.winfo_screenheight()

        # Calculate position coordinates
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the window geometry
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.main_font = ("Arial", 14, "bold")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.thread_phase1 = None
        self.circle1 = None
        self.circle2 = None
        self.circle3 = None
        self.circle4 = None
        self.circle5 = None
        self.circle6 = None

        # configure grid layout (1x3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.create_in_out()
        self.create_setting()
        self.create_status()

        self.windows = []

        self.log_screen = log_screen.LoggerUI(self)
        self.log_screen.hide_window()
        self.notify_screen = notify_screen.NotifyScreen(self)
        self.notify_screen.hide_window()
        
        self.windows.append(self.log_screen)
        self.windows.append(self.notify_screen)

        self.stop_event = Event()

        self.set_icon()

    def set_icon(self):
        image_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "images"
        )
        icon_path = Image.open(
            os.path.join(image_path, "ai_64.ico")
        )
        """Set the window icon."""
        try:
            # Use Pillow to load the icon as a PhotoImage
            self.icon_photo = ImageTk.PhotoImage(icon_path)

            # Apply the icon to the window
            self.wm_iconbitmap()
            self.iconphoto(False, self.icon_photo)
            self.log_screen.set_icon(self.icon_photo)
            self.notify_screen.set_icon(self.icon_photo)

        except Exception as e:
            print(f"Error setting icon: {e}")

    def on_close(self):
        """Handle the event when the X button is pressed."""
        # Display a message or ignore the close event
        messagebox.showinfo("Action Denied", "Can not close this window")
        # self.close_sub_windows()

    def close_sub_windows(self):
        """Close all open windows."""
        for window in self.windows:
            window.destroy()
        self.windows.clear()

    def open_directory_dialog(self, identifier):
        directory_path = filedialog.askdirectory(
            title="Select a Directory",
        )
        if directory_path:
            print(f"Selected directory: {directory_path}")

        if identifier == "in":
            self.in_entry.configure(state="normal")
            self.in_entry.insert(0, directory_path)
            self.in_entry.configure(state="readonly")

        elif identifier == "out":
            self.out_entry.configure(state="normal")
            self.out_entry.insert(0, directory_path)
            self.out_entry.configure(state="readonly")

        else:
            print(f"The identifier not vaild")

    def create_in_out(self):
        # create in/out folder frame with widgets
        self.in_out_frame = ctk.CTkFrame(self, height=75, corner_radius=0)
        self.in_out_frame.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.in_out_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.in_entry = ctk.CTkEntry(
            self.in_out_frame, placeholder_text="This entry must not empty", font=self.main_font
        )
        self.in_entry.grid(row=0, column=0, columnspan=5, padx=2, pady=2, sticky="nsew")
        self.in_entry.configure(state="readonly")

        self.out_entry = ctk.CTkEntry(
            self.in_out_frame, placeholder_text="This entry must not empty", font=self.main_font
        )
        self.out_entry.grid(
            row=1, column=0, columnspan=5, padx=2, pady=2, sticky="nsew"
        )
        self.out_entry.configure(state="readonly")

        self.in_button = ctk.CTkButton(
            self.in_out_frame,
            font=self.main_font,
            corner_radius=4,
            text="Input Directory",
            command=lambda: self.open_directory_dialog("in"),
        )
        self.in_button.grid(row=0, column=5, padx=2, pady=2, sticky="nsew")

        self.out_button = ctk.CTkButton(
            self.in_out_frame,
            font=self.main_font,
            corner_radius=4,
            text="Output Directory",
            command=lambda: self.open_directory_dialog("out"),
        )
        self.out_button.grid(row=1, column=5, padx=2, pady=2, sticky="nsew")

    def create_setting(self):
        # create setting frame with widgets
        self.setting_frame = ctk.CTkFrame(self, height=120, corner_radius=0)
        self.setting_frame.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        self.setting_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.para_frame = ctk.CTkFrame(self.setting_frame, height=120, corner_radius=0)
        self.para_frame.grid(
            row=0, column=0, columnspan=4, padx=2, pady=2, sticky="nsew"
        )
        self.para_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.para_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.CTkLabel1 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel1", fg_color="transparent", font=self.main_font
        )
        self.CTkLabel1.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkLabel2 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel2", fg_color="transparent", font=self.main_font
        )
        self.CTkLabel2.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkLabel3 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel3", fg_color="transparent", font=self.main_font
        )
        self.CTkLabel3.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkLabel4 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel4", fg_color="transparent", font=self.main_font
        )
        self.CTkLabel4.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")

        self.CTkEntry1 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry1", font=self.main_font)
        self.CTkEntry1.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry2 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry2", font=self.main_font)
        self.CTkEntry2.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry3 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry3", font=self.main_font)
        self.CTkEntry3.grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry4 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry4", font=self.main_font)
        self.CTkEntry4.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")

        self.CTkLabel5 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel5", fg_color="transparent", font=self.main_font
        )
        self.CTkLabel5.grid(row=0, column=2, padx=2, pady=2, sticky="nsew")

        self.CTkLabel6 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel6", fg_color="transparent", font=self.main_font
        )
        self.CTkLabel6.grid(row=1, column=2, padx=2, pady=2, sticky="nsew")

        self.CTkLabel7 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel7", fg_color="transparent", font=self.main_font
        )
        self.CTkLabel7.grid(row=2, column=2, padx=2, pady=2, sticky="nsew")

        self.CTkLabel8 = ctk.CTkLabel(
            self.para_frame, text="CTkLabel8", fg_color="transparent", font=self.main_font
        )
        self.CTkLabel8.grid(row=3, column=2, padx=2, pady=2, sticky="nsew")

        self.CTkEntry5 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry5", font=self.main_font)
        self.CTkEntry5.grid(row=0, column=3, padx=2, pady=2, sticky="nsew")
        self.CTkEntry6 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry6", font=self.main_font)
        self.CTkEntry6.grid(row=1, column=3, padx=2, pady=2, sticky="nsew")
        self.CTkEntry7 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry7", font=self.main_font)
        self.CTkEntry7.grid(row=2, column=3, padx=2, pady=2, sticky="nsew")
        self.CTkEntry8 = ctk.CTkEntry(self.para_frame, placeholder_text="CTkEntry8", font=self.main_font)
        self.CTkEntry8.grid(row=3, column=3, padx=2, pady=2, sticky="nsew")

        self.opt_frame = ctk.CTkFrame(self.setting_frame, height=120, corner_radius=0)
        self.opt_frame.grid(row=0, column=4, padx=2, pady=2, sticky="nsew")
        self.opt_frame.grid_rowconfigure((0, 1, 2, 4), weight=1)

        self.CTkCheckBox1 = ctk.CTkCheckBox(self.opt_frame, text="CTkCheckBox1", font=self.main_font)
        self.CTkCheckBox1.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox1.grid_anchor = "center"
        self.CTkCheckBox2 = ctk.CTkCheckBox(self.opt_frame, text="CTkCheckBox2", font=self.main_font)
        self.CTkCheckBox2.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox2.grid_anchor = "center"
        self.CTkCheckBox3 = ctk.CTkCheckBox(self.opt_frame, text="CTkCheckBox3", font=self.main_font)
        self.CTkCheckBox3.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox3.grid_anchor = "center"
        self.show_log = ctk.CTkSwitch(self.opt_frame, text="Log Off", command= self.show_log_change,
                                        font=self.main_font,
        )
        self.show_log.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        self.show_log.grid_anchor = "center"

        self.process_frame = ctk.CTkFrame(
            self.setting_frame, height=120, corner_radius=0
        )
        self.process_frame.grid(row=0, column=5, padx=2, pady=2)
        self.process_frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.start_button = ctk.CTkButton(
            self.process_frame,
            font=self.main_font,
            text="Start",
            anchor="center",
            corner_radius=4,
            command=self.start_button_click,
        )
        self.is_process_starting = False

        self.start_button.grid(row=0, column=0, padx=2, pady=5, sticky="nsew")
        self.reset_button = ctk.CTkButton(
            self.process_frame,
            font=self.main_font,
            text="Reset",
            anchor="center",
            corner_radius=4,
            command=self.reset_app,
        )
        self.reset_button.grid(row=1, column=0, padx=2, pady=5, sticky="nsew")

        self.progress_bar = ctk.CTkProgressBar(
            self.process_frame, orientation="horizontal", mode="indeterminate"
        )
        self.progress_bar.configure(progress_color="gray")
        self.progress_bar.grid(row=2, column=0, padx=2, pady=30, sticky="nsew")

    def create_status(self):
        # create status frame with widgets
        self.status_frame = ctk.CTkFrame(self, height=106, corner_radius=0)
        self.status_frame.grid(row=2, column=0, padx=2, pady=2, sticky="ew")
        self.status_frame.grid_columnconfigure(
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1
        )

        r_circle = 32
        x_base = 48
        height_base = 106
        connection_line_distance = 110

        self.canvas = ctk.CTkCanvas(
            self.status_frame,
            width=r_circle,
            height=height_base,
            highlightthickness=0,
            bg="#2b2b2b",
        )
        self.canvas.grid(row=0, column=0, columnspan=11, sticky="nsew")

        color_text_in_circle = "black"
        color_circle = "dimgray"
        color_connection_line = "dimgray"
        color_text_on_line = "dimgray"

        self.circle1 = CircleToCircle(
            self.canvas, x=x_base, y=height_base / 2, r=r_circle, color=color_circle
        )
        self.circle2 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 2 + connection_line_distance,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        self.circle1.add_text("1", font=self.main_font, text_color=color_text_in_circle)
        self.circle2.add_text("2", font=self.main_font, text_color=color_text_in_circle)

        self.circle1.draw_line_to(
            self.circle2,
            color=color_connection_line,
            width=8,
            label="Checking ...",
            label_color=color_text_on_line,
        )

        self.circle3 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 4 + connection_line_distance * 2,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        self.circle4 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 6 + connection_line_distance * 3,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        self.circle3.add_text("3", font=self.main_font, text_color=color_text_in_circle)
        self.circle4.add_text("4", font=self.main_font, text_color=color_text_in_circle)

        self.circle2.draw_line_to(
            self.circle3,
            color=color_connection_line,
            width=8,
            label="Scanning ...",
            label_color=color_text_on_line,
        )
        self.circle3.draw_line_to(
            self.circle4,
            color=color_connection_line,
            width=8,
            label="Combining ...",
            label_color=color_text_on_line,
        )

        self.circle5 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 8 + connection_line_distance * 4,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        self.circle6 = CircleToCircle(
            self.canvas,
            x=x_base + r_circle * 10 + connection_line_distance * 5,
            y=height_base / 2,
            r=r_circle,
            color=color_circle,
        )
        self.circle5.add_text("5", font=self.main_font, text_color=color_text_in_circle)
        self.circle6.add_text("6", font=self.main_font, text_color=color_text_in_circle)

        self.circle4.draw_line_to(
            self.circle5,
            color=color_connection_line,
            width=8,
            label="Training ...",
            label_color=color_text_on_line,
        )
        self.circle5.draw_line_to(
            self.circle6,
            color=color_connection_line,
            width=8,
            label="Evaluating ...",
            label_color=color_text_on_line,
        )

    def set_group_control(self, state_control : str, except_reset_button : bool = False, except_start_button : bool = False):
        self.in_button.configure(state=state_control)
        self.out_button.configure(state=state_control)

        self.CTkEntry1.configure(state=state_control)
        self.CTkEntry2.configure(state=state_control)
        self.CTkEntry3.configure(state=state_control)
        self.CTkEntry4.configure(state=state_control)
        self.CTkEntry5.configure(state=state_control)
        self.CTkEntry6.configure(state=state_control)
        self.CTkEntry7.configure(state=state_control)
        self.CTkEntry8.configure(state=state_control)

        self.CTkCheckBox1.configure(state=state_control)
        self.CTkCheckBox2.configure(state=state_control)
        self.CTkCheckBox3.configure(state=state_control)
        self.show_log.configure(state=state_control)

        if not except_reset_button:
            self.reset_button.configure(state=state_control)

        if not except_start_button:
            self.start_button.configure(state=state_control)

    def toggle_start_button(self):
        self.is_process_starting = not self.is_process_starting

        self.start_button.configure(
            text="Stop" if self.is_process_starting else "Start",
            text_color="red" if self.is_process_starting else "white",
        )
    def start_button_click(self):
        self.toggle_start_button()

        commo_state = "disabled" if self.is_process_starting else "normal"

        self.set_group_control(commo_state, except_start_button = True)  

        if not self.thread_phase1 and self.is_process_starting:
            self.stop_event.clear()
            self.thread_phase1 = Thread(target=self.phase1_calling, daemon=True)
            self.thread_phase1.start()
        elif self.thread_phase1 and not self.is_process_starting:
            self.stop_thread()
            self.set_group_control("disabled")  


    def check_thread_termination(self):
        """Check periodically if the thread has stopped."""
        if self.thread_phase1 and self.thread_phase1.is_alive():
            self.after(100, self.check_thread_termination)  # Check again after 100ms

    def stop_thread(self):
        """Signal the thread to stop and wait for it."""
        self.stop_event.set()
        self.check_thread_termination()

    def phase1_calling(self):
        self.progress_bar.configure(progress_color="aqua")
        self.progress_bar.start()

        circles = [
            self.circle1,
            self.circle2,
            self.circle3,
            self.circle4,
            self.circle5,
            self.circle6,
        ]
        """Simulate a long-running task."""
        for index, circle in enumerate(circles):
            if self.stop_event.is_set():
                break

            circle.set_color_circle("orange")
            circle.set_color_line("orange")
            circle.set_color_text_line("orange")

            time.sleep(2)  # Simulate the task

            circle.set_color_text_line("green")
            circle.set_color_circle("green")
            circle.set_color_line("green")


            self.after(0, self.log_screen.add_log, "Example \n")

        self.progress_bar.stop()
        self.progress_bar.configure(progress_color="whitesmoke")
        self.thread_phase1 = None
        self.notify_screen.show_window(text_body="This is example notify", type_notify= TypeNotify.ERROR)
        self.reset_button.configure(state = "normal")
        self.start_button.configure(state = "disabled")
        self.toggle_start_button()

    def show_log_change(self):
        self.show_log.configure(text= "Log On" if self.show_log.get() else "Log Off", 
                                text_color = "aqua" if self.show_log.get() else "white")
        self.log_screen.show_window() if self.show_log.get() else self.log_screen.hide_window()

    def reset_status(self):
        circles = [
            self.circle1,
            self.circle2,
            self.circle3,
            self.circle4,
            self.circle5,
            self.circle6,
        ]
        for circle in circles: 
            circle.set_color_circle("dimgray")
            circle.set_color_line("dimgray")
            circle.set_color_text_line("dimgray")

    def reset_app(self):
        self.reset_status()
        self.set_group_control("normal")  

        self.in_entry.configure(state="normal")
        self.in_entry.delete(0, "end")
        self.in_entry.focus()
        self.in_entry.configure(state="readonly")

        self.out_entry.configure(state="normal")
        self.out_entry.delete(0, "end")
        self.out_entry.focus()
        self.out_entry.configure(state="readonly")

        self.CTkEntry1.delete(0, "end")
        self.CTkEntry2.delete(0, "end")
        self.CTkEntry3.delete(0, "end")
        self.CTkEntry4.delete(0, "end")
        self.CTkEntry5.delete(0, "end")
        self.CTkEntry6.delete(0, "end")
        self.CTkEntry7.delete(0, "end")
        self.CTkEntry8.delete(0, "end")

        self.CTkCheckBox1.deselect()
        self.CTkCheckBox2.deselect()
        self.CTkCheckBox3.deselect()
        self.show_log.deselect()

        self.log_screen.hide_window()
