import tkinter as tk
from tkinter import font

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

        self.timer_font = font.Font(size=80, weight='bold')
        self.medium_font = font.Font(size=30)
        self.small_font = font.Font(size=11)

        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges the widgets in the main window.
        """
        self.fullscreen_frame = tk.Frame(self.master)
        self.fullscreen_frame.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)
        self.fullscreen_button = tk.Button(self.fullscreen_frame, text="⛶", font=("Arial", 12))
        self.fullscreen_button.pack()

        self.total_time_label = tk.Label(self.master, text="Total Time: 00:00/00:00", font=self.medium_font)
        self.total_time_label.pack(pady=10)

        self.current_phase_frame = tk.Frame(self.master)
        self.current_phase_frame.pack(expand=True)

        self.status_label = tk.Label(self.current_phase_frame, text="Stopped", font=self.medium_font)
        self.status_label.pack()

        self.timer_label = tk.Label(self.current_phase_frame, text="00:00", font=self.timer_font, fg="black")
        self.timer_label.pack()

        self.current_phase_total_time_label = tk.Label(self.current_phase_frame, text="Phase Total Time: 00:00", font=self.medium_font)
        self.current_phase_total_time_label.pack()

        self.phase_frame = tk.Frame(self.master)
        self.phase_frame.pack(pady=20)

        self.num_phases_label = tk.Label(self.phase_frame, text="Number of Phases:", font=self.small_font)
        self.num_phases_label.grid(row=0, column=0, padx=10, pady=5)
        self.num_phases_entry = tk.Entry(self.phase_frame, font=self.small_font, justify='center', width=5)
        self.num_phases_entry.grid(row=0, column=1, padx=10, pady=5)

        self.generate_button = tk.Button(self.phase_frame, text="Generate Phases", font=self.small_font)
        self.generate_button.grid(row=0, column=2, padx=10, pady=5)

        self.phases_input_frame = tk.Frame(self.master)
        self.phases_input_frame.pack(pady=10)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        self.start_pause_button = tk.Button(self.button_frame, text="Start", font=self.medium_font, width=10)
        self.start_pause_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Reset", font=self.medium_font, width=10)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.utility_frame = tk.Frame(self.master)
        self.utility_frame.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

        self.save_button = tk.Button(self.utility_frame, text="💾", font=("Arial", 12))
        self.save_button.pack(side=tk.TOP, pady=5)

        self.load_button = tk.Button(self.utility_frame, text="📂", font=("Arial", 12))
        self.load_button.pack(side=tk.TOP, pady=5)

    def update_timer_display(self, time_str, color="black"):
        """
        Updates the timer display with the given time string and color.

        Args:
            time_str (str): The time string to display.
            color (str): The color of the text.
        """
        self.timer_label.config(text=time_str, fg=color)

    def update_phase_display(self, phase_name, color="black"):
        """
        Updates the phase display with the given phase name and color.

        Args:
            phase_name (str): The name of the current phase.
            color (str): The color of the text.
        """
        self.status_label.config(text=phase_name, fg=color)

    def update_total_time_display(self, elapsed_str, total_str, color="black"):
        """
        Updates the total time display with the given elapsed and total time strings and color.

        Args:
            elapsed_str (str): The elapsed time string.
            total_str (str): The total time string.
            color (str): The color of the text.
        """
        self.total_time_label.config(text=f"Total Time: {elapsed_str}/{total_str}", fg=color)

    def update_current_phase_total_time(self, time_str, color="black"):
        """
        Updates the current phase total time display with the given time string and color.

        Args:
            time_str (str): The time string to display.
            color (str): The color of the text.
        """
        self.current_phase_total_time_label.config(text=f"Phase Total Time: {time_str}", fg=color)

    def update_button_states(self, running, has_phases):
        """
        Updates the states of the control buttons based on the timer's state.

        Args:
            running (bool): Whether the timer is currently running.
            has_phases (bool): Whether there are phases defined.
        """
        start_state = tk.NORMAL if has_phases and not running else tk.DISABLED
        pause_state = tk.NORMAL if has_phases and running else tk.DISABLED
        reset_state = tk.NORMAL if has_phases and not running else tk.DISABLED
        generate_state = tk.NORMAL if not running else tk.DISABLED

        self.start_pause_button.config(
            text="Pause" if running else "Start",
            state=pause_state if running else start_state
        )
        self.reset_button.config(state=reset_state)
        self.generate_button.config(state=generate_state)

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
            phase_name_label = tk.Label(self.phases_input_frame, text=f"{i + 1}", font=self.small_font)
            phase_name_label.grid(row=i, column=0, padx=10, pady=5)

            phase_name_entry = tk.Entry(self.phases_input_frame, font=self.small_font, width=15)
            phase_name_entry.grid(row=i, column=1, padx=10, pady=5)

            phase_time_entry = tk.Entry(self.phases_input_frame, font=self.small_font, justify='center', width=10)
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
                self.phase_inputs[i][0].delete(0, tk.END)
                self.phase_inputs[i][0].insert(0, name)
                self.phase_inputs[i][1].delete(0, tk.END)
                self.phase_inputs[i][1].insert(0, time)