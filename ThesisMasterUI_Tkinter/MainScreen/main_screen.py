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
# from MainScreen.components import CircleToCircle
from utils.exec_command import execute_command
from utils.extract_value import extract_value_from_log
from utils.show_log import print_with_timestep
import subprocess
import psutil

DISABLED_COLOR = "#737373"
ENABLED_COLOR = "#FFFFFF"

class MainScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Thesis Master UI")
        width = 780
        height = 480
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
        # self.circle1 = None
        # self.circle2 = None
        # self.circle3 = None
        # self.circle4 = None
        # self.circle5 = None
        # self.circle6 = None
        
        self.is_process_done = False
        self.current_percent_process = 0

        # configure grid layout (1 col x 4 row)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure((1, 2, 3), weight=1)

        self.create_mode()
        self.create_config_path()
        self.create_setting()
        # self.create_status_detail()
        self.create_status_common()

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
        if self.is_process_starting:
            messagebox.showinfo("Action Denied", "Process is running !!!")
        else:
            self.close_sub_windows()
            self.destroy()

    def close_sub_windows(self):
        """Close all open windows."""
        for window in self.windows:
            window.destroy()
        self.windows.clear()

    def open_directory_dialog(self, identifier):
        directory_path = filedialog.askdirectory(
            title="Select a Directory",
        )
        if not directory_path and identifier != "predict":
            print(f"Directory must be not None")

        print_with_timestep(f"Button {identifier} is clicked by the user")
        print_with_timestep(f"Path {directory_path} selected by the user")

        if identifier == "train":
            self.train_path.configure(state="normal")
            self.train_path.delete(0, "end")
            self.train_path.insert(0, directory_path)
            self.train_path.configure(state="readonly")

        elif identifier == "result":
            self.result_path.configure(state="normal")
            self.result_path.delete(0, "end")
            self.result_path.insert(0, directory_path)
            self.result_path.configure(state="readonly")

        elif identifier == "predict":
            self.predict_path.configure(state="normal")
            self.predict_path.delete(0, "end")
            self.predict_path.insert(0, directory_path)
            self.predict_path.configure(state="readonly")

        else:
            print_with_timestep(f"The identifier not vaild")
            return
        
    def create_mode(self):
        self.mode_frame = ctk.CTkFrame(self, height=32, corner_radius=0)
        self.mode_frame.grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        self.mode_frame.grid_columnconfigure((0, 1), weight=1)
        self.mode_frame.grid_rowconfigure((0), weight=1)

        self.mode_var = tk.StringVar(value="")
        self.mode_label = ctk.CTkLabel(self.mode_frame, text="Mode:", font=self.main_font)
        self.mode_label.grid(row=0, column=0, sticky="se", padx=4, pady=4)

        self.mode_menu = ctk.CTkComboBox(
            self.mode_frame, values=["Init mode", "Train mode", "Create mode", "Predict mode"],
            variable=self.mode_var, command=self.on_mode_change
        )
        self.mode_menu.grid(row=0, column=1, sticky="se", padx=4, pady=4)
        self.mode_menu.set("Init mode")
        
    def create_config_path(self):
        # create in/out folder frame with widgets
        self.config_path_frame = ctk.CTkFrame(self, height=72, corner_radius=0)
        self.config_path_frame.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.config_path_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.config_path_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.train_path = ctk.CTkEntry(
            self.config_path_frame, placeholder_text="Path to your training data", font=self.main_font
        )
        self.train_path.grid(row=0, column=0, columnspan=5, padx=2, pady=2, sticky="nsew")
        self.train_path.configure(state="readonly")

        self.result_path = ctk.CTkEntry(
            self.config_path_frame, placeholder_text="Path to save your results", font=self.main_font
        )
        self.result_path.grid(row=1, column=0, columnspan=5, padx=2, pady=2, sticky="nsew")
        self.result_path.configure(state="readonly")

        
        self.predict_path = ctk.CTkEntry(
            self.config_path_frame, placeholder_text="Path to your predict data", font=self.main_font
        )
        self.predict_path.grid(row=2, column=0, columnspan=5, padx=2, pady=2, sticky="nsew")
        self.predict_path.configure(state="readonly")

        
        self.json_path = ctk.CTkEntry(
            self.config_path_frame, placeholder_text="Path to your JSON config", font=self.main_font
        )
        self.json_path.grid(row=3, column=0, columnspan=5, padx=2, pady=2, sticky="nsew")
        self.json_path.configure(state="readonly")
        
        self.model_path = ctk.CTkEntry(
            self.config_path_frame, placeholder_text="Path to your model deep learning", font=self.main_font
        )
        self.model_path.grid(row=4, column=0, columnspan=5, padx=2, pady=2, sticky="nsew")
        self.model_path.configure(state="readonly")
        
        self.train_path_button = ctk.CTkButton(
            self.config_path_frame,
            font=self.main_font,
            corner_radius=4,
            text="Data path",
            command=lambda: self.open_directory_dialog("train"),
        )
        self.train_path_button.grid(row=0, column=5, padx=2, pady=2, sticky="nsew")
        self.train_path_button.configure(state="disabled")

        self.result_path_button = ctk.CTkButton(
            self.config_path_frame,
            font=self.main_font,
            corner_radius=4,
            text="Result path",
            command=lambda: self.open_directory_dialog("result"),
        )
        self.result_path_button.grid(row=1, column=5, padx=2, pady=2, sticky="nsew")
        self.result_path_button.configure(state="disabled")

        self.predict_path_button = ctk.CTkButton(
            self.config_path_frame,
            font=self.main_font,
            corner_radius=4,
            text="Predict path",
            command=lambda: self.open_directory_dialog("predict"),
        )
        self.predict_path_button.grid(row=2, column=5, padx=2, pady=2, sticky="nsew")
        self.predict_path_button.configure(state="disabled")

        self.json_path_button = ctk.CTkButton(
            self.config_path_frame,
            font=self.main_font,
            corner_radius=4,
            text="Json path",
            command=lambda: self.open_directory_dialog("json"),
        )
        self.json_path_button.grid(row=3, column=5, padx=2, pady=2, sticky="nsew")
        self.json_path_button.configure(state="disabled")

        self.model_path_button = ctk.CTkButton(
            self.config_path_frame,
            font=self.main_font,
            corner_radius=4,
            text="Model path",
            command=lambda: self.open_directory_dialog("model"),
        )
        self.model_path_button.grid(row=4, column=5, padx=2, pady=2, sticky="nsew")
        self.model_path_button.configure(state="disabled")

    def create_setting(self):
        # create setting frame with widgets
        self.setting_frame = ctk.CTkFrame(self, height=120, corner_radius=0)
        self.setting_frame.grid(row=2, column=0, padx=2, pady=2, sticky="ew")
        self.setting_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)


        self.para_frame1 = ctk.CTkFrame(self.setting_frame, height=120, corner_radius=0)
        self.para_frame1.grid(
            row=0, column=0, padx=2, pady=2, sticky="nsew"
        )
        self.para_frame1.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.para_frame1.grid_columnconfigure((0, 1), weight=1)

        self.CTkLabel_noh = ctk.CTkLabel(
            self.para_frame1, text="-noh", text_color=DISABLED_COLOR, fg_color="transparent", font=self.main_font
        )
        self.CTkLabel_noh.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_noh = ctk.CTkEntry(self.para_frame1, font=self.main_font)
        self.CTkEntry_noh.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_noh.configure(state="disable")

        self.CTkLabel_mld = ctk.CTkLabel(
            self.para_frame1, text="-mld", text_color=DISABLED_COLOR, fg_color="transparent", font=self.main_font
        )
        self.CTkLabel_mld.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_mld = ctk.CTkEntry(self.para_frame1, font=self.main_font)
        self.CTkEntry_mld.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_mld.configure(state="disable")
        

        self.CTkLabel_e = ctk.CTkLabel(
            self.para_frame1, text="-e", text_color=DISABLED_COLOR, fg_color="transparent", font=self.main_font
        )
        self.CTkLabel_e.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_e = ctk.CTkEntry(self.para_frame1, font=self.main_font)
        self.CTkEntry_e.grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_e.configure(state="disable")


        self.para_frame2 = ctk.CTkFrame(self.setting_frame, height=120, corner_radius=0)
        self.para_frame2.grid(
            row=0, column=1, padx=2, pady=2, sticky="nsew"
        )
        self.para_frame2.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        self.CTkCheckBox_pred_only = ctk.CTkCheckBox(self.para_frame2, text="-pred_only", font=self.main_font)
        self.CTkCheckBox_pred_only.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox_pred_only.grid_anchor = "center"
        self.CTkCheckBox_pred_only.configure(state="disabled")

        self.CTkCheckBox_omd = ctk.CTkCheckBox(self.para_frame2, text="-omd", font=self.main_font)
        self.CTkCheckBox_omd.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox_omd.grid_anchor = "center"
        self.CTkCheckBox_omd.configure(state="disabled")

        self.CTkCheckBox_sppd = ctk.CTkCheckBox(self.para_frame2, text="-sppd", font=self.main_font)
        self.CTkCheckBox_sppd.grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox_sppd.grid_anchor = "center"
        self.CTkCheckBox_sppd.configure(state="disabled")


        self.para_frame3 = ctk.CTkFrame(self.setting_frame, height=120, corner_radius=0)
        self.para_frame3.grid(
            row=0, column=2, padx=2, pady=2, sticky="nsew"
        )
        self.para_frame3.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.CTkCheckBox_pt = ctk.CTkCheckBox(self.para_frame3, text="-pt", font=self.main_font)
        self.CTkCheckBox_pt.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox_pt.grid_anchor = "center"
        self.CTkCheckBox_pt.configure(state="disabled")

        self.CTkCheckBox_tf = ctk.CTkCheckBox(self.para_frame3, text="-tf", font=self.main_font)
        self.CTkCheckBox_tf.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox_tf.grid_anchor = "center"
        self.CTkCheckBox_tf.configure(state="disabled")

        self.CTkCheckBox_lps1 = ctk.CTkCheckBox(self.para_frame3, text="-lps1", font=self.main_font)
        self.CTkCheckBox_lps1.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox_lps1.grid_anchor = "center"
        self.CTkCheckBox_lps1.configure(state="disabled")

        self.CTkCheckBox_v = ctk.CTkCheckBox(self.para_frame3, text="-v", font=self.main_font)
        self.CTkCheckBox_v.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkCheckBox_v.grid_anchor = "center"
        self.CTkCheckBox_v.configure(state="disabled")

        self.para_frame4 = ctk.CTkFrame(self.setting_frame, height=120, corner_radius=0)
        self.para_frame4.grid(
            row=0, column=3, padx=2, pady=2, sticky="nsew"
        )
        self.para_frame4.grid_columnconfigure((0), weight=1)

        self.show_log = ctk.CTkSwitch(self.para_frame4, text="Log Off", command= self.show_log_change,
                                        font=self.main_font,
        )
        self.show_log.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.show_log.grid_anchor = "center"

        self.process_frame = ctk.CTkFrame(
            self.setting_frame, height=120, corner_radius=0
        )
        self.process_frame.grid(row=0, column=4, padx=2, pady=2)
        self.process_frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.start_button = ctk.CTkButton(
            self.process_frame,
            font=self.main_font,
            text="Start",
            anchor="center",
            corner_radius=4,
            command=self.start_button_click,
        )
        self.start_button.configure(state="disabled")
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
        self.reset_button.configure(state="disabled")

        self.activate_progress_bar = ctk.CTkProgressBar(
            self.process_frame, orientation="horizontal", mode="indeterminate", progress_color="whitesmoke"
        )
        self.activate_progress_bar.grid(row=2, column=0, padx=2, pady=30, sticky="nsew")

        self.is_process_starting = False

    def create_status_common(self):
        self.status_frame = ctk.CTkFrame(self, height=106, corner_radius=0)
        self.status_frame.grid(row=3, column=0, padx=2, pady=2, sticky="ew")
        self.status_frame.grid_columnconfigure((0), weight=1)
        self.status_frame.grid_rowconfigure((0, 1), weight=1)

        self.status_process_bar = ctk.CTkProgressBar(
            self.status_frame, orientation="horizontal", mode="determinate", progress_color="whitesmoke"
        )
        self.status_process_bar.set(0.0)
        self.status_process_bar.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

        self.status_label = ctk.CTkLabel(
            self.status_frame, text="No process is running.", fg_color="transparent", font=self.main_font
        )
        self.status_label.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")

    # def create_status_detail(self):
    #     # create status frame with widgets
    #     self.status_frame = ctk.CTkFrame(self, height=106, corner_radius=0)
    #     self.status_frame.grid(row=2, column=0, padx=2, pady=2, sticky="ew")
    #     self.status_frame.grid_columnconfigure(
    #         (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1
    #     )

    #     r_circle = 32
    #     x_base = 48
    #     height_base = 106
    #     connection_line_distance = 110

    #     self.canvas = ctk.CTkCanvas(
    #         self.status_frame,
    #         width=r_circle,
    #         height=height_base,
    #         highlightthickness=0,
    #         bg="#2b2b2b",
    #     )
    #     self.canvas.grid(row=0, column=0, columnspan=11, sticky="nsew")

    #     color_text_in_circle = "black"
    #     color_circle = "dimgray"
    #     color_connection_line = "dimgray"
    #     color_text_on_line = "dimgray"

    #     self.circle1 = CircleToCircle(
    #         self.canvas, x=x_base, y=height_base / 2, r=r_circle, color=color_circle
    #     )
    #     self.circle2 = CircleToCircle(
    #         self.canvas,
    #         x=x_base + r_circle * 2 + connection_line_distance,
    #         y=height_base / 2,
    #         r=r_circle,
    #         color=color_circle,
    #     )
    #     self.circle1.add_text("1", font=self.main_font, text_color=color_text_in_circle)
    #     self.circle2.add_text("2", font=self.main_font, text_color=color_text_in_circle)

    #     self.circle1.draw_line_to(
    #         self.circle2,
    #         color=color_connection_line,
    #         width=8,
    #         label="Checking ...",
    #         label_color=color_text_on_line,
    #     )

    #     self.circle3 = CircleToCircle(
    #         self.canvas,
    #         x=x_base + r_circle * 4 + connection_line_distance * 2,
    #         y=height_base / 2,
    #         r=r_circle,
    #         color=color_circle,
    #     )
    #     self.circle4 = CircleToCircle(
    #         self.canvas,
    #         x=x_base + r_circle * 6 + connection_line_distance * 3,
    #         y=height_base / 2,
    #         r=r_circle,
    #         color=color_circle,
    #     )
    #     self.circle3.add_text("3", font=self.main_font, text_color=color_text_in_circle)
    #     self.circle4.add_text("4", font=self.main_font, text_color=color_text_in_circle)

    #     self.circle2.draw_line_to(
    #         self.circle3,
    #         color=color_connection_line,
    #         width=8,
    #         label="Scanning ...",
    #         label_color=color_text_on_line,
    #     )
    #     self.circle3.draw_line_to(
    #         self.circle4,
    #         color=color_connection_line,
    #         width=8,
    #         label="Combining ...",
    #         label_color=color_text_on_line,
    #     )

    #     self.circle5 = CircleToCircle(
    #         self.canvas,
    #         x=x_base + r_circle * 8 + connection_line_distance * 4,
    #         y=height_base / 2,
    #         r=r_circle,
    #         color=color_circle,
    #     )
    #     self.circle6 = CircleToCircle(
    #         self.canvas,
    #         x=x_base + r_circle * 10 + connection_line_distance * 5,
    #         y=height_base / 2,
    #         r=r_circle,
    #         color=color_circle,
    #     )
    #     self.circle5.add_text("5", font=self.main_font, text_color=color_text_in_circle)
    #     self.circle6.add_text("6", font=self.main_font, text_color=color_text_in_circle)

    #     self.circle4.draw_line_to(
    #         self.circle5,
    #         color=color_connection_line,
    #         width=8,
    #         label="Training ...",
    #         label_color=color_text_on_line,
    #     )
    #     self.circle5.draw_line_to(
    #         self.circle6,
    #         color=color_connection_line,
    #         width=8,
    #         label="Evaluating ...",
    #         label_color=color_text_on_line,
    #     )

    def set_group_control(self, state_control : str, except_reset_button : bool = False, 
                          except_start_button : bool = False):
        self.train_path_button.configure(state=state_control)
        self.result_path_button.configure(state=state_control)
        self.predict_path_button.configure(state=state_control)

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
        print_with_timestep(f"Start button is clicked by the user, current state {self.is_process_starting}")
        self.toggle_start_button()

        commo_state = "disabled" if self.is_process_starting else "normal"

        self.set_group_control(commo_state, except_start_button = True)  

        if not self.thread_phase1 and self.is_process_starting:
            self.stop_event.clear()
            # self.thread_phase1 = Thread(target=self.phase1_calling_detail, daemon=True)
            self.thread_phase1 = Thread(target=self.phase1_calling_common, daemon=True)
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

    def error_critical_handle(self):
        self.is_process_starting = False
        self.start_button.configure(text= "Start", state="disabled")
        self.activate_progress_bar.stop()
        self.activate_progress_bar.configure(progress_color="red", fg_color="red")
        self.status_process_bar.set(1.0)
        self.status_process_bar.configure(progress_color="red", fg_color="red")
        self.status_label.configure(text= "Process is running 100%")

    def stream_output(self, stream, callback):
        """Reads output from a stream line-by-line and passes each line to a callback."""
        while True:
            time.sleep(0.01)
            line = stream.readline()
            if not line:  # End of stream
                break
            callback(line.strip())

    def handle_output(self, output_line):
        if output_line:
            self.after(100, self.log_screen.add_log, output_line)  # Update the log screen
            self.current_percent_process = self.update_process_status(output_line, self.current_percent_process)  # Update progress

    def phase1_calling_common(self):
        self.activate_progress_bar.configure(progress_color="aqua")
        self.activate_progress_bar.start()

        self.status_process_bar.configure(progress_color="chartreuse")
        self.status_process_bar.set(0.0)
        self.status_label.configure(text= "Process is running 0%")

        self.is_process_done = False
        ws = os.environ['ROOT_WS_DUY']
        self.current_percent_process = 0
        if not ws:
            self.notify_screen.show_window(text_body="Contact admin, has critical error.", type_notify= TypeNotify.ERROR)
            self.error_critical_handle()
            return
        exe_file_path = os.path.join(ws, "ThesisMaster/scripts/run_script.sh")
        if not os.path.isfile(exe_file_path):
            self.notify_screen.show_window(text_body="Contact admin, has critical error.", type_notify= TypeNotify.ERROR)
            self.error_critical_handle()
            return
        
        if not self.train_path.get() or not self.result_path.get():
            self.notify_screen.show_window(text_body="The path of train and result must not empty", type_notify= TypeNotify.WARNING)
        else: 
            command = f"""stdbuf -oL bash {exe_file_path} -i {self.train_path.get()} -o {self.result_path.get()}"""

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd= ws,
                bufsize=1
            )

            proc = psutil.Process(process.pid)

            stop_event = Event()


            stdout_thread = Thread(target=self.stream_output, args=(stop_event, process.stdout, self.handle_output))
            stderr_thread = Thread(target=self.stream_output, args=(stop_event, process.stderr, self.handle_output))
            stdout_thread.start()
            stderr_thread.start()


            try:
                while True:
                    print_with_timestep(f"Process is running ...")

                    if self.stop_event.is_set():
                        stop_event.set()    
                        stdout_thread.join(timeout=2)
                        stderr_thread.join(timeout=2)
                        print_with_timestep(f"Process is stopping ...")
                        for child in proc.children(recursive=True):
                            child.kill()
                        proc.kill()
                        process.terminate()
                        process.wait(timeout=2)

                        break
                    if process.poll() is not None:
                        break
                    if process.poll() is None:  # If the process is still running
                        process.kill()  # Force kill the process

                # for remaining in process.stdout:
                #     self.after(100, self.log_screen.add_log, f"{remaining.strip()}")
                #     self.current_percent_process = self.update_process_status(remaining.strip(), self.current_percent_process)


                # for remaining in process.stderr:
                #     self.after(100, self.log_screen.add_log, f"{remaining.strip()}")
                #     self.current_percent_process = self.update_process_status(remaining.strip(), self.current_percent_process)

                time.sleep(0.01)
            except subprocess.TimeoutExpired:
                print_with_timestep(f"Process stop with timeout")
                process.stdout.close()
                process.stderr.close()
                stdout_thread.join()
                stderr_thread.join()
                process.kill()  
                process.wait()

            self.is_process_done = True if self.current_percent_process == 100 else False
        
        print_with_timestep(f"Process stop with {self.current_percent_process}%")
        self.activate_progress_bar.stop()
        self.thread_phase1 = None
        if self.is_process_done:
            self.after(0, lambda : self.status_process_bar.set(1.0))    
            self.after(0, lambda : self.status_label.configure(text= f"Process is running {100}%"))

            self.notify_screen = None
            self.notify_screen = notify_screen.NotifyScreen(self)
            self.notify_screen.show_window(text_body="The process done", type_notify= TypeNotify.INFOR)
            self.activate_progress_bar.configure(progress_color="whitesmoke")

        else: 
            self.notify_screen = None
            self.notify_screen = notify_screen.NotifyScreen(self)
            self.notify_screen.show_window(text_body="The process stops unexpectedly", type_notify= TypeNotify.WARNING)
            self.activate_progress_bar.configure(progress_color= "yellow", fg_color="yellow")
            self.status_process_bar.configure(progress_color= "yellow", fg_color="yellow")

        self.toggle_start_button()
        self.start_button.configure(state = "disabled")
        self.reset_button.configure(state = "normal")
        
    def update_process_status(self, log: str, current_percent_process: int) -> int:
            new_percent_process = extract_value_from_log(log)
            if new_percent_process == -1:
                new_percent_process = current_percent_process

            self.after(0, lambda : self.status_process_bar.set(new_percent_process / 100))    
            self.after(0, lambda : self.status_label.configure(text= f"Process is running {new_percent_process}%"))

            return new_percent_process

    # def phase1_calling_detail(self):
    #     self.activate_progress_bar.configure(progress_color="aqua")

    #     circles = [
    #         self.circle1,
    #         self.circle2,
    #         self.circle3,
    #         self.circle4,
    #         self.circle5,
    #         self.circle6,
    #     ]
    #     """Simulate a long-running task."""
    #     for index, circle in enumerate(circles):
    #         if self.stop_event.is_set():
    #             break

    #         circle.set_color_circle("orange")
    #         circle.set_color_line("orange")
    #         circle.set_color_text_line("orange")

    #         time.sleep(2)  # Simulate the task

    #         circle.set_color_text_line("green")
    #         circle.set_color_circle("green")
    #         circle.set_color_line("green")


    #         self.after(0, self.log_screen.add_log, "Example \n")

    #     self.activate_progress_bar.stop()
    #     self.activate_progress_bar.configure(progress_color="whitesmoke")
    #     self.thread_phase1 = None
    #     self.notify_screen.show_window(text_body="This is example notify", type_notify= TypeNotify.ERROR)
    #     self.reset_button.configure(state = "normal")
    #     self.start_button.configure(state = "disabled")
    #     self.toggle_start_button()

    def show_log_change(self):
        print_with_timestep(f"The log screen button is clicked by the user")
        self.show_log.configure(text= "Log On" if self.show_log.get() else "Log Off", 
                                text_color = "aqua" if self.show_log.get() else "white")
        self.log_screen.show_window() if self.show_log.get() else self.log_screen.hide_window()

    def reset_status(self):
        # circles = [
        #     self.circle1,
        #     self.circle2,
        #     self.circle3,
        #     self.circle4,
        #     self.circle5,
        #     self.circle6,
        # ]
        # for circle in circles: 
        #     circle.set_color_circle("dimgray")
        #     circle.set_color_line("dimgray")
        #     circle.set_color_text_line("dimgray")

        self.status_process_bar.configure(progress_color = "whitesmoke", fg_color=ctk.ThemeManager.theme["CTkProgressBar"]["fg_color"])
        self.activate_progress_bar.configure(progress_color= "whitesmoke", fg_color=ctk.ThemeManager.theme["CTkProgressBar"]["fg_color"])
        self.status_process_bar.configure(progress_color= "whitesmoke", fg_color=ctk.ThemeManager.theme["CTkProgressBar"]["fg_color"])

        self.status_process_bar.set(0.0)

        self.status_label.configure(text= "No process is running.")

    def reset_app(self):
        print_with_timestep(f"Reset button is clicked by the user, current state {self.is_process_starting}")

        self.reset_status()
        self.set_group_control("normal")  

        self.train_path.configure(state="normal")
        self.train_path.delete(0, "end")
        self.train_path.configure(placeholder_text="Path to your training data")
        self.train_path.focus()
        self.train_path.configure(state="readonly")

        self.result_path.configure(state="normal")
        self.result_path.delete(0, "end")
        self.result_path.configure(placeholder_text="Path to save your results")
        self.result_path.focus()
        self.result_path.configure(state="readonly")

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

        self.log_screen.clear_log()
        self.log_screen.hide_window()

    def on_mode_change(self, mode) ->None:
        init_mode = "disabled"
        self.train_path_button.configure(state=init_mode)
        self.result_path_button.configure(state=init_mode)
        self.predict_path_button.configure(state=init_mode)
        self.model_path_button.configure(state=init_mode)
        self.json_path_button.configure(state=init_mode)
        self.start_button.configure(state=init_mode)
        self.reset_button.configure(state=init_mode)

        self.CTkLabel_noh.configure(text_color=DISABLED_COLOR)
        self.CTkEntry_noh.configure(state=init_mode)
        self.CTkLabel_mld.configure(text_color=DISABLED_COLOR)
        self.CTkEntry_mld.configure(state=init_mode)
        self.CTkLabel_e.configure(text_color=DISABLED_COLOR)
        self.CTkEntry_e.configure(state=init_mode)

        self.CTkCheckBox_pred_only.configure(state=init_mode)
        self.CTkCheckBox_omd.configure(state=init_mode)
        self.CTkCheckBox_sppd.configure(state=init_mode)
        
        self.CTkCheckBox_pt.configure(state=init_mode) 
        self.CTkCheckBox_tf.configure(state=init_mode)
        self.CTkCheckBox_lps1.configure(state=init_mode)
        self.CTkCheckBox_v.configure(state=init_mode)
            
        if mode == "Train mode":
            train_mode = "normal"
            self.train_path_button.configure(state=train_mode)
            self.result_path_button.configure(state=train_mode)
            self.predict_path_button.configure(state=train_mode)
            self.json_path_button.configure(state=train_mode)
            
            self.CTkLabel_noh.configure(text_color=ENABLED_COLOR)
            self.CTkEntry_noh.configure(state=train_mode)
            self.CTkLabel_mld.configure(text_color=ENABLED_COLOR)
            self.CTkEntry_mld.configure(state=train_mode)
            self.CTkLabel_e.configure(text_color=ENABLED_COLOR)
            self.CTkEntry_e.configure(state=train_mode)

            self.CTkCheckBox_pt.configure(state=train_mode) 
            self.CTkCheckBox_tf.configure(state=train_mode)
            self.CTkCheckBox_lps1.configure(state=train_mode)
            self.CTkCheckBox_v.configure(state=train_mode)
            
            self.start_button.configure(state=train_mode)
            self.reset_button.configure(state=train_mode)

            
        elif mode == "Create mode":
            create_mode = "disabled"
            self.model_path_button.configure(state=create_mode)
            self.CTkEntry_e.configure(state=create_mode)
            self.CTkCheckBox_pred_only.configure(state=create_mode)
            self.CTkCheckBox_omd.configure(state=create_mode)
            self.CTkCheckBox_sppd.configure(state=create_mode)
            self.CTkCheckBox_pt.configure(state=create_mode) 
            self.CTkCheckBox_tf.configure(state=create_mode)