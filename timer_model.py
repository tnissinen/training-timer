import time

class TimerModel:
    def __init__(self):
        self.running = False
        self.start_time = None
        self.total_start_time = None
        self.paused_time = 0
        self.total_paused_time = 0
        self.current_phase_index = 0
        self.current_phase_duration = 0
        self.pause_start_time = None

    def start(self):
        if not self.running:
            if self.total_start_time is None:
                self.total_start_time = time.time()
            if self.pause_start_time is not None:
                self.paused_time += time.time() - self.pause_start_time
                self.total_paused_time += time.time() - self.pause_start_time
                self.pause_start_time = None
            else:
                self.start_time = time.time()
            self.running = True

    def pause(self):
        if self.running:
            self.running = False
            self.pause_start_time = time.time()

    def reset(self):
        self.running = False
        self.start_time = None
        self.total_start_time = None
        self.paused_time = 0
        self.total_paused_time = 0
        self.pause_start_time = None
        self.current_phase_index = 0

    def get_elapsed_time(self):
        if not self.start_time:
            return 0
        if self.running:
            return time.time() - self.start_time - self.paused_time
        elif self.pause_start_time:
            return self.pause_start_time - self.start_time - self.paused_time
        else:
            return 0

    def get_total_elapsed_time(self):
        if not self.total_start_time:
            return 0
        return time.time() - self.total_start_time - self.total_paused_time

    def next_phase(self):
        self.current_phase_index += 1
        self.start_time = time.time()
        self.paused_time = 0