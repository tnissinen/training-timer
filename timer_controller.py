import tkinter as tk
from tkinter import filedialog, messagebox
import winsound
import time
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
        self.sound_enabled = False  # Sound is disabled by default

        # Set callback for when phases are changed in the view
        self.view.on_phases_changed_callback = self.bind_phase_jump_events

        self.bind_events()
        self.update_view()
        self.update_button_states()

        # Set initial sound button icon
        self.view.sound_button.configure(text="🔇")

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
        self.view.sound_button.configure(command=self.toggle_sound)
        self.view.edit_button.configure(command=self.view.toggle_edit_mode)

        # Bind keyboard shortcuts (only when not in edit mode)
        self.master.bind('<space>', lambda e: self.toggle_timer() if not self.view.edit_mode else None)
        self.master.bind('<r>', lambda e: self.reset_timer() if not self.view.edit_mode else None)
        self.master.bind('<R>', lambda e: self.reset_timer() if not self.view.edit_mode else None)
        self.master.bind('<F11>', lambda e: self.toggle_fullscreen())

    def bind_phase_jump_events(self):
        """
        Binds click events to phase number labels for jumping to phases.
        """
        if hasattr(self.view, 'phase_number_labels'):
            for i, label in enumerate(self.view.phase_number_labels):
                label.bind("<Button-1>", lambda e, phase_idx=i: self.jump_to_phase(phase_idx))

    def toggle_timer(self):
        """
        Toggles the timer between running and paused states.
        """
        if not self.model.running:
            # Exit edit mode if active
            if self.view.edit_mode:
                self.view.toggle_edit_mode()

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
            # Set progress bar to white when paused
            elapsed_time = self.model.get_elapsed_time()
            if self.model.current_phase_duration > 0:
                progress = min(elapsed_time / self.model.current_phase_duration, 1.0)
                self.view.update_progress_bar(progress, "white")
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
        self.view.update_progress_bar(0, "white")
        self.view.update_global_progress_bar(0)
        self.view.update_current_phase_indicator(-1)  # Hide indicator when reset

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
                self.view.update_progress_bar(0, "white")  # Reset progress bar
                self.view.update_global_progress_bar(0)  # Reset global progress bar
                self.view.update_current_phase_indicator(-1)  # Hide indicator

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
            self.view.update_entry_states()  # Set readonly/normal based on edit_mode
            self.bind_phase_jump_events()  # Bind click events to phase numbers
            self.update_view()
            self.update_button_states()
        except ValueError:
            pass  # Silently ignore invalid input

    def jump_to_phase(self, phase_index):
        """
        Jumps to a specific phase during the workout.

        Args:
            phase_index (int): The index of the phase to jump to.
        """
        # Don't allow jumping in edit mode
        if self.view.edit_mode:
            return

        # Validate phase index
        if phase_index < 0 or phase_index >= len(self.phase_manager.phases):
            return

        # Calculate total elapsed time up to the beginning of this phase
        elapsed_before_phase = 0
        for i in range(phase_index):
            phase = self.phase_manager.get_phase(i)
            if phase:
                minutes, seconds = map(int, phase[1].split(":"))
                elapsed_before_phase += minutes * 60 + seconds

        # Check if timer has been started at all
        was_running = self.model.running
        timer_was_started = self.model.total_start_time is not None

        # If timer hasn't been started yet, initialize it but keep it paused
        if not timer_was_started:
            self.model.total_start_time = time.time()
            self.model.phase_start_time = time.time()
            self.model.running = False
            self.model.pause_start_time = time.time()

        # Update model to new phase with adjusted total time
        self.model.jump_to_phase(phase_index, elapsed_before_phase)
        self.model.current_phase_duration = self.get_current_phase_duration()

        # Update the view
        self.update_view()
        progress_color = "#00ff41" if was_running else "white"
        self.view.update_progress_bar(0, progress_color)  # Reset progress bar for new phase
        self.view.update_current_phase_indicator(phase_index)

        # Update global progress bar based on jumped position
        try:
            total_time = sum(
                int(time.split(":")[0]) * 60 + int(time.split(":")[1]) for _, time in self.phase_manager.phases)
            if total_time > 0:
                global_progress = min(elapsed_before_phase / total_time, 1.0)
                self.view.update_global_progress_bar(global_progress)
        except (ValueError, IndexError):
            pass

        # Display the current phase information
        current_phase = self.phase_manager.get_phase(self.model.current_phase_index)
        if current_phase:
            color = "#00ff41" if was_running else "white"
            self.view.update_phase_display(current_phase[0], color)
            minutes, seconds = map(int, current_phase[1].split(":"))
            self.view.update_current_phase_total_time(f"{minutes:02}:{seconds:02}", "white")

        # Update timer display
        if not was_running:
            self.view.update_timer_display("00:00", "white")


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
            self.view.update_timer_display(time_str, "#00ff41")

            # Update progress bar with green color when running
            if self.model.current_phase_duration > 0:
                progress = min(elapsed_time / self.model.current_phase_duration, 1.0)
                self.view.update_progress_bar(progress, "#00ff41")

            # Update current phase indicator in the list
            self.view.update_current_phase_indicator(self.model.current_phase_index)

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

                    # Update global progress bar
                    if total_time > 0:
                        global_progress = min(total_elapsed_time / total_time, 1.0)
                        self.view.update_global_progress_bar(global_progress)
                except (ValueError, IndexError):
                    total_time_str = "00:00"

                self.view.update_total_time_display(total_str, total_time_str, "white")

            if elapsed_time >= self.model.current_phase_duration:
                self.model.next_phase()
                if self.model.current_phase_index < len(self.phase_manager.phases):
                    self.model.current_phase_duration = self.get_current_phase_duration()
                    self.play_sound()  # Play sound when phase changes
                    self.update_view()
                else:
                    self.finish_timer()

            self.master.after(100, self.update_timer)

    def finish_timer(self):
        """
        Stops the timer and updates the display to indicate the timer has finished.
        """
        self.model.running = False
        self.model.finished = True
        self.play_sound()  # Play sound when timer finishes
        self.view.update_timer_color("#ff0051")
        self.view.update_phase_display("Finished", "#ff0051")
        self.update_button_states()  # Update button states based on finished state
        self.view.update_current_phase_indicator(-1)  # Hide indicator when finished

    def update_view(self):
        """
        Updates the view with the current phase and total time information.
        """
        if self.model.running:
            current_phase = self.phase_manager.get_phase(self.model.current_phase_index)
            if current_phase:
                self.view.update_phase_display(current_phase[0], "#00ff41")
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
        Validates the provided phases and shows error messages.

        Args:
            phases (list): A list of tuples containing phase names and times.

        Returns:
            bool: True if all phases are valid, False otherwise.
        """
        for i, (name, time) in enumerate(phases):
            if not name:
                messagebox.showerror("Validation Error", f"Phase {i+1}: Name cannot be empty")
                return False
            if not time:
                messagebox.showerror("Validation Error", f"Phase {i+1}: Time cannot be empty")
                return False
            if not self.is_valid_time(time):
                messagebox.showerror("Validation Error", f"Phase {i+1}: Invalid time format.\nUse MM:SS (e.g., 01:30 for 1 minute 30 seconds)")
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
        is_finished = self.model.finished
        self.view.update_button_states(is_running, has_phases, is_finished)

    def play_sound(self):
        """
        Plays a system beep sound to notify the user.
        """
        if not self.sound_enabled:
            return
        try:
            winsound.Beep(1000, 500)  # Frequency: 1000 Hz, Duration: 500 ms
        except RuntimeError:
            # If sound fails, silently continue
            pass

    def toggle_sound(self):
        """
        Toggles sound notifications on/off.
        """
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.view.sound_button.configure(text="🔊")
        else:
            self.view.sound_button.configure(text="🔇")