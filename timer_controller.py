import tkinter as tk
from tkinter import filedialog, messagebox
from timer_model import TimerModel
from phase_manager import PhaseManager
from timer_view import TimerView

class TimerController:
    def __init__(self, root):
        """
        Initializes the TimerController with the given root window.
        :param root: The main window of the application.
        """
        self.master = root

        self.model = TimerModel()
        self.phase_manager = PhaseManager()
        self.view = TimerView(root)

        self.bind_events()
        self.update_view()
        self.update_button_states()

    def bind_events(self):
        """
        Binds the control buttons to their respective event handlers.
        """
        self.view.start_pause_button.configure(command=self.toggle_timer)
        self.view.reset_button.configure(command=self.reset_timer)
        self.view.save_button.configure(command=self.save_phases)
        self.view.load_button.configure(command=self.load_phases)
        self.view.generate_button.configure(command=self.generate_phases)
        self.view.fullscreen_button.configure(command=self.toggle_fullscreen)

    def toggle_timer(self):
        """
        Toggles the timer between running and paused states.
        """
        if not self.model.running:
            # Update phase_manager.phases from current input fields before starting
            if hasattr(self.view, 'phase_inputs') and self.view.phase_inputs:
                phases = self.view.get_phase_inputs()
                if self.validate_phases(phases):
                    self.phase_manager.phases = phases
                else:
                    return  # Don't start timer if phases are invalid

            self.model.current_phase_duration = self.get_current_phase_duration()
            self.model.start()
            self.master.after(100, self.update_timer)  # Schedule the next update
        else:
            self.model.pause()
        self.update_view()

    def reset_timer(self):
        """
        Resets the timer to its initial state.
        """
        # Update phase_manager.phases from current input fields before resetting
        if hasattr(self.view, 'phase_inputs') and self.view.phase_inputs:
            phases = self.view.get_phase_inputs()
            if self.validate_phases(phases):
                self.phase_manager.phases = phases

        self.model.reset()
        self.update_view()
        self.update_button_states()
        self.view.update_timer_display("00:00", "white")

        # Display first phase information after reset
        if len(self.phase_manager.phases) > 0:
            first_phase = self.phase_manager.get_phase(0)
            if first_phase:
                self.view.update_phase_display(first_phase[0], "white")
                minutes, seconds = map(int, first_phase[1].split(":"))
                self.view.update_current_phase_total_time(f"{minutes:02}:{seconds:02}", "white")
        else:
            self.view.update_phase_display("", "white")

    def save_phases(self):
        """
        Saves the phases to a JSON file.
        """
        # Check if phase inputs exist
        if not hasattr(self.view, 'phase_inputs') or not self.view.phase_inputs:
            return

        phases = self.view.get_phase_inputs()
        if not self.validate_phases(phases):
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.phase_manager.phases = phases
            self.phase_manager.save_phases(file_path)

    def load_phases(self):
        """
        Loads phases from a JSON file and updates the view.
        """
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            if self.phase_manager.load_phases(file_path):
                # Validate loaded phases
                if not self.validate_phases(self.phase_manager.phases):
                    self.phase_manager.phases = []  # Clear invalid phases
                    return

                # Update UI with loaded phase count and generate inputs
                self.view.num_phases_entry.delete(0, tk.END)
                self.view.num_phases_entry.insert(0, str(len(self.phase_manager.phases)))
                self.generate_phases(is_default=False)

                # Reset timer after inputs are created
                self.model.reset()
                self.update_view()
                self.update_button_states()
                self.view.update_timer_display("00:00", "white")

                # Display first phase information
                if len(self.phase_manager.phases) > 0:
                    first_phase = self.phase_manager.get_phase(0)
                    if first_phase:
                        self.view.update_phase_display(first_phase[0], "white")
                        minutes, seconds = map(int, first_phase[1].split(":"))
                        self.view.update_current_phase_total_time(f"{minutes:02}:{seconds:02}", "white")

    def generate_phases(self, is_default=True):
        """
        Generates the specified number of phases and updates the view.
        """
        try:
            num_phases = int(self.view.num_phases_entry.get())

            # Reset timer when generating new phases
            if is_default:  # Only reset when generating default phases (not when loading)
                self.reset_timer()

            self.view.create_phase_inputs(num_phases)
            if is_default:
                self.phase_manager.generate_default_phases(num_phases)
            self.view.set_phase_inputs(self.phase_manager.phases[:num_phases])
            self.update_view()
            self.update_button_states()
        except ValueError:
            pass  # Silently ignore invalid input


    def toggle_fullscreen(self):
        """
        Toggles the fullscreen mode of the application window.
        """
        is_fullscreen = self.view.master.attributes('-fullscreen')
        if is_fullscreen:
            self.view.master.attributes('-fullscreen', False)
            self.view.master.state('zoomed')
            self.view.fullscreen_button.configure(text="⛶")
        else:
            self.view.master.state('normal')
            self.view.master.attributes('-fullscreen', True)
            self.view.fullscreen_button.configure(text="⯃")

    def update_timer(self):
        """
        Updates the timer display and handles phase transitions.
        """
        if self.model.running:

            elapsed_time = self.model.get_elapsed_time()
            minutes, seconds = divmod(int(elapsed_time), 60)
            time_str = f"{minutes:02}:{seconds:02}"
            self.view.update_timer_display(time_str, "dark green")

            # Update total time display
            total_elapsed_time = self.model.get_total_elapsed_time()

            if total_elapsed_time is not None:
                total_minutes, total_seconds = divmod(int(total_elapsed_time), 60)
                total_str = f"{total_minutes:02}:{total_seconds:02}"

                try:
                    total_time = sum(
                        int(time.split(":")[0]) * 60 + int(time.split(":")[1]) for _, time in self.phase_manager.phases)
                    total_minutes, total_seconds = divmod(total_time, 60)
                    total_time_str = f"{total_minutes:02}:{total_seconds:02}"
                except (ValueError, IndexError):
                    total_time_str = "00:00"

                self.view.update_total_time_display(total_str, total_time_str, "white")

            if elapsed_time >= self.model.current_phase_duration:
                self.model.next_phase()
                if self.model.current_phase_index < len(self.phase_manager.phases):
                    self.model.current_phase_duration = self.get_current_phase_duration()
                    self.update_view()
                else:
                    self.finish_timer()

            self.master.after(100, self.update_timer)

    def finish_timer(self):
        """
        Stops the timer and updates the display to indicate the timer has finished.
        """
        self.model.running = False
        self.view.update_timer_color("dark red")
        self.view.update_phase_display("Finished", "dark red")
        self.view.update_button_states(False, len(self.phase_manager.phases) > 0)

    def update_view(self):
        """
        Updates the view with the current phase and total time information.
        """
        if self.model.running:
            current_phase = self.phase_manager.get_phase(self.model.current_phase_index)
            if current_phase:
                self.view.update_phase_display(current_phase[0], "dark green")
                minutes, seconds = divmod(self.model.current_phase_duration, 60)
                self.view.update_current_phase_total_time(f"{minutes:02}:{seconds:02}", "white")
        else:
            self.view.update_timer_color("white")

        try:
            total_time = sum(
                int(time.split(":")[0]) * 60 + int(time.split(":")[1]) for _, time in self.phase_manager.phases)
            total_minutes, total_seconds = divmod(total_time, 60)
            total_str = f"{total_minutes:02}:{total_seconds:02}"
        except (ValueError, IndexError):
            total_str = "00:00"

        elapsed_time = self.model.get_total_elapsed_time()
        if elapsed_time is not None:
            elapsed_minutes, elapsed_seconds = divmod(int(elapsed_time), 60)
            elapsed_str = f"{elapsed_minutes:02}:{elapsed_seconds:02}"

            self.view.update_total_time_display(elapsed_str, total_str, "white")

        self.update_button_states()

    def get_current_phase_duration(self):
        """
        Retrieves the duration of the current phase.

        Returns:
            int: The duration of the current phase in seconds.
        """
        current_phase = self.phase_manager.get_phase(self.model.current_phase_index)
        if current_phase:
            minutes, seconds = map(int, current_phase[1].split(":"))
            return minutes * 60 + seconds
        return 0

    def validate_phases(self, phases):
        """
        Validates the provided phases.

        Args:
            phases (list): A list of tuples containing phase names and times.

        Returns:
            bool: True if all phases are valid, False otherwise.
        """
        for name, time in phases:
            if not name or not time:
                return False
            if not self.is_valid_time(time):
                return False
        return True

    def is_valid_time(self, time_str):
        """
        Checks if the provided time string is in a valid MM:SS format.

        Args:
            time_str (str): The time string to validate.

        Returns:
            bool: True if the time string is valid, False otherwise.
        """
        try:
            minutes, seconds = map(int, time_str.split(":"))
            return minutes >= 0 and 0 <= seconds < 60
        except ValueError:
            return False

    def update_button_states(self):
        """
        Updates the states of the control buttons based on the timer's state.
        """
        has_phases = len(self.phase_manager.phases) > 0
        is_running = self.model.running
        self.view.update_button_states(is_running, has_phases)