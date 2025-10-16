# Training Timer

A professional interval training timer application designed for managing multi-phase workout routines with customizable durations and audio notifications.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Multi-Phase Workouts**: Create and manage unlimited workout phases with custom names and durations
- **Visual Progress Tracking**: Large, easily readable timer display with real-time progress bar
- **Audio Notifications**: Sound alerts when transitioning between phases (toggleable)
- **Workout Persistence**: Save and load custom workout routines as JSON files
- **Modern Dark UI**: Sleek interface built with CustomTkinter featuring neon green accents
- **Keyboard Shortcuts**: Quick controls for efficient workout management
- **Fullscreen Mode**: Distraction-free training experience
- **Edit Mode**: Live editing of workout phases without stopping your session
- **Total Time Tracking**: Monitor both current phase and total workout elapsed time
- **Phase Jumping**: Click any phase number to instantly jump to that phase during your workout

## Screenshots

The application features a 3-panel layout:
- **Left**: Phase list with current phase indicator (▶)
- **Center**: Large timer display (120pt font) with progress bar
- **Right**: Control buttons (fullscreen, save, load, sound toggle)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/training-timer.git
cd training-timer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Basic Controls

#### Mouse Controls
- **Start/Pause Button**: Begin or pause the timer
- **Reset Button**: Reset timer to beginning
- **Phase Numbers (1, 2, 3...)**: Click any phase number to jump directly to that phase during workout
- **Edit Button (✎)**: Toggle edit mode to modify phases
- **Fullscreen Button**: Enter/exit fullscreen mode
- **Save Button**: Save current workout routine to JSON file
- **Load Button**: Load a saved workout routine
- **Sound Button**: Toggle audio notifications

#### Keyboard Shortcuts
- **Space**: Start/Pause timer
- **R**: Reset timer
- **F11**: Toggle fullscreen mode

### Creating Custom Workouts

1. Click the **Edit button (✎)** to enter edit mode
2. Modify phase names and durations (format: MM:SS)
3. Use **+ Add Phase** to add new phases
4. Use **✕** button next to phases to remove them
5. Click **Generate Default Phases** to restore the 11 built-in phases
6. Click **Save** to persist your workout routine

### Phase Duration Format

All phase durations must be in **MM:SS** format:
- `05:00` = 5 minutes
- `00:30` = 30 seconds
- `12:45` = 12 minutes and 45 seconds

### Default Phases

The application includes 11 pre-configured phases for a complete workout routine:
1. Lämmittely (Warm-up) - 03:00
2. Etuheilautus (Arm swings) - 00:30
3. Leuanvetoa (Pull-ups) - 00:30
4. Dippejä (Dips) - 00:30
5. Punnerruksia (Push-ups) - 00:30
6. Kyykkyä (Squats) - 00:30
7. Istumaannousua (Sit-ups) - 00:30
8. Juoksua (Running) - 03:00
9. Liikkuvuusharjoitus (Mobility) - 03:00
10. Venyttelyä (Stretching) - 03:00
11. Loppuverryttely (Cool-down) - 03:00

**Total duration**: ~18 minutes

## Project Structure

```
training-timer/
├── main.py                 # Application entry point
├── timer_model.py          # Timer state management (MVC Model)
├── timer_view.py           # UI rendering (MVC View)
├── timer_controller.py     # Business logic (MVC Controller)
├── phase_manager.py        # Workout phase data management
├── test_timer.py           # Unit tests
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── saved_phases.json      # Example workout routines
```

## Architecture

The application follows the **Model-View-Controller (MVC)** pattern:

- **Model** (`TimerModel`): Manages timer state, elapsed time calculations, and phase tracking
- **View** (`TimerView`): Handles UI rendering and user interface updates
- **Controller** (`TimerController`): Coordinates Model and View, handles user input and business logic
- **Helper** (`PhaseManager`): Manages workout phase data and JSON persistence

This architecture provides:
- Clean separation of concerns
- Easy testing of individual components
- Independent UI updates from timer logic
- Isolated phase data management

## Development

### Running Tests

Execute the test suite:
```bash
python -m unittest test_timer.py
```

Or run with verbose output:
```bash
python -m unittest test_timer.py -v
```

### Test Coverage

The test suite covers:
- Timer state management (start, pause, reset)
- Elapsed time calculations
- Phase CRUD operations
- Phase validation (MM:SS format)
- JSON save/load operations
- Default phase generation

## Customization

### Color Scheme

The default color scheme features:
- Background: Pure black (#000000)
- Primary accent: Neon green (#00ff41)
- Error/Finish: Neon red (#ff0051)
- Input fields: Dark gray (#1a1a1a)

Colors can be customized in `timer_view.py`.

### Audio Notifications

Audio notifications use Windows `winsound.Beep()`. For cross-platform support, consider integrating libraries like `playsound` or `pygame.mixer`.

## File Format

Workout routines are saved as JSON files with the following structure:

```json
[
  {
    "name": "Lämmittely",
    "duration": "03:00"
  },
  {
    "name": "Etuheilautus",
    "duration": "00:30"
  }
]
```

## Known Limitations

- Audio notifications are Windows-specific (uses `winsound`)
- Phase durations must be in MM:SS format (no hours support)
- No pause between phase transitions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for modern UI components
- Icons and UI design inspired by modern fitness applications
- Recent improvements made with Claude Code assistance

## Support

If you encounter any issues or have questions, please open an issue on GitHub.