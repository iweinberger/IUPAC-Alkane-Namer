# Developer Guide — IUPAC Alkane Namer

## 🚀 Overview
This project is a small desktop application built with **Pygame** that lets users build, visualize, and generate IUPAC names for alkane-style molecules. The UI is page-driven, and the core molecular logic is implemented in the `Atom` and `Alkane` classes.

## 🧱 Key Components

### 📄 `main.py`
- Entry point of the application.
- Creates pages and starts the main `window` loop.
- Pages are provided in a `window.page_list` and swapped by setting `window.page`.

### 🧩 Pages (UI Screens)
Each page is implemented as three functions, then wrapped into a `page` object:
- `*_definitions(window)` — called once when page is activated.
- `*_page(screen, window)` — called each frame to render the UI.
- `*_event_handler(window, event, key)` — called on every event.

Pages in this project:
- `Main_Page.py` — main menu
- `Molecule_Display.py` — molecule builder/editor
- `Imports_Page.py` — load saved molecule files
- `close_window.py` — save confirmation dialog (separate process)

### 🧬 Molecular Model
- `Alkane_Classes.py` contains:
  - `Atom` — stores element, bonds, rendering, collision detection, and naming logic.
  - `Alkane` — represents a main carbon chain for naming.

### 🪟 Window + UI Framework
- `Window_Classes.py` implements:
  - `window` — high-level application loop, titlebar, resizing, and event propagation.
  - `page` — container for page functions.
  - `button` — basic UI button with hover and click styles.

## 🏃 Running the App
From the project root:
```powershell
python main.py
```

## 🧩 Extending the App
### Adding a new page
1. Create a new module (e.g., `New_Page.py`).
2. Define `New_Page_definitions`, `New_Page_page`, and `New_Page_event_handler`.
3. Import and register in `main.py` by adding to the `page_list`.

### Adding a new molecule tool
1. Add a new `window.activity` integer mode in `Molecule_Display_definitions`.
2. Hook the mode into the UI (add button) and define behavior in `Molecule_Display_event_handler`.

## 🧪 Saving / Loading
- Molecules are serialized with Python `pickle` via:
  - `Atom.export_molocule(filename)` and `Atom.import_molocule(filename)`.
- Saved file path is selected in `Imports_Page.py`.

## 📌 Style Notes
- The project uses a simple home-grown UI system: `button` objects with `draw()` and `on_click()` methods.
- Most UI state is stored directly on the `window` object (e.g., `window.saved`, `window.activity`).
