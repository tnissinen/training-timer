import customtkinter as ctk

class TimerView:
    def __init__(self, master):
        """
        Initializes the TimerView with the given master window.

        Args:
            master (tk.Tk): The main window of the application.
        """
        self.master = master
        self.master.title("Exercise Timer")
        self.master.state('zoomed')

        # Modern color scheme
        self.accent_color = "#00ff41"  # Neon green accent
        self.accent_red = "#ff0051"     # Neon red for finished
        self.text_color = "#ffffff"     # Pure white
        self.input_bg = "#1a1a1a"       # Dark input background
        self.button_hover = "#00cc34"   # Darker green on hover

        # Modern fonts - increased sizes for better visibility
        self.timer_font = ctk.CTkFont(size=120, weight='bold')
        self.big_font = ctk.CTkFont(size=48, weight='bold')
        self.medium_font = ctk.CTkFont(size=28)
        self.total_time_font = ctk.CTkFont(size=36, weight='bold')
        self.semismall_font = ctk.CTkFont(size=18, weight='bold')
        self.small_font = ctk.CTkFont(size=14)

        self.basic_button_width = 140
        self.button_height = 50
        self.edit_mode = False  # Edit mode is off by default

        self.create_widgets()
        self.bind_focus_events()
        self.create_tooltips()

    def create_widgets(self):
        """
        Creates and arranges the widgets in the main window.
        """
        # Frame for total time label with more padding
        self.total_time_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.total_time_frame.pack(side=ctk.TOP, fill=ctk.X, pady=25)
        self.total_time_label = ctk.CTkLabel(self.total_time_frame, text="Total Time: 00:00/00:00",
                                             font=self.total_time_font, text_color=self.text_color)
        self.total_time_label.pack()

        # Main content frame to hold left panel and center content
        self.main_content_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.main_content_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)

        # LEFT SIDE: Phase list panel (increased width)
        self.left_panel = ctk.CTkFrame(self.main_content_frame, fg_color="transparent", width=500)
        self.left_panel.pack(side=ctk.LEFT, fill=ctk.Y, padx=(0, 20))
        self.left_panel.pack_propagate(False)

        # Phase controls at top of left panel
        self.phase_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.phase_frame.pack(pady=(0, 15), fill=ctk.X)

        self.num_phases_label = ctk.CTkLabel(self.phase_frame, text="Phases:", font=self.semismall_font,
                                             text_color=self.text_color)
        # Hidden by default (not in edit mode)

        self.num_phases_entry = ctk.CTkEntry(self.phase_frame, font=self.small_font, justify='center', width=70,
                                             height=40, corner_radius=10, fg_color=self.input_bg,
                                             border_color=self.accent_color, border_width=2)
        # Hidden by default (not in edit mode)

        self.generate_button = ctk.CTkButton(self.phase_frame, text="Generate", font=self.semismall_font,
                                            width=100, height=self.button_height,
                                            corner_radius=12, fg_color=self.accent_color, hover_color=self.button_hover,
                                            text_color="black")
        # Hidden by default (not in edit mode)

        self.edit_button = ctk.CTkButton(self.phase_frame, text="✎", font=("Arial", 20),
                                        width=50, height=50,
                                        corner_radius=12, fg_color="#2a2a2a", hover_color="#3a3a3a",
                                        text_color=self.text_color)
        self.edit_button.pack(side=ctk.RIGHT)

        # Scrollable frame for phase inputs - takes most of left side vertically
        self.phases_input_frame = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent")
        self.phases_input_frame.pack(fill=ctk.BOTH, expand=True)

        # CENTER: Timer display - absolutely positioned in global center
        self.current_phase_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.current_phase_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.status_label = ctk.CTkLabel(self.current_phase_frame, text="", font=self.big_font,
                                         text_color=self.text_color)
        self.status_label.pack(pady=(0, 10))

        self.timer_label = ctk.CTkLabel(self.current_phase_frame, text="00:00", font=self.timer_font,
                                        text_color=self.text_color)
        self.timer_label.pack(pady=10)

        self.current_phase_total_time_label = ctk.CTkLabel(self.current_phase_frame, text="/00:00",
                                                           font=self.medium_font, text_color=self.text_color)
        self.current_phase_total_time_label.pack(pady=(5, 0))

        # Progress bar for current phase
        self.progress_bar = ctk.CTkProgressBar(self.current_phase_frame, width=400, height=20,
                                               corner_radius=10, fg_color="#2a2a2a",
                                               progress_color=self.accent_color)
        self.progress_bar.pack(pady=(20, 0))
        self.progress_bar.set(0)

        # Control buttons below timer
        self.button_frame = ctk.CTkFrame(self.current_phase_frame, fg_color="transparent")
        self.button_frame.pack(pady=30)

        self.start_pause_button = ctk.CTkButton(self.button_frame, text="Start", font=self.semismall_font,
                                                width=self.basic_button_width, height=self.button_height,
                                                corner_radius=12, fg_color=self.accent_color,
                                                hover_color=self.button_hover, text_color="black")
        self.start_pause_button.pack(side=ctk.LEFT, padx=15)

        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", font=self.semismall_font,
                                         width=self.basic_button_width, height=self.button_height,
                                         corner_radius=12, fg_color="#2a2a2a",
                                         hover_color="#3a3a3a", text_color=self.text_color)
        self.reset_button.pack(side=ctk.LEFT, padx=15)

        # Frame for fullscreen, save/load, and sound buttons - placed last so it stays on top
        self.right_button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.right_button_frame.place(relx=0.97, rely=0.2, anchor=ctk.NE)

        self.fullscreen_button = ctk.CTkButton(self.right_button_frame, text="⛶", font=("Arial", 24),
                                               width=60, height=60, corner_radius=15,
                                               fg_color="#2a2a2a", hover_color="#3a3a3a")
        self.fullscreen_button.pack(side=ctk.TOP, pady=8)

        self.save_button = ctk.CTkButton(self.right_button_frame, text="💾", font=("Arial", 24),
                                        width=60, height=60, corner_radius=15,
                                        fg_color="#2a2a2a", hover_color="#3a3a3a")
        self.save_button.pack(side=ctk.TOP, pady=8)

        self.load_button = ctk.CTkButton(self.right_button_frame, text="📂", font=("Arial", 24),
                                        width=60, height=60, corner_radius=15,
                                        fg_color="#2a2a2a", hover_color="#3a3a3a")
        self.load_button.pack(side=ctk.TOP, pady=8)

        self.sound_button = ctk.CTkButton(self.right_button_frame, text="🔊", font=("Arial", 24),
                                         width=60, height=60, corner_radius=15,
                                         fg_color="#2a2a2a", hover_color="#3a3a3a")
        self.sound_button.pack(side=ctk.TOP, pady=8)

    def update_timer_display(self, time_str, color="black"):
        """
        Updates the timer display with the given time string and color.

        Args:
            time_str (str): The time string to display.
            color (str): The color of the text.
        """
        self.timer_label.configure(text=time_str, text_color=color)

    def update_timer_color(self, color="black"):
        """
        Updates the timer display with the given time string and color.

        Args:
            time_str (str): The time string to display.
            color (str): The color of the text.
        """
        self.timer_label.configure(text_color=color)

    def update_phase_display(self, phase_name, color="black"):
        """
        Updates the phase display with the given phase name and color.

        Args:
            phase_name (str): The name of the current phase.
            color (str): The color of the text.
        """
        self.status_label.configure(text=phase_name, text_color=color)

    def update_total_time_display(self, elapsed_str, total_str, color="black"):
        """
        Updates the total time display with the given elapsed and total time strings and color.

        Args:
            elapsed_str (str): The elapsed time string.
            total_str (str): The total time string.
            color (str): The color of the text.
        """
        self.total_time_label.configure(text=f"Total Time: {elapsed_str}/{total_str}", text_color=color)

    def update_current_phase_total_time(self, time_str, color="black"):
        """
        Updates the current phase total time display with the given time string and color.

        Args:
            time_str (str): The time string to display.
            color (str): The color of the text.
        """

        self.current_phase_total_time_label.configure(text=f"/{time_str}", text_color=color)

    def update_progress_bar(self, progress):
        """
        Updates the progress bar with the given progress value.

        Args:
            progress (float): Progress value between 0.0 and 1.0
        """
        self.progress_bar.set(progress)

    def update_current_phase_indicator(self, phase_index):
        """
        Updates the visual indicator to show which phase is currently active.

        Args:
            phase_index (int): The index of the current active phase (-1 to hide all)
        """
        if hasattr(self, 'phase_indicators'):
            for i, indicator in enumerate(self.phase_indicators):
                if i == phase_index:
                    indicator.configure(text="▶")
                else:
                    indicator.configure(text="")

    def update_button_states(self, running, has_phases):
        """
        Updates the states of the control buttons based on the timer's state.

        Args:
            running (bool): Whether the timer is currently running.
            has_phases (bool): Whether there are phases defined.
        """

        start_state = ctk.NORMAL if has_phases and not running else ctk.DISABLED
        pause_state = ctk.NORMAL if has_phases and running else ctk.DISABLED
        reset_state = ctk.NORMAL if has_phases and not running else ctk.DISABLED
        generate_state = ctk.NORMAL if not running else ctk.DISABLED

        start_pause_button_text = "Pause" if running else "Start"
        start_pause_button_state = pause_state if running else start_state

        self.start_pause_button.configure(text=start_pause_button_text, state=start_pause_button_state)
        self.reset_button.configure(state=reset_state)
        self.generate_button.configure(state=generate_state)

    def create_phase_inputs(self, num_phases):
        """
        Creates input fields for the specified number of phases.

        Args:
            num_phases (int): The number of phases to create input fields for.
        """

        for widget in self.phases_input_frame.winfo_children():
            widget.destroy()

        self.phase_inputs = []
        self.remove_buttons = []
        self.phase_indicators = []

        for i in range(num_phases):
            # Indicator for current phase (initially invisible)
            indicator = ctk.CTkLabel(self.phases_input_frame, text="▶", font=("Arial", 14),
                                    text_color=self.accent_color, width=20)
            indicator.grid(row=i, column=0, padx=(0, 0), pady=8, sticky="e")
            indicator.configure(text="")  # Start hidden
            self.phase_indicators.append(indicator)

            phase_name_label = ctk.CTkLabel(self.phases_input_frame, text=f"{i + 1}", font=self.small_font,
                                           text_color=self.text_color, width=30)
            phase_name_label.grid(row=i, column=1, padx=8, pady=8)

            # Create entries - always as normal (we'll manage editability ourselves)
            phase_name_entry = ctk.CTkEntry(self.phases_input_frame, font=self.small_font, width=200,
                                           height=35, corner_radius=8, fg_color=self.input_bg,
                                           border_color="#333333", border_width=1, state="normal")
            phase_name_entry.grid(row=i, column=2, padx=8, pady=8)

            phase_time_entry = ctk.CTkEntry(self.phases_input_frame, font=self.small_font, justify='center',
                                           width=80, height=35, corner_radius=8, fg_color=self.input_bg,
                                           border_color="#333333", border_width=1, state="normal")
            phase_time_entry.grid(row=i, column=3, padx=8, pady=8)

            # Remove button with X icon (only visible in edit mode)
            remove_button = ctk.CTkButton(self.phases_input_frame, text="✕", font=("Arial", 16),
                                         width=35, height=35, corner_radius=8,
                                         fg_color="#2a2a2a", hover_color="#ff0051",
                                         command=lambda idx=i: self.remove_phase(idx))
            if self.edit_mode:
                remove_button.grid(row=i, column=4, padx=8, pady=8)
            else:
                remove_button.grid_forget()

            self.phase_inputs.append((phase_name_entry, phase_time_entry))
            self.remove_buttons.append(remove_button)

    def get_phase_inputs(self):
        """
        Retrieves the phase inputs from the input fields.

        Returns:
            list: A list of tuples containing phase names and times.
        """
        return [(name_entry.get(), time_entry.get()) for name_entry, time_entry in self.phase_inputs]

    def set_phase_inputs(self, phases):
        """
        Sets the phase inputs in the input fields.

        Args:
            phases (list): A list of tuples containing phase names and times.
        """
        for i, (name, time) in enumerate(phases):
            if i < len(self.phase_inputs):
                name_entry = self.phase_inputs[i][0]
                time_entry = self.phase_inputs[i][1]

                # Entries are always normal now, just set values
                name_entry.delete(0, ctk.END)
                name_entry.insert(0, name)
                time_entry.delete(0, ctk.END)
                time_entry.insert(0, time)

    def update_entry_states(self):
        """
        Updates the state of all phase input entries based on edit_mode.
        Always keeps them as "normal" but changes visual appearance.
        """
        if hasattr(self, 'phase_inputs'):
            for name_entry, time_entry in self.phase_inputs:
                # Keep state as normal, but change visual appearance
                name_entry.configure(state="normal")
                time_entry.configure(state="normal")

                if self.edit_mode:
                    # Editable - bright colors
                    name_entry.configure(border_color=self.accent_color, border_width=2)
                    time_entry.configure(border_color=self.accent_color, border_width=2)
                else:
                    # Not editable - dim colors
                    name_entry.configure(border_color="#333333", border_width=1)
                    time_entry.configure(border_color="#333333", border_width=1)

    def bind_focus_events(self):
        """
        Binds click events to remove focus from input fields when clicking outside them.
        Only works when NOT in edit mode.
        """
        def clear_focus(event):
            # Only clear focus if not in edit mode
            if self.edit_mode:
                return

            # Get the widget that was clicked
            widget = event.widget
            # Check if the clicked widget is not an entry field
            if not isinstance(widget, ctk.CTkEntry):
                self.master.focus()

        # Bind to the main window and all major frames
        self.master.bind("<Button-1>", clear_focus)
        self.total_time_frame.bind("<Button-1>", clear_focus)
        self.main_content_frame.bind("<Button-1>", clear_focus)
        self.current_phase_frame.bind("<Button-1>", clear_focus)

    def toggle_edit_mode(self):
        """
        Toggles edit mode for the phase list on/off.
        """
        self.edit_mode = not self.edit_mode

        # Update button appearance and show/hide generate controls
        if self.edit_mode:
            self.edit_button.configure(text="✓", fg_color=self.accent_color, hover_color=self.button_hover, text_color="black")
            # Show generate controls
            self.num_phases_label.pack(side=ctk.LEFT, padx=(0, 10))
            self.num_phases_entry.pack(side=ctk.LEFT, padx=(0, 10))
            self.generate_button.pack(side=ctk.LEFT, padx=(0, 5))
        else:
            self.edit_button.configure(text="✎", fg_color="#2a2a2a", hover_color="#3a3a3a", text_color=self.text_color)
            # Hide generate controls
            self.num_phases_label.pack_forget()
            self.num_phases_entry.pack_forget()
            self.generate_button.pack_forget()

        # Recreate phase inputs with new edit mode
        if hasattr(self, 'phase_inputs') and self.phase_inputs:
            current_phases = self.get_phase_inputs()
            self.create_phase_inputs(len(current_phases))
            self.set_phase_inputs(current_phases)
            self.update_entry_states()  # Set state based on edit mode

    def create_tooltips(self):
        """
        Creates tooltips for icon buttons.
        """
        def create_tooltip(widget, text, position="below"):
            tooltip = None

            def show_tooltip(event):
                nonlocal tooltip
                tooltip = ctk.CTkLabel(self.master, text=text,
                                      font=self.small_font,
                                      fg_color="#2a2a2a",
                                      corner_radius=6,
                                      text_color=self.text_color,
                                      padx=8, pady=4)

                # Update to get actual size
                tooltip.update_idletasks()

                if position == "left":
                    # Position to the left of the widget
                    x = widget.winfo_rootx() - tooltip.winfo_reqwidth() - 10
                    y = widget.winfo_rooty() + widget.winfo_height() // 2 - tooltip.winfo_reqheight() // 2
                else:
                    # Position below the widget (default)
                    x = widget.winfo_rootx() + widget.winfo_width() // 2 - tooltip.winfo_reqwidth() // 2
                    y = widget.winfo_rooty() + widget.winfo_height() + 5

                tooltip.place(x=x - self.master.winfo_rootx(), y=y - self.master.winfo_rooty())

            def hide_tooltip(event):
                nonlocal tooltip
                if tooltip:
                    tooltip.destroy()
                    tooltip = None

            widget.bind("<Enter>", show_tooltip)
            widget.bind("<Leave>", hide_tooltip)

        # Add tooltips to right side buttons (position to the left)
        create_tooltip(self.fullscreen_button, "Fullscreen (F11)", position="left")
        create_tooltip(self.save_button, "Save Routine", position="left")
        create_tooltip(self.load_button, "Load Routine", position="left")
        create_tooltip(self.sound_button, "Toggle Sound", position="left")

        # Edit button on left side (position below)
        create_tooltip(self.edit_button, "Edit Phases", position="below")

    def remove_phase(self, index):
        """
        Removes a phase at the specified index.

        Args:
            index (int): The index of the phase to remove.
        """
        if hasattr(self, 'phase_inputs') and index < len(self.phase_inputs):
            # Get current phase data
            current_phases = self.get_phase_inputs()
            # Remove the phase at the specified index
            current_phases.pop(index)

            # Update the number of phases entry
            self.num_phases_entry.delete(0, ctk.END)
            self.num_phases_entry.insert(0, str(len(current_phases)))

            # Recreate the phase inputs with the new count
            self.create_phase_inputs(len(current_phases))

            # Restore the remaining phase data
            self.set_phase_inputs(current_phases)