import tkinter as tk
from tkinter import font
import time


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exercise Timer")

        # Set the window to be almost fullscreen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width - 100}x{screen_height - 100}")

        # Font for various UI elements
        self.timer_font = font.Font(size=80, weight='bold')
        self.medium_font = font.Font(size=30)
        self.small_font = font.Font(size=20)

        # Create an info label to display the phase status at the top of the screen
        self.status_label = tk.Label(root, text="Stopped", font=self.medium_font)
        self.status_label.pack(pady=10)

        # Create a label to display the timer in the middle of the screen
        self.timer_label = tk.Label(root, text="00:00", font=self.timer_font, fg="black")
        self.timer_label.pack(expand=True)

        # Create a frame to hold the phase inputs
        self.phase_frame = tk.Frame(root)
        self.phase_frame.pack(pady=20)

        # Create an entry for the number of phases
        self.num_phases_label = tk.Label(self.phase_frame, text="Number of Phases:", font=self.small_font)
        self.num_phases_label.grid(row=0, column=0, padx=10, pady=5)
        self.num_phases = tk.Entry(self.phase_frame, font=self.small_font, justify='center', width=5)
        self.num_phases.insert(0, "3")  # Default number of phases is 3
        self.num_phases.grid(row=0, column=1, padx=10, pady=5)

        # Create a button to generate phase inputs
        self.generate_button = tk.Button(self.phase_frame, text="Generate Phases", command=self.generate_phase_inputs, font=self.small_font)
        self.generate_button.grid(row=0, column=2, padx=10, pady=5)

        # Create a frame to hold the phase input fields
        self.phases_input_frame = tk.Frame(root)
        self.phases_input_frame.pack(pady=10)

        # Create a frame to hold the buttons at the bottom of the window
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        # Create a single button for Start/Pause
        self.start_pause_button = tk.Button(self.button_frame, text="Start", command=self.toggle_timer, font=self.medium_font, width=10)
        self.start_pause_button.pack(side=tk.LEFT, padx=10)

        # Create a Reset button, placed beside the Start/Pause button
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_timer, font=self.medium_font, width=10)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Initialize timer variables
        self.running = False
        self.start_time = None
        self.paused_time = 0
        self.current_phase_index = 0
        self.phases = []
        self.current_phase_duration = 0

    def generate_phase_inputs(self):
        """Generate input fields for the number of phases specified."""
        for widget in self.phases_input_frame.winfo_children():
            widget.destroy()  # Clear any existing input fields

        num_phases = int(self.num_phases.get())
        self.phases = []

        for i in range(num_phases):
            phase_name_label = tk.Label(self.phases_input_frame, text=f"Phase {i + 1} Name:", font=self.small_font)
            phase_name_label.grid(row=i, column=0, padx=10, pady=5)

            phase_name_entry = tk.Entry(self.phases_input_frame, font=self.small_font, width=15)
            phase_name_entry.grid(row=i, column=1, padx=10, pady=5)

            phase_time_label = tk.Label(self.phases_input_frame, text="Time (MM:SS):", font=self.small_font)
            phase_time_label.grid(row=i, column=2, padx=10, pady=5)

            phase_time_entry = tk.Entry(self.phases_input_frame, font=self.small_font, justify='center', width=10)
            phase_time_entry.grid(row=i, column=3, padx=10, pady=5)

            self.phases.append((phase_name_entry, phase_time_entry))

    def toggle_timer(self):
        if not self.running:
            # Start or resume the timer
            self.start_timer()
        else:
            # Pause the timer
            self.pause_timer()

    def start_timer(self):
        if not self.running:
            # Initialize phases if starting from zero
            if self.start_time is None:
                self.load_phases()

            # Start the timer
            self.start_time = time.time() - self.paused_time
            self.running = True
            self.start_pause_button.config(text="Pause")
            self.update_timer()

    def load_phases(self):
        self.phase_list = []
        for name_entry, time_entry in self.phases:
            name = name_entry.get()
            time_input = time_entry.get()
            minutes, seconds = map(int, time_input.split(":"))
            phase_seconds = minutes * 60 + seconds
            self.phase_list.append((name, phase_seconds))
        self.current_phase_index = 0
        self.paused_time = 0
        self.start_time = None
        self.current_phase_duration = self.phase_list[self.current_phase_index][1]
        self.update_status()

    def update_status(self):
        if self.current_phase_index < len(self.phase_list):
            current_phase_name = self.phase_list[self.current_phase_index][0]
            self.status_label.config(text=current_phase_name, fg="dark green")
            self.timer_label.config(fg="dark green")
        else:
            self.status_label.config(text="Finished", fg="dark red")
            self.timer_label.config(fg="dark red")
            self.running = False

    def pause_timer(self):
        if self.running:
            self.running = False
            self.paused_time = time.time() - self.start_time
            self.start_pause_button.config(text="Start")
            self.status_label.config(fg="black")
            self.timer_label.config(fg="black")

    def reset_timer(self):
        self.running = False
        self.start_time = None
        self.paused_time = 0
        self.current_phase_index = 0
        self.timer_label.config(text="00:00", fg="black")
        self.status_label.config(text="Stopped", fg="black")
        self.start_pause_button.config(text="Start")

    def update_timer(self):
        if self.running and self.current_phase_index < len(self.phase_list):
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            time_str = f"{minutes:02}:{seconds:02}"
            self.timer_label.config(text=time_str)

            if elapsed_time >= self.current_phase_duration:
                self.current_phase_index += 1
                if self.current_phase_index < len(self.phase_list):
                    # Update the duration for the next phase
                    self.current_phase_duration = self.phase_list[self.current_phase_index][1]
                    self.start_time = time.time()  # Start timing the next phase
                    self.update_status()
                else:
                    self.update_status()  # Finish the timer if no more phases
            else:
                self.root.after(1000, self.update_timer)  # Update the timer every second

        elif self.current_phase_index >= len(self.phase_list):
            self.status_label.config(text="Finished", fg="dark red")
            self.timer_label.config(fg="dark red")
            self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
