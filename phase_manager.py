import json

class PhaseManager:
    def __init__(self):
        """
        Initializes the PhaseManager with default and empty phases.
        """
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

    def load_phases(self, file_path):
        """
        Loads phases from a JSON file.

        Args:
            file_path (str): The path to the JSON file containing phases.

        Returns:
            bool: True if phases were loaded successfully, False otherwise.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                phases_data = json.load(f)
            self.phases = [(phase["name"], phase["time"]) for phase in phases_data]
            return True
        except Exception as e:
            print(f"Failed to load phases: {str(e)}")
            return False

    def save_phases(self, file_path):
        """
        Saves the current phases to a JSON file.

        Args:
            file_path (str): The path to the JSON file to save phases.

        Returns:
            bool: True if phases were saved successfully, False otherwise.
        """
        try:
            phases_data = [{"name": name, "time": time} for name, time in self.phases]
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(phases_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Failed to save phases: {str(e)}")
            return False

    def generate_default_phases(self, num_phases):
        """
        Generates a specified number of default phases.

        Args:
            num_phases (int): The number of default phases to generate.
        """
        self.phases = self.default_phases[:num_phases].copy()

    def get_phase(self, index):
        """
        Retrieves a phase by its index.

        Args:
            index (int): The index of the phase to retrieve.

        Returns:
            tuple: The phase name and time if the index is valid, None otherwise.
        """
        if 0 <= index < len(self.phases):
            return self.phases[index]
        return None

    def set_phase(self, index, name, time):
        """
        Sets the name and time of a phase at a specified index.

        Args:
            index (int): The index of the phase to set.
            name (str): The name of the phase.
            time (str): The time of the phase in MM:SS format.
        """
        if 0 <= index < len(self.phases):
            self.phases[index] = (name, time)

    def add_phase(self, name, time):
        """
        Adds a new phase to the list of phases.

        Args:
            name (str): The name of the phase.
            time (str): The time of the phase in MM:SS format.
        """
        self.phases.append((name, time))

    def remove_phase(self, index):
        """
        Removes a phase by its index.

        Args:
            index (int): The index of the phase to remove.
        """
        if 0 <= index < len(self.phases):
            del self.phases[index]

    def get_phase_count(self):
        """
        Returns the number of phases.

        Returns:
            int: The number of phases.
        """
        return len(self.phases)