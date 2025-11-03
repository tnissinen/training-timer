import json
import os

class SettingsManager:
    def __init__(self, settings_file="settings.json"):
        """
        Initializes the SettingsManager with the given settings file path.

        Args:
            settings_file (str): Path to the settings file
        """
        self.settings_file = settings_file
        self.settings = self.load_settings()

    def load_settings(self):
        """
        Loads settings from the settings file. If the file doesn't exist or is invalid,
        returns default settings.

        Returns:
            dict: The loaded settings or default settings
        """
        default_settings = {
            "last_program_file": None,
            "sound_enabled": False
        }

        if not os.path.exists(self.settings_file):
            return default_settings

        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Ensure all default keys exist
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
        except (json.JSONDecodeError, IOError):
            return default_settings

    def save_settings(self):
        """
        Saves the current settings to the settings file.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False

    def get(self, key, default=None):
        """
        Gets a setting value by key.

        Args:
            key (str): The setting key
            default: Default value if key doesn't exist

        Returns:
            The setting value or default
        """
        return self.settings.get(key, default)

    def set(self, key, value):
        """
        Sets a setting value and saves to file.

        Args:
            key (str): The setting key
            value: The value to set

        Returns:
            bool: True if successful, False otherwise
        """
        self.settings[key] = value
        return self.save_settings()

    def get_last_program_file(self):
        """
        Gets the last loaded program file path.

        Returns:
            str or None: The file path or None
        """
        return self.get("last_program_file")

    def set_last_program_file(self, file_path):
        """
        Sets the last loaded program file path.

        Args:
            file_path (str): The file path to save

        Returns:
            bool: True if successful, False otherwise
        """
        return self.set("last_program_file", file_path)

    def is_sound_enabled(self):
        """
        Checks if sound is enabled.

        Returns:
            bool: True if sound is enabled, False otherwise
        """
        return self.get("sound_enabled", False)

    def set_sound_enabled(self, enabled):
        """
        Sets the sound enabled state.

        Args:
            enabled (bool): True to enable sound, False to disable

        Returns:
            bool: True if successful, False otherwise
        """
        return self.set("sound_enabled", enabled)
