import time

class TimerModel:
    def __init__(self):
        """
        Initializes the TimerModel with default values.
        """
        self.running = False
        self.finished = False
        self.phase_start_time = None
        self.total_start_time = None
        self.phase_paused_time = 0
        self.total_paused_time = 0
        self.current_phase_index = 0
        self.current_phase_duration = 0
        self.pause_start_time = None

    def start(self):
        """
        Starts the timer. If the timer was paused, it resumes from the paused state.
        """
        if not self.running:
            if self.total_start_time is None:
                self.total_start_time = time.time()
            if self.pause_start_time is not None:
                self.phase_paused_time += time.time() - self.pause_start_time
                self.total_paused_time += time.time() - self.pause_start_time
                self.pause_start_time = None
            else:
                self.phase_start_time = time.time()
            self.running = True

    def pause(self):
        """
        Pauses the timer.
        """
        if self.running:
            self.running = False
            self.pause_start_time = time.time()

    def reset(self):
        """
        Resets the timer to its initial state.
        """
        self.running = False
        self.finished = False
        self.phase_start_time = None
        self.total_start_time = None
        self.phase_paused_time = 0
        self.total_paused_time = 0
        self.pause_start_time = None
        self.current_phase_index = 0

    def get_elapsed_time(self):
        """
        Returns the elapsed time for the current phase.

        Returns:
            float: Elapsed time in seconds.
        """
        if not self.phase_start_time:
            return 0
        if self.running:
            return time.time() - self.phase_start_time - self.phase_paused_time
        elif self.pause_start_time:
            return self.pause_start_time - self.phase_start_time - self.phase_paused_time
        else:
            return 0

    def get_total_elapsed_time(self):
        """
        Returns the total elapsed time since the timer started.

        Returns:
            float: Total elapsed time in seconds.
        """
        if not self.total_start_time:
            return 0
        if self.running:
            return time.time() - self.total_start_time - self.total_paused_time
        elif self.pause_start_time:
            return self.pause_start_time - self.total_start_time - self.total_paused_time
        return 0

    def next_phase(self):
        """
        Moves to the next phase and resets the phase timer.
        """
        self.current_phase_index += 1
        self.phase_start_time = time.time()
        self.phase_paused_time = 0

    def jump_to_phase(self, phase_index, elapsed_before_phase=0):
        """
        Jumps to a specific phase and resets the phase timer.
        Adjusts the total elapsed time to account for skipped phases.

        Args:
            phase_index (int): The index of the phase to jump to.
            elapsed_before_phase (float): Total duration of all phases before this one in seconds.
        """
        self.finished = False  # Clear finished state when jumping
        self.current_phase_index = phase_index
        self.phase_start_time = time.time()
        self.phase_paused_time = 0

        # Adjust total time tracking to reflect jumping to this phase
        if self.total_start_time is not None:
            # Reset total_start_time and total_paused_time to make elapsed time = elapsed_before_phase
            current_time = time.time()
            self.total_start_time = current_time - elapsed_before_phase
            self.total_paused_time = 0

            # If paused, update pause_start_time relative to new total_start_time
            if self.pause_start_time is not None:
                self.pause_start_time = current_time