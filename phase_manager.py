import json

class PhaseManager:
    def __init__(self):
        self.phases = []
        self.default_phases = [
            ("Lämmittely", "02:00"),
            ("Etuheilautus", "02:00"),
            ("Rinnalleveto", "02:00"),
            ("OAJ", "02:00"),
            ("Etuheilautus", "01:00"),
            ("OALC", "02:00"),
            ("Etuheilautus", "01:00"),
            ("2xtempaus 1min tauolla", "05:00"),
            ("Etuheilautus", "01:00"),
            ("OALC", "02:00"),
            ("Etuheilautus", "02:00")
        ]
        self.generate_default_phases()

    def load_phases(self, file_path):
        try:
            with open(file_path, "r") as f:
                phases_data = json.load(f)
            self.phases = [(phase["name"], phase["time"]) for phase in phases_data]
            return True
        except Exception as e:
            print(f"Failed to load phases: {str(e)}")
            return False

    def save_phases(self, file_path):
        try:
            phases_data = [{"name": name, "time": time} for name, time in self.phases]
            with open(file_path, "w") as f:
                json.dump(phases_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save phases: {str(e)}")
            return False

    def generate_default_phases(self):
        self.phases = self.default_phases.copy()

    def get_phase(self, index):
        if 0 <= index < len(self.phases):
            return self.phases[index]
        return None

    def set_phase(self, index, name, time):
        if 0 <= index < len(self.phases):
            self.phases[index] = (name, time)

    def add_phase(self, name, time):
        self.phases.append((name, time))

    def remove_phase(self, index):
        if 0 <= index < len(self.phases):
            del self.phases[index]

    def get_phase_count(self):
        return len(self.phases)