import tkinter as tk
from tkinter import font

class TimerView:
    def __init__(self, master):
        self.master = master
        self.master.title("Exercise Timer")
        self.master.state('zoomed')

        self.timer_font = font.Font(size=80, weight='bold')
        self.medium_font = font.Font(size=30)
        self.small_font = font.Font(size=11)

        self.create_widgets()

    def create_widgets(self):
        # Fullscreen toggle
        self.fullscreen_frame = tk.Frame(self.master)
        self.fullscreen_frame.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)
        self.fullscreen_button = tk.Button(self.fullscreen_frame, text="⛶", font=("Arial", 12))
        self.fullscreen_button.pack()

        # Total time label
        self.total_time_label = tk.Label(self.master, text="Total Time: 00:00/00:00", font=self.medium_font)
        self.total_time_label.pack(pady=10)

        # Current phase frame
        self.current_phase_frame = tk.Frame(self.master)
        self.current_phase_frame.pack(expand=True)

        self.status_label = tk.Label(self.current_phase_frame, text="Stopped", font=self.medium_font)
        self.status_label.pack()

        self.timer_label = tk.Label(self.current_phase_frame, text="00:00", font=self.timer_font, fg="black")
        self.timer_label.pack()

        self.current_phase_total_time_label = tk.Label(self.current_phase_frame, text="Phase Total Time: 00:00", font=self.medium_font)
        self.current_phase_total_time_label.pack()

        # Phase input controls
        self.phase_frame = tk.Frame(self.master)
        self.phase_frame.pack(pady=20)

        self.num_phases_label = tk.Label(self.phase_frame, text="Number of Phases:", font=self.small_font)
        self.num_phases_label.grid(row=0, column=0, padx=10, pady=5)
        self.num_phases_entry = tk.Entry(self.phase_frame, font=self.small_font, justify='center', width=5)
        self.num_phases_entry.grid(row=0, column=1, padx=10, pady=5)

        self.generate_button = tk.Button(self.phase_frame, text="Generate Phases", font=self.small_font)
        self.generate_button.grid(row=0, column=2, padx=10, pady=5)

        # Phase input fields frame
        self.phases_input_frame = tk.Frame(self.master)
        self.phases_input_frame.pack(pady=10)

        # Control buttons
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        self.start_pause_button = tk.Button(self.button_frame, text="Start", font=self.medium_font, width=10)
        self.start_pause_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Reset", font=self.medium_font, width=10)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Utility buttons
        self.utility_frame = tk.Frame(self.master)
        self.utility_frame.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

        self.save_button = tk.Button(self.utility_frame, text="💾", font=("Arial", 12))
        self.save_button.pack(side=tk.TOP, pady=5)

        self.load_button = tk.Button(self.utility_frame, text="📂", font=("Arial", 12))
        self.load_button.pack(side=tk.TOP, pady=5)

    def update_timer_display(self, time_str, color="black"):
        self.timer_label.config(text=time_str, fg=color)

    def update_phase_display(self, phase_name, color="black"):
        self.status_label.config(text=phase_name, fg=color)

    def update_total_time_display(self, elapsed_str, total_str, color="black"):
        self.total_time_label.config(text=f"Total Time: {elapsed_str}/{total_str}", fg=color)

    def update_current_phase_total_time(self, time_str, color="black"):
        self.current_phase_total_time_label.config(text=f"Phase Total Time: {time_str}", fg=color)

    def update_button_states(self, running):
        self.start_pause_button.config(text="Pause" if running else "Start")
        self.reset_button.config(state=tk.DISABLED if running else tk.NORMAL)
        self.generate_button.config(state=tk.DISABLED if running else tk.NORMAL)

    def create_phase_inputs(self, num_phases):
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
        return [(name_entry.get(), time_entry.get()) for name_entry, time_entry in self.phase_inputs]

    def set_phase_inputs(self, phases):
        for i, (name, time) in enumerate(phases):
            if i < len(self.phase_inputs):
                self.phase_inputs[i][0].delete(0, tk.END)
                self.phase_inputs[i][0].insert(0, name)
                self.phase_inputs[i][1].delete(0, tk.END)
                self.phase_inputs[i][1].insert(0, time)