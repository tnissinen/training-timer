import customtkinter as ctk

class TimerView:
    def __init__(self, master):
        """
        Initializes the TimerView with the given master window.

        Args:
            master (tk.Tk): The main window of the application.
        """
        self.master = master
        self.master.title("Exercise Timer")
        self.master.state('zoomed')

        self.timer_font = ctk.CTkFont(size=80, weight='bold')
        self.big_font = ctk.CTkFont(size=66)
        self.medium_font = ctk.CTkFont(size=36)
        self.semismall_font = ctk.CTkFont(size=26)
        self.small_font = ctk.CTkFont(size=12)

        self.basic_button_width = 120

        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges the widgets in the main window.
        """
        # Frame for total time label
        self.total_time_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.total_time_frame.pack(side=ctk.TOP, fill=ctk.X, pady=10)
        self.total_time_label = ctk.CTkLabel(self.total_time_frame, text="Total Time: 00:00/00:00",
                                             font=self.medium_font)
        self.total_time_label.pack()

        # Frame for fullscreen and save/load buttons
        self.fullscreen_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.fullscreen_frame.pack(side=ctk.TOP, anchor=ctk.NE, padx=10, pady=0)
        self.fullscreen_button = ctk.CTkButton(self.fullscreen_frame, text="⛶", font=("Arial", 14), width=50)
        self.fullscreen_button.pack(side=ctk.TOP, pady=5)

        self.save_button = ctk.CTkButton(self.fullscreen_frame, text="💾", font=("Arial", 14), width=50)
        self.save_button.pack(side=ctk.TOP, pady=(30, 5))

        self.load_button = ctk.CTkButton(self.fullscreen_frame, text="📂", font=("Arial", 14), width=50)
        self.load_button.pack(side=ctk.TOP, pady=5)

        self.current_phase_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.current_phase_frame.pack(expand=True, pady=0)

        self.status_label = ctk.CTkLabel(self.current_phase_frame, text="", font=self.big_font)
        self.status_label.pack()

        self.timer_label = ctk.CTkLabel(self.current_phase_frame, text="00:00", font=self.timer_font)
        self.timer_label.pack()

        self.current_phase_total_time_label = ctk.CTkLabel(self.current_phase_frame, text="/00:00",
                                                           font=self.medium_font)
        self.current_phase_total_time_label.pack()

        self.phase_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.phase_frame.pack(pady=20)

        self.num_phases_label = ctk.CTkLabel(self.phase_frame, text="Number of Phases:", font=self.small_font)
        self.num_phases_label.grid(row=0, column=0, padx=10, pady=5)
        self.num_phases_entry = ctk.CTkEntry(self.phase_frame, font=self.small_font, justify='center', width=50)
        self.num_phases_entry.grid(row=0, column=1, padx=10, pady=5)

        self.generate_button = ctk.CTkButton(self.phase_frame, text="Generate Phases", font=self.small_font, width=self.basic_button_width, height=30)
        self.generate_button.grid(row=0, column=2, padx=10, pady=5)

        # Scrollable frame for phase inputs
        self.phases_input_frame = ctk.CTkScrollableFrame(self.master, fg_color="transparent", height=300, width=400)
        self.phases_input_frame.pack(pady=10, expand=True)
        self.phases_input_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content

        self.button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.button_frame.pack(side=ctk.BOTTOM, pady=20)

        self.start_pause_button = ctk.CTkButton(self.button_frame, text="Start", font=self.semismall_font, width=self.basic_button_width, height=40)
        self.start_pause_button.pack(side=ctk.LEFT, padx=10)

        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", font=self.semismall_font, width=self.basic_button_width, height=40)
        self.reset_button.pack(side=ctk.LEFT, padx=10)

    def update_timer_display(self, time_str, color="black"):
        """
        Updates the timer display with the given time string and color.

        Args:
            time_str (str): The time string to display.
            color (str): The color of the text.
        """
        self.timer_label.configure(text=time_str, text_color=color)

    def update_timer_color(self, color="black"):
        """
        Updates the timer display with the given time string and color.

        Args:
            time_str (str): The time string to display.
            color (str): The color of the text.
        """
        self.timer_label.configure(text_color=color)

    def update_phase_display(self, phase_name, color="black"):
        """
        Updates the phase display with the given phase name and color.

        Args:
            phase_name (str): The name of the current phase.
            color (str): The color of the text.
        """
        self.status_label.configure(text=phase_name, text_color=color)

    def update_total_time_display(self, elapsed_str, total_str, color="black"):
        """
        Updates the total time display with the given elapsed and total time strings and color.

        Args:
            elapsed_str (str): The elapsed time string.
            total_str (str): The total time string.
            color (str): The color of the text.
        """
        self.total_time_label.configure(text=f"Total Time: {elapsed_str}/{total_str}", text_color=color)

    def update_current_phase_total_time(self, time_str, color="black"):
        """
        Updates the current phase total time display with the given time string and color.

        Args:
            time_str (str): The time string to display.
            color (str): The color of the text.
        """

        self.current_phase_total_time_label.configure(text=f"/{time_str}", text_color=color)

    def update_button_states(self, running, has_phases):
        """
        Updates the states of the control buttons based on the timer's state.

        Args:
            running (bool): Whether the timer is currently running.
            has_phases (bool): Whether there are phases defined.
        """

        start_state = ctk.NORMAL if has_phases and not running else ctk.DISABLED
        pause_state = ctk.NORMAL if has_phases and running else ctk.DISABLED
        reset_state = ctk.NORMAL if has_phases and not running else ctk.DISABLED
        generate_state = ctk.NORMAL if not running else ctk.DISABLED

        start_pause_button_text = "Pause" if running else "Start"
        start_pause_button_state = pause_state if running else start_state

        self.start_pause_button.configure(text=start_pause_button_text, state=start_pause_button_state)
        self.reset_button.configure(state=reset_state)
        self.generate_button.configure(state=generate_state)

    def create_phase_inputs(self, num_phases):
        """
        Creates input fields for the specified number of phases.

        Args:
            num_phases (int): The number of phases to create input fields for.
        """

        for widget in self.phases_input_frame.winfo_children():
            widget.destroy()

        self.phase_inputs = []
        for i in range(num_phases):
            phase_name_label = ctk.CTkLabel(self.phases_input_frame, text=f"{i + 1}", font=self.small_font)
            phase_name_label.grid(row=i, column=0, padx=10, pady=5)

            phase_name_entry = ctk.CTkEntry(self.phases_input_frame, font=self.small_font)
            phase_name_entry.grid(row=i, column=1, padx=10, pady=5)

            phase_time_entry = ctk.CTkEntry(self.phases_input_frame, font=self.small_font, justify='center', width=80)
            phase_time_entry.grid(row=i, column=3, padx=10, pady=5)

            self.phase_inputs.append((phase_name_entry, phase_time_entry))

    def get_phase_inputs(self):
        """
        Retrieves the phase inputs from the input fields.

        Returns:
            list: A list of tuples containing phase names and times.
        """
        return [(name_entry.get(), time_entry.get()) for name_entry, time_entry in self.phase_inputs]

    def set_phase_inputs(self, phases):
        """
        Sets the phase inputs in the input fields.

        Args:
            phases (list): A list of tuples containing phase names and times.
        """
        for i, (name, time) in enumerate(phases):
            if i < len(self.phase_inputs):
                self.phase_inputs[i][0].delete(0, ctk.END)
                self.phase_inputs[i][0].insert(0, name)
                self.phase_inputs[i][1].delete(0, ctk.END)
                self.phase_inputs[i][1].insert(0, time)