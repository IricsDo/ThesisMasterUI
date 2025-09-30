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
import re
# from MainScreen.components import CircleToCircle
# from utils.exec_command import execute_command
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

    def browse_file(self, identifier):
        widget_map = {
            "model": (self.model_path, [("Model", "*.pth *.pb"), ("All", "*.*")]),
            "json": (self.json_path, [("JSON", "*.json"), ("All", "*.*")])
        }

        if identifier not in widget_map:
            print_with_timestep("The identifier not valid")
            return

        widget, filetypes = widget_map[identifier]
        file_path = filedialog.askopenfilename(
            title=f"Select {identifier} file",
            filetypes=filetypes
        )

        if file_path:
            widget.configure(state="normal")
            widget.delete(0, "end")
            widget.insert(0, file_path)
            widget.configure(state="readonly")
        else:
            print("Path must be not None")

                
    def browse_folder(self, identifier):
        widget_map = {
            "train": self.train_path,
            "result": self.result_path,
            "predict": self.predict_path,
        }

        directory_path = filedialog.askdirectory(title="Select a Directory")
        if not directory_path:
            print("Directory must be not None")
            return

        print_with_timestep(f"Button {identifier} is clicked by the user")
        print_with_timestep(f"Path {directory_path} selected by the user")

        widget = widget_map.get(identifier)
        if widget:
            widget.configure(state="normal")
            widget.delete(0, "end")
            widget.insert(0, directory_path)
            widget.configure(state="readonly")
        else:
            print_with_timestep("The identifier not valid")

        
    def create_mode(self):
        self.mode_frame = ctk.CTkFrame(self, height=32, corner_radius=0)
        self.mode_frame.grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        self.mode_frame.grid_columnconfigure((0, 1), weight=1)
        self.mode_frame.grid_rowconfigure((0), weight=1)

        self.current_mode_var = tk.StringVar(value="")
        self.mode_label = ctk.CTkLabel(self.mode_frame, text="Mode:", font=self.main_font)
        self.mode_label.grid(row=0, column=0, sticky="se", padx=4, pady=4)

        self.mode_combobox = ctk.CTkComboBox(
            self.mode_frame, values=["Init mode", "Train mode", "Create mode", "Predict mode"],
            variable=self.current_mode_var, command=self.on_mode_change, font=self.main_font
        )
        self.mode_combobox.grid(row=0, column=1, sticky="se", padx=4, pady=4)
        self.mode_combobox.set("Init mode")
        
        
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
            command=lambda: self.browse_folder("train"),
        )
        self.train_path_button.grid(row=0, column=5, padx=2, pady=2, sticky="nsew")
        self.train_path_button.configure(state="disabled")

        self.result_path_button = ctk.CTkButton(
            self.config_path_frame,
            font=self.main_font,
            corner_radius=4,
            text="Result path",
            command=lambda: self.browse_folder("result"),
        )
        self.result_path_button.grid(row=1, column=5, padx=2, pady=2, sticky="nsew")
        self.result_path_button.configure(state="disabled")

        self.predict_path_button = ctk.CTkButton(
            self.config_path_frame,
            font=self.main_font,
            corner_radius=4,
            text="Predict path",
            command=lambda: self.browse_folder("predict"),
        )
        self.predict_path_button.grid(row=2, column=5, padx=2, pady=2, sticky="nsew")
        self.predict_path_button.configure(state="disabled")

        self.json_path_button = ctk.CTkButton(
            self.config_path_frame,
            font=self.main_font,
            corner_radius=4,
            text="Json path",
            command=lambda: self.browse_file("json"),
        )
        self.json_path_button.grid(row=3, column=5, padx=2, pady=2, sticky="nsew")
        self.json_path_button.configure(state="disabled")

        self.model_path_button = ctk.CTkButton(
            self.config_path_frame,
            font=self.main_font,
            corner_radius=4,
            text="Model path",
            command=lambda: self.browse_file("model"),
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
        self.CTkEntry_noh = ctk.CTkEntry(self.para_frame1, placeholder_text="Required, example: 4,10,29", font=("Arial", 10, "bold"))
        self.CTkEntry_noh.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_noh.configure(state="disable")

        self.CTkLabel_mld = ctk.CTkLabel(
            self.para_frame1, text="-mld", text_color=DISABLED_COLOR, fg_color="transparent", font=self.main_font
        )
        self.CTkLabel_mld.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_mld = ctk.CTkEntry(self.para_frame1, placeholder_text="Optional, default: 0", font=("Arial", 10, "bold"))
        self.CTkEntry_mld.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_mld.configure(state="disable")
        

        self.CTkLabel_e = ctk.CTkLabel(
            self.para_frame1, text="-e", text_color=DISABLED_COLOR, fg_color="transparent", font=self.main_font
        )
        self.CTkLabel_e.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.CTkEntry_e = ctk.CTkEntry(self.para_frame1, placeholder_text="Optional, default: 10000", font=("Arial", 10, "bold"))
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

        self.current_backend_var = ctk.StringVar(value="auto")  # default to auto
        self.backend_combobox = ctk.CTkComboBox(self.para_frame3, 
                values=["auto", "tensorflow", "pytorch"], 
                variable=self.current_backend_var, font=self.main_font)
        self.backend_combobox.set("auto")

        self.backend_combobox.grid(row=0, rowspan= 1, column=0, padx=2, pady=2, sticky="nsew")
        self.backend_combobox.grid_anchor = "center"
        self.backend_combobox.configure(state="disabled")

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
        self.process_frame.grid_rowconfigure((0, 1, 2), weight=0)

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
        
        self.reset_text = tk.StringVar()
        self.reset_text.set(f"Reset: {self.current_mode_var.get()}")
        self.reset_button = ctk.CTkButton(
            self.process_frame,
            font=self.main_font,
            textvariable=self.reset_text,
            anchor="center",
            corner_radius=4,
            command=self.reset_mode,
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
    
        if self.current_mode_var.get() == "Train mode":
            self.train_path_button.configure(state=state_control)
            self.result_path_button.configure(state=state_control)
            self.predict_path_button.configure(state=state_control)
            self.json_path_button.configure(state=state_control)
        
            self.CTkEntry_noh.configure(state=state_control)
            self.CTkEntry_mld.configure(state=state_control)
            self.CTkEntry_e.configure(state=state_control)
                                    
            self.backend_combobox.configure(state=state_control) 
            self.CTkCheckBox_lps1.configure(state=state_control)
            self.CTkCheckBox_v.configure(state=state_control)
                
        elif self.current_mode_var.get() == "Create mode":
            self.train_path_button.configure(state=state_control)
            self.result_path_button.configure(state=state_control)

            self.CTkEntry_noh.configure(state=state_control)
            self.CTkEntry_mld.configure(state=state_control)

            self.CTkCheckBox_omd.configure(state=state_control)
            self.CTkCheckBox_lps1.configure(state=state_control)
            self.CTkCheckBox_v.configure(state=state_control)
            
        elif self.current_mode_var.get() == "Predict mode":
            self.predict_path_button.configure(state=state_control)
            self.model_path_button.configure(state=state_control)

            self.CTkCheckBox_pred_only.configure(state=state_control)
            self.CTkCheckBox_sppd.configure(state=state_control)

            self.backend_combobox.configure(state=state_control) 
            self.CTkCheckBox_v.configure(state=state_control)

        self.show_log.configure(state=state_control)

        if not except_reset_button:
            self.reset_button.configure(state=state_control)

        if not except_start_button:
            self.start_button.configure(state=state_control)
        
        self.focus()
 
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
        self.phase1_calling_common()
        
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

    def build_command_for_runner(self):
        """
        Build args for scripts/run_script.sh (without 'bash scripts/run_script.sh').
        Mode:
        - with -pred_only   => predict mode
        - with -omd         => create/make-data mode
        - otherwise         => train mode

        Validation rules:
        - Required strings per mode must be non-empty.
        - number_of_h must match r"\d+(,\d+)*" (e.g., "4,10,19") and becomes "-noh 4 10 19".
        - min_len_data, epochs_str (if provided) must be non-negative integers (>= 0).
        """

        # -------- Read UI values (direct/gọn) --------
        train_dir    = self.train_path.get().strip()
        result_dir   = self.result_path.get().strip()
        predict_dir  = self.predict_path.get().strip()
        model_path   = self.model_path.get().strip()
        train_json   = self.json_path.get().strip()
        number_of_h  = self.CTkEntry_noh.get().strip()
        min_len_data = self.CTkEntry_mld.get().strip()
        epochs_str   = self.CTkEntry_e.get().strip()

        predict_only_flag    = self.CTkCheckBox_pred_only.get()
        only_make_data_flag  = self.CTkCheckBox_omd.get()
        skip_prepare_flag    = self.CTkCheckBox_sppd.get()
        load_status_phase_1  = self.CTkCheckBox_lps1.get()
        verbose_flag         = self.CTkCheckBox_v.get()
        backend_choice       = self.current_backend_var.get().strip().lower()  # "auto"|"pytorch"|"tensorflow"

        # -------- Small validators --------
        def warn(msg):
            self.notify_screen.show_window(text_body=msg, type_notify=TypeNotify.WARNING)

        def is_nonneg_int(s: str) -> bool:
            return s.isdigit() and int(s) >= 0

        def validate_noh_format(noh: str) -> bool:
            # strict "4,10,19" etc. (no spaces, only commas and digits)
            import re
            return bool(re.fullmatch(r"\d+(,\d+)*", noh))

        # -------- Builder helpers --------
        def add_noh_args(cmd, noh_str):
            # noh_str must already be validated to r"\d+(,\d+)*"
            parts = noh_str.split(",")
            cmd += ["-noh"] + parts
            return cmd

        def add_common_flags(cmd):
            # Optional integers >= 0
            if min_len_data:
                if not is_nonneg_int(min_len_data):
                    warn("`min_len_data` must be a non-negative integer (e.g., 0,1,2,...)")
                    return None
                cmd += ["-mld", min_len_data]
            if load_status_phase_1:
                cmd.append("-lps1")
            if verbose_flag:
                cmd.append("-v")
            return cmd

        def add_backend_train_required(cmd):
            # Train requires pytorch|tensorflow (not auto)
            if backend_choice == "pytorch":
                cmd.append("-pt")
            elif backend_choice == "tensorflow":
                cmd.append("-tf")
            else:
                warn("Training requires backend: choose PyTorch or TensorFlow (Auto is not allowed).")
                return None
            return cmd

        def add_backend_predict_optional(cmd):
            # Predict accepts auto/pytorch/tensorflow; auto => no flag
            if backend_choice == "pytorch":
                cmd.append("-pt")
            elif backend_choice == "tensorflow":
                cmd.append("-tf")
            return cmd

        # -------- Determine mode by flags --------
        if predict_only_flag:
            # =========== PREDICT MODE ===========
            # Required strings
            if not model_path:
                warn("Predict mode requires `Model path`.")
                return None
            if not predict_dir:
                warn("Predict mode requires `Predict folder`.")
                return None

            cmd = ["-pred_only", "-mp", model_path, "-p", predict_dir]
            # Backend optional
            cmd = add_backend_predict_optional(cmd)
            # Optional flags
            if skip_prepare_flag:
                cmd.append("--skip_prepare_predict_data")
            if verbose_flag:
                cmd.append("-v")
            return cmd

        elif only_make_data_flag:
            # =========== CREATE / MAKE-DATA MODE ===========
            # Required strings
            if not train_dir:
                warn("Create mode requires `Train folder`.")
                return None
            if not result_dir:
                warn("Create mode requires `Result folder`.")
                return None
            if not number_of_h:
                warn("Create mode requires `Num of hidro (-noh)` in format like: 4,10,19.")
                return None
            if not validate_noh_format(number_of_h):
                warn(f"Invalid -noh format: '{number_of_h}'. Use comma-separated numbers (e.g. 4,10,19).")
                return None

            cmd = ["-i", train_dir, "-o", result_dir, "-omd"]
            cmd = add_noh_args(cmd, number_of_h)

            # Optional: include training json if you want to pass it along
            if train_json:
                cmd += ["-trainj", train_json]

            cmd = add_common_flags(cmd)
            if cmd is None:
                return None
            return cmd

        else:
            # =========== TRAIN MODE (default) ===========
            # Required strings
            if not train_dir:
                warn("Train mode requires `Train folder`.")
                return None
            if not result_dir:
                warn("Train mode requires `Result folder`.")
                return None
            if not train_json:
                warn("Train mode requires `Training JSON`.")
                return None
            if not number_of_h:
                warn("Train mode requires `Num of hidro (-noh)` in format like: 4,10,19.")
                return None
            if not validate_noh_format(number_of_h):
                warn(f"Invalid -noh format: '{number_of_h}'. Use comma-separated numbers (e.g. 4,10,19).")
                return None

            cmd = ["-i", train_dir, "-o", result_dir, "-trainj", train_json]
            cmd = add_noh_args(cmd, number_of_h)

            # Backend required for training
            cmd = add_backend_train_required(cmd)
            if cmd is None:
                return None

            # Optional epochs >= 0
            if epochs_str:
                if not is_nonneg_int(epochs_str):
                    warn("`epochs` must be a non-negative integer (e.g., 0,1,2,...)")
                    return None
                cmd += ["-e", epochs_str]

            # Optional predict folder during training
            if predict_dir:
                cmd += ["-p", predict_dir]

            cmd = add_common_flags(cmd)
            if cmd is None:
                return None
            return cmd

    def phase1_calling_common(self):
        self.activate_progress_bar.configure(progress_color="aqua")
        self.activate_progress_bar.start()

        self.status_process_bar.configure(progress_color="chartreuse")
        self.status_process_bar.set(0.0)
        self.status_label.configure(text= "Process is running 0%")

        self.is_process_done = False
        
        cmd_args = self.build_command_for_runner()
        if cmd_args is None:
            return 

        ws = os.environ.get("ROOT_WS_DUY", "")
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
            
            command = ["stdbuf", "-oL", "bash", exe_file_path] + cmd_args

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

    def reset_mode(self):
        print_with_timestep(f"Reset button is clicked by the user, current state {self.is_process_starting}")

        self.reset_status()
        if self.current_mode_var.get() == "Train mode":
            self.train_path_button.configure(state="normal")
            self.result_path_button.configure(state="normal")
            self.predict_path_button.configure(state="normal")
            self.json_path_button.configure(state="normal")


            self.train_path.configure(state="normal")
            self.train_path.delete(0, "end")
            self.train_path.configure(placeholder_text="Path to your training data")
            self.train_path.configure(state="readonly")
            
            self.result_path.configure(state="normal")
            self.result_path.delete(0, "end")
            self.result_path.configure(placeholder_text="Path to save your results")
            self.result_path.configure(state="readonly")

            self.predict_path.configure(state="normal")
            self.predict_path.delete(0, "end")
            self.predict_path.configure(placeholder_text="Path to your predict data")
            self.predict_path.configure(state="readonly")
            
            self.model_path.configure(state="normal")
            self.model_path.delete(0, "end")
            self.model_path.configure(placeholder_text="Path to your model deep learning")
            self.model_path.configure(state="readonly")
            
            self.json_path.configure(state="normal")
            self.json_path.delete(0, "end")
            self.json_path.configure(placeholder_text="Path to your JSON config")
            self.json_path.configure(state="readonly")
            
            self.backend_combobox.set("tensorflow")
            self.CTkCheckBox_lps1.deselect()
            
            self.CTkCheckBox_v.deselect()
                
            self.CTkEntry_noh.delete(0, "end")
            self.CTkEntry_noh.configure(placeholder_text="Required, example: 4,10,29")

            self.CTkEntry_mld.delete(0, "end")
            self.CTkEntry_mld.configure(placeholder_text="Optional, default: 0")

            self.CTkEntry_e.delete(0, "end")
            self.CTkEntry_e.configure(placeholder_text="Optional, default: 10000")
                    
                
        elif self.current_mode_var.get() == "Create mode":
            self.train_path_button.configure(state="normal")
            self.result_path_button.configure(state="normal")

            self.train_path.configure(state="normal")
            self.train_path.delete(0, "end")
            self.train_path.configure(placeholder_text="Path to your training data")
            self.train_path.configure(state="readonly")
            
            self.result_path.configure(state="normal")
            self.result_path.delete(0, "end")
            self.result_path.configure(placeholder_text="Path to save your results")
            self.result_path.configure(state="readonly")
            
            self.CTkEntry_noh.delete(0, "end")
            self.CTkEntry_noh.configure(placeholder_text="Required, example: 4,10,29")

            self.CTkEntry_mld.delete(0, "end")
            self.CTkEntry_mld.configure(placeholder_text="Optional, default: 0")
            
            self.CTkCheckBox_omd.deselect()
            
            self.CTkCheckBox_lps1.deselect()
            self.CTkCheckBox_v.deselect()
            
        elif self.current_mode_var.get() == "Predict mode":
            self.predict_path_button.configure(state="normal")
            self.model_path_button.configure(state="normal")
            
            self.predict_path.configure(state="normal")
            self.predict_path.delete(0, "end")
            self.predict_path.configure(placeholder_text="Path to your predict data")
            self.predict_path.configure(state="readonly")

            self.model_path.configure(state="normal")
            self.model_path.delete(0, "end")
            self.model_path.configure(placeholder_text="Path to your model deep learning")
            self.model_path.configure(state="readonly")

            self.CTkCheckBox_pred_only.deselect()
            self.CTkCheckBox_sppd.deselect()

            self.backend_combobox.set("tensorflow")
            self.CTkCheckBox_v.deselect()
        
        self.show_log.deselect()

        self.log_screen.clear_log()
        self.log_screen.hide_window()

        self.focus()

    def update_reset_text(self, *args):
        self.reset_text.set(f"Reset: {self.current_mode_var.get()}")

    def on_mode_change(self, mode) ->None:
        self.reset_text.set(f"Reset: {self.current_mode_var.get()}")
        
        init_mode = "disabled"
        self.train_path_button.configure(state=init_mode)
        self.train_path.configure(state="normal")
        self.train_path.delete(0, "end")
        self.train_path.configure(placeholder_text="Path to your training data")
        self.train_path.configure(state="readonly")
        
        self.result_path_button.configure(state=init_mode)
        self.result_path.configure(state="normal")
        self.result_path.delete(0, "end")
        self.result_path.configure(placeholder_text="Path to save your results")
        self.result_path.configure(state="readonly")

        self.predict_path_button.configure(state=init_mode)
        self.predict_path.configure(state="normal")
        self.predict_path.delete(0, "end")
        self.predict_path.configure(placeholder_text="Path to your predict data")
        self.predict_path.configure(state="readonly")
        
        self.model_path_button.configure(state=init_mode)
        self.model_path.configure(state="normal")
        self.model_path.delete(0, "end")
        self.model_path.configure(placeholder_text="Path to your model deep learning")
        self.model_path.configure(state="readonly")
        
        self.json_path_button.configure(state=init_mode)
        self.json_path.configure(state="normal")
        self.json_path.delete(0, "end")
        self.json_path.configure(placeholder_text="Path to your JSON config")
        self.json_path.configure(state="readonly")
        
        self.start_button.configure(state=init_mode)
        self.reset_button.configure(state=init_mode)

        self.CTkLabel_noh.configure(text_color=DISABLED_COLOR)
        self.CTkEntry_noh.delete(0, "end")
        self.CTkEntry_noh.configure(state=init_mode,placeholder_text="Required, example: 4,10,29")
        
        self.CTkLabel_mld.configure(text_color=DISABLED_COLOR)
        self.CTkEntry_mld.delete(0, "end")
        self.CTkEntry_mld.configure(state=init_mode,placeholder_text="Optional, default: 0")

        self.CTkLabel_e.configure(text_color=DISABLED_COLOR)
        self.CTkEntry_e.delete(0, "end")
        self.CTkEntry_e.configure(state=init_mode, placeholder_text="Optional, default: 10000")

        self.CTkCheckBox_pred_only.deselect()
        self.CTkCheckBox_omd.deselect()
        self.CTkCheckBox_sppd.deselect()
        
        self.backend_combobox.configure(values=["auto", "tensorflow", "pytorch"])
        self.backend_combobox.set("auto")
        self.CTkCheckBox_lps1.deselect()
        self.CTkCheckBox_v.deselect()
        
        self.CTkCheckBox_pred_only.configure(state=init_mode)
        self.CTkCheckBox_omd.configure(state=init_mode)
        self.CTkCheckBox_sppd.configure(state=init_mode)
        
        self.backend_combobox.configure(state=init_mode) 
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

            allowed = ["tensorflow", "pytorch"]
            self.backend_combobox.configure(values=allowed, state=train_mode)
            if self.current_backend_var.get() == "auto":
                self.backend_combobox.set("tensorflow")  # default if auto selected 
            self.CTkCheckBox_lps1.configure(state=train_mode)
            self.CTkCheckBox_v.configure(state=train_mode)
            
            self.start_button.configure(state=train_mode)
            self.reset_button.configure(state=train_mode)

            
        elif mode == "Create mode":
            create_mode = "normal"
            self.train_path_button.configure(state=create_mode)
            self.result_path_button.configure(state=create_mode)

            self.CTkLabel_noh.configure(text_color=ENABLED_COLOR)
            self.CTkEntry_noh.configure(state=create_mode)
            self.CTkLabel_mld.configure(text_color=ENABLED_COLOR)
            self.CTkEntry_mld.configure(state=create_mode)
            
            self.CTkCheckBox_omd.configure(state=create_mode)
            
            self.CTkCheckBox_lps1.configure(state=create_mode)
            self.CTkCheckBox_v.configure(state=create_mode)

            self.start_button.configure(state=create_mode)
            self.reset_button.configure(state=create_mode)
        
        elif mode == "Predict mode":
            predict_mode = "normal"
            
            self.predict_path_button.configure(state=predict_mode)
            self.model_path_button.configure(state=predict_mode)

            self.CTkCheckBox_pred_only.configure(state=predict_mode)
            self.CTkCheckBox_sppd.configure(state=predict_mode)

            self.backend_combobox.configure(state=predict_mode) 
            self.backend_combobox.set("auto")

            self.CTkCheckBox_v.configure(state=predict_mode)
            
            self.start_button.configure(state=predict_mode)
            self.reset_button.configure(state=predict_mode)
        
        self.focus()