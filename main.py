import tkinter as tk
from timer_controller import TimerController

def main():
    """
    The main entry point of the application. Initializes the main window and the TimerController.

    Creates the main Tkinter window, initializes the TimerController with the root window,
    and starts the Tkinter main event loop.
    """
    root = tk.Tk()
    app = TimerController(root)
    root.mainloop()

if __name__ == "__main__":
    """
    If this module is run as the main program, execute the main function.
    """
    main()