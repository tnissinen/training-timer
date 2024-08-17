import tkinter as tk
from tkinter import font
import time


class TimerApp:
    def __init__(self, root):
        """
        Initialize the TimerApp with the given root window.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Exercise Timer")

        self.default_phases = [("Lämmittely", "02:00"),
                               ("Etuheilautus", "02:00"),
                               ("Rinnalleveto", "02:00"),
                               ("OAJ", "02:00"),
                               ("Etuheilautus", "01:00"),
                               ("OALC", "02:00"),
                               ("Etuheilautus", "01:00"),
                               ("2xtempaus 1min tauolla", "05:00"),
                               ("Etuheilautus", "01:00"),
                               ("OALC", "02:00"),
                               ("Etuheilautus", "02:00")]

        # Set the window size to be slightly smaller than the screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width - 200}x{screen_height - 200}")

        # Define fonts for various UI elements
        self.timer_font = font.Font(size=80, weight='bold')
        self.medium_font = font.Font(size=30)
        self.small_font = font.Font(size=11)

        # Label to display the total time
        self.total_time_label = tk.Label(root, text="Total Time: 00:00/00:00", font=self.medium_font)
        self.total_time_label.pack(pady=10)

        # Frame for the current phase
        self.current_phase_frame = tk.Frame(root)
        self.current_phase_frame.pack(expand=True)

        # Label to display the status (e.g., "Stopped", "Running")
        self.status_label = tk.Label(self.current_phase_frame, text="Stopped", font=self.medium_font)
        self.status_label.pack()

        # Label to display the timer for the current phase
        self.timer_label = tk.Label(self.current_phase_frame, text="00:00", font=self.timer_font, fg="black")
        self.timer_label.pack()

        # Label to display the total time for the current phase
        self.current_phase_total_time_label = tk.Label(self.current_phase_frame, text="Phase Total Time: 00:00", font=self.medium_font)
        self.current_phase_total_time_label.pack()

        # Frame for phase input controls
        self.phase_frame = tk.Frame(root)
        self.phase_frame.pack(pady=20)

        # Label and entry for the number of phases
        self.num_phases_label = tk.Label(self.phase_frame, text="Number of Phases:", font=self.small_font)
        self.num_phases_label.grid(row=0, column=0, padx=10, pady=5)
        self.num_phases = tk.Entry(self.phase_frame, font=self.small_font, justify='center', width=5)
        self.num_phases.insert(0, str(len(self.default_phases)))
        self.num_phases.grid(row=0, column=1, padx=10, pady=5)

        # Button to generate phase inputs
        self.generate_button = tk.Button(self.phase_frame, text="Generate Phases", command=self.generate_phase_inputs, font=self.small_font)
        self.generate_button.grid(row=0, column=2, padx=10, pady=5)

        # Frame for phase input fields
        self.phases_input_frame = tk.Frame(root)
        self.phases_input_frame.pack(pady=10)

        # Frame for control buttons (Start, Reset)
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        # Start/Pause button
        self.start_pause_button = tk.Button(self.button_frame, text="Start", command=self.toggle_timer, font=self.medium_font, width=10)
        self.start_pause_button.pack(side=tk.LEFT, padx=10)
        self.start_pause_button.config(state=tk.DISABLED)

        # Reset button
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_timer, font=self.medium_font, width=10)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Initialize timer state variables
        self.running = False
        self.start_time = None
        self.total_start_time = None
        self.paused_time = 0
        self.total_paused_time = 0
        self.current_phase_index = 0
        self.phases = []
        self.current_phase_duration = 0
        self.total_overall_time_str = "00:00"
        self.pause_start_time = None


    def generate_phase_inputs(self):
        for widget in self.phases_input_frame.winfo_children():
            widget.destroy()

        num_phases = int(self.num_phases.get())
        self.phases = []

        for i in range(num_phases):

            # set phase text from default phases

            if i < len(self.default_phases):
                default_text = "{}:".format(self.default_phases[i][0])
                default_value = self.default_phases[i][1]
            else:
                default_text = "{}:".format(self.default_phases[-1][0])
                default_value = self.default_phases[-1][1]

            phase_name_label = tk.Label(self.phases_input_frame, text=f"Phase {i + 1} Name:", font=self.small_font)
            phase_name_label.grid(row=i, column=0, padx=10, pady=5)

            phase_name_entry = tk.Entry(self.phases_input_frame, font=self.small_font, width=15)
            phase_name_entry.insert(0, default_text)
            phase_name_entry.grid(row=i, column=1, padx=10, pady=5)

            phase_time_label = tk.Label(self.phases_input_frame, text="", font=self.small_font)
            phase_time_label.grid(row=i, column=2, padx=10, pady=5)

            phase_time_entry = tk.Entry(self.phases_input_frame, font=self.small_font, justify='center', width=10)
            phase_time_entry.insert(0, default_value)
            phase_time_entry.grid(row=i, column=3, padx=10, pady=5)

            self.phases.append((phase_name_entry, phase_time_entry))

        self.update_total_time()

        self.start_pause_button.config(state=tk.NORMAL)

    def update_total_time(self):
        total_seconds = 0
        for _, time_entry in self.phases:
            time_input = time_entry.get()
            try:
                minutes, seconds = map(int, time_input.split(":"))
                total_seconds += minutes * 60 + seconds
            except ValueError:
                continue

        total_minutes, total_seconds = divmod(total_seconds, 60)
        total_time_str = f"{total_minutes:02}:{total_seconds:02}"

        self.total_overall_time_str = total_time_str

        if self.total_start_time:
            elapsed_total_seconds = int(time.time() - self.total_start_time - self.total_paused_time)
            elapsed_total_minutes, elapsed_total_seconds = divmod(elapsed_total_seconds, 60)
            elapsed_total_time_str = f"{elapsed_total_minutes:02}:{elapsed_total_seconds:02}"
        else:
            elapsed_total_time_str = "00:00"

        self.total_time_label.config(text=f"Total Time: {elapsed_total_time_str}/{self.total_overall_time_str}")

        if self.current_phase_index < len(self.phases):
            current_phase_time_input = self.phases[self.current_phase_index][1].get()
            try:
                current_phase_minutes, current_phase_seconds = map(int, current_phase_time_input.split(":"))
                current_phase_total_seconds = current_phase_minutes * 60 + current_phase_seconds
            except ValueError:
                current_phase_total_seconds = 0

            current_phase_total_minutes, current_phase_total_seconds = divmod(current_phase_total_seconds, 60)
            current_phase_total_time_str = f"/ {current_phase_total_minutes:02}:{current_phase_total_seconds:02}"
            self.current_phase_total_time_label.config(text=current_phase_total_time_str)

    def toggle_timer(self):
        if not self.running:
            self.start_timer()
        else:
            self.pause_timer()

    def start_timer(self):
        if not self.running:
            if self.total_start_time is None:
                self.load_phases()
                self.total_start_time = time.time()
            if self.pause_start_time is not None:
                self.paused_time += time.time() - self.pause_start_time
                self.total_paused_time += time.time() - self.pause_start_time
            else:
                self.start_time = time.time()
            self.running = True
            self.start_pause_button.config(text="Pause")
            self.update_timer()

    def load_phases(self):
        self.phase_list = []
        for name_entry, time_entry in self.phases:
            name = name_entry.get()
            time_input = time_entry.get()
            try:
                minutes, seconds = map(int, time_input.split(":"))
                phase_seconds = minutes * 60 + seconds
            except ValueError:
                phase_seconds = 0
            if phase_seconds > 0:
                self.phase_list.append((name, phase_seconds))
        self.current_phase_index = 0
        self.paused_time = 0
        self.total_paused_time = 0
        self.start_time = None

        if self.phase_list:
            self.current_phase_duration = self.phase_list[self.current_phase_index][1]
        else:
            self.current_phase_duration = 0

        self.update_status()

    def update_status(self):
        if self.current_phase_index < len(self.phase_list):
            current_phase_name = self.phase_list[self.current_phase_index][0]
            self.status_label.config(text=current_phase_name, fg="dark green")
            self.timer_label.config(fg="dark green")
            self.total_time_label.config(fg="dark green")
            self.current_phase_total_time_label.config(fg="dark green")

            #current_phase_total_minutes, current_phase_total_seconds = divmod(self.current_phase_duration, 60)
            #current_phase_total_time_str = f"Phase Total Time: {current_phase_total_minutes:02}:{current_phase_total_seconds:02}"
            #self.current_phase_total_time_label.config(text=current_phase_total_time_str)
        else:
            self.status_label.config(text="Finished", fg="dark red")
            self.timer_label.config(fg="dark red")
            self.current_phase_total_time_label.config(fg="dark red")
            self.total_time_label.config(fg="dark red")
            self.running = False
            self.start_pause_button.config(text="Start")
            self.start_time = None
            self.total_start_time = None
            self.paused_time = 0
            self.total_paused_time = 0
            self.pause_start_time = None
            self.current_phase_index = 0

    def pause_timer(self):
        if self.running:
            self.running = False
            self.pause_start_time = time.time()
            self.start_pause_button.config(text="Start")

    def reset_timer(self):
        self.running = False
        self.start_time = None
        self.total_start_time = None
        self.paused_time = 0
        self.total_paused_time = 0
        self.pause_start_time = None
        self.current_phase_index = 0
        self.timer_label.config(text="00:00", fg="black")
        self.status_label.config(text="Stopped", fg="black")
        self.total_time_label.config(fg="black")
        self.current_phase_total_time_label.config(fg="black")
        self.start_pause_button.config(text="Start")

        if self.current_phase_index < len(self.phase_list):
            current_phase_total_minutes, current_phase_total_seconds = divmod(self.current_phase_duration, 60)
            current_phase_total_time_str = f"Phase Total Time: {current_phase_total_minutes:02}:{current_phase_total_seconds:02}"
            self.current_phase_total_time_label.config(text=current_phase_total_time_str)

        self.update_total_time()

    def update_timer(self):
        if self.running and self.current_phase_index < len(self.phase_list):
            elapsed_time = time.time() - self.start_time - self.paused_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            time_str = f"{minutes:02}:{seconds:02}"

            self.timer_label.config(text=time_str)
            self.update_total_time()

            if elapsed_time >= self.current_phase_duration:
                self.current_phase_index += 1
                if self.current_phase_index < len(self.phase_list):
                    self.current_phase_duration = self.phase_list[self.current_phase_index][1]
                    self.start_time = time.time()
                    self.paused_time = 0
                    self.update_status()
                    self.root.after(100, self.update_timer)
                else:
                    self.update_status()
            else:
                self.root.after(1000, self.update_timer)

        elif self.current_phase_index >= len(self.phase_list):
            self.total_time_label.config(fg="dark red")
            self.status_label.config(text="Finished", fg="dark red")
            self.timer_label.config(fg="dark red")

            self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
