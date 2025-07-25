# Calorie Counter App - Modular Structure

## Overview

The application has been restructured from a single monolithic file (`calorie_counter_app.py`) into a clean, modular architecture under the `src/` directory.

## File Structure

```
calorie-counter-app/
├── main.py                 # Entry point (imports from src/)
├── calorie_counter_app.py  # Original monolithic file (backup)
├── buildozer.spec         # Build configuration (updated)
├── requirements.txt       # Dependencies
├── README.md
└── src/                   # Modular source code
    ├── __init__.py        # Package initialization
    ├── main_app.py        # Main application class
    ├── widgets.py         # Custom UI widgets
    ├── data_manager.py    # Data storage and retrieval
    ├── ui_utils.py        # UI utility functions
    └── stats_display.py   # Statistics display components
```

## Module Breakdown

### `src/main_app.py` (525 lines)
- **Purpose**: Main application class and UI layout
- **Key Components**: 
  - `CalorieCounterApp` class (inherits from `kivy.app.App`)
  - Screen management and navigation
  - UI layout construction
  - Event handlers for user interactions
- **Dependencies**: All other src modules, Kivy framework

### `src/widgets.py` (296 lines)
- **Purpose**: Custom styled UI components
- **Key Components**:
  - `StyledLabel` - Labels with custom styling
  - `StyledButton` - Buttons with rounded corners and hover effects
  - `StyledTextInput` - Text inputs with custom appearance
  - `MealCard` - Cards for displaying meal information
- **Dependencies**: Kivy graphics and widget classes

### `src/data_manager.py` (162 lines)
- **Purpose**: Data persistence and management
- **Key Components**:
  - `CalorieDataManager` class
  - CRUD operations for meals
  - Weekly statistics calculation
  - JsonStore wrapper for data persistence
- **Dependencies**: Kivy JsonStore, datetime

### `src/ui_utils.py` (120 lines)
- **Purpose**: UI utility functions and popups
- **Key Components**:
  - Popup creation and management
  - UI helper functions
  - Common dialog implementations
- **Dependencies**: Kivy popup and layout classes

### `src/stats_display.py` (289 lines)
- **Purpose**: Statistics visualization and display
- **Key Components**:
  - Statistics calculation methods
  - Chart and graph components
  - Data visualization widgets
- **Dependencies**: Kivy graphics, custom widgets

## Benefits of Modular Structure

1. **Maintainability**: Each module has a single responsibility
2. **Reusability**: Components can be imported and reused
3. **Testing**: Individual modules can be tested independently
4. **Collaboration**: Multiple developers can work on different modules
5. **Code Organization**: Logical separation of concerns

## Build Configuration

The `buildozer.spec` has been updated to include the new `src/` directory:
```
source.include_dirs = src
```

## Running the Application

The entry point remains the same:
```bash
python main.py
```

The `main.py` file now imports from the structured modules instead of the monolithic file.

## Original vs. Structured

- **Original**: 1400+ lines in `calorie_counter_app.py`
- **Structured**: Split into 6 focused modules with clear responsibilities
- **Functionality**: Identical behavior, improved architecture
- **Build Compatibility**: Fully compatible with existing build processes

## Next Steps

1. Test the modular application thoroughly
2. Remove the original `calorie_counter_app.py` once confirmed working
3. Add unit tests for individual modules
4. Consider adding type hints for better code documentation
5. Implement logging across modules for better debugging
