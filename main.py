import tkinter as tk
import customtkinter as ctk
from timer_controller import TimerController

def main():
    """
    The main entry point of the application. Initializes the main window and the TimerController.

    Creates the main CustomTkinter window, initializes the TimerController with the root window,
    and starts the CustomTkinter main event loop.
    """
    ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    root = ctk.CTk()
    root.configure(fg_color="black")  # Set background to pure black
    root.after(0, lambda: root.wm_state('zoomed'))
    app = TimerController(root)
    root.mainloop()

if __name__ == "__main__":
    """
    If this module is run as the main program, execute the main function.
    """
    main()