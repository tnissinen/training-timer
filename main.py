import tkinter as tk
from timer_controller import TimerController

def main():
    root = tk.Tk()
    app = TimerController(root)
    root.mainloop()

if __name__ == "__main__":
    main()