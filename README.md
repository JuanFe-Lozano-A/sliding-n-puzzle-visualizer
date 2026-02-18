# Sliding N-Puzzle Visualizer

An interactive, high-performance N×N sliding puzzle visualizer and solver with real-time algorithm visualization, heuristic tracking, and adjustable animation speeds.

## 🎮 Features

- **Multiple Solving Algorithms**
  - A* Search with Manhattan Distance heuristic
  - Breadth-First Search (BFS)
  - Extensible architecture for custom solvers

- **Interactive Gameplay**
  - Manual puzzle solving with arrow keys
  - Resizable window with responsive UI
  - Real-time board visualization

- **Algorithm Visualization**
  - Live decision logging showing move sequences
  - Real-time metrics tracking (nodes explored, path cost, etc.)
  - Adjustable animation speeds (0.5Hz to 20Hz)
  - Piece highlighting during solution execution

- **Flexible Board Sizes**
  - Configurable board dimensions (2×2 to 9×9)
  - Dynamic resizing with slider control
  - Responsive layout adapts to window size

## 📋 Requirements

- Python 3.6+
- pygame 2.6+
- numpy

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sliding-n-puzzle
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

Run the application:
```bash
python3 main.py
```

The game opens with a 4×4 puzzle board and control panel on the right side.

### Game Controls

| Control | Action |
|---------|--------|
| **Arrow Keys** | Move puzzle pieces manually |
| **Solve (A*)** | Solve puzzle using A* algorithm with Manhattan Distance heuristic |
| **Solve (BFS)** | Solve puzzle using Breadth-First Search |
| **Shuffle** | Randomize puzzle state |
| **Pause** | Pause/Resume automated solving |
| **Board Size Slider** | Change puzzle dimensions (2×2 to 9×9) |
| **Speed Slider** | Adjust animation speed (0.5Hz - 20Hz) |

### UI Components

- **Left Panel**: Interactive puzzle board with visual feedback
- **Right Sidebar** (400px):
  - Solver buttons (A* and BFS)
  - Shuffle and Pause buttons
  - Board size slider
  - Animation speed slider
  - Decision log (shows move history)
  - Metrics display (algorithm statistics)

## 🏗️ Project Structure

```
sliding-n-puzzle/
├── main.py                 # Application entry point and game loop
├── requirements.txt        # Python dependencies
├── LICENSE
├── README.md
│
├── core/                   # Core game logic
│   ├── board.py           # Board state management
│   ├── shuffler.py        # Puzzle shuffling/randomization
│   └── state_manager.py   # Game state tracking
│
├── solvers/               # Solver algorithms
│   ├── base_solver.py     # Abstract solver interface
│   ├── a_star.py          # A* search implementation
│   ├── bfs.py             # Breadth-First Search implementation
│   └── heuristics.py      # Heuristic functions (Manhattan Distance, etc.)
│
├── ui/                    # User interface and rendering
│   ├── renderer.py        # Board visualization
│   ├── components.py      # UI components (buttons, sliders, logs)
│   └── colors.py          # Color constants
│
├── tests/                 # Unit and integration tests
│   └── test_solvers.py
│
└── assets/                # Game assets (if any)
```

## 🔧 How It Works

### Board Representation
- N×N grid storing tile values (1 to n²-1, with 0 for empty space)
- Supports efficient state transitions and goal checking

### A* Algorithm
- **Heuristic**: Manhattan Distance (optimal for sliding puzzles)
- **Cost Function**: f(n) = g(n) + h(n)
  - g(n): Number of moves from start
  - h(n): Estimated moves to goal
- Efficient exploration with priority queue

### BFS Algorithm
- Explores all states level-by-level
- Guarantees finding shortest solution
- Higher memory usage than A*

### Animation System
- Smooth piece movement based on animation speed
- Real-time rendering at 60 FPS
- Piece highlighting during solver execution

## 🎨 Responsive Design

The application uses a smart layout system:
- **Fixed Sidebar Width**: 400px for controls
- **Dynamic Board Area**: Scales with window size
- **Responsive UI**: All components reposition on window resize
- **Cell Size Calculation**: Automatically adjusted based on available space

```
┌─────────────────────────────────────┬──────────────┐
│                                     │              │
│          Puzzle Board               │ Control      │
│     (Scales with window)            │ Panel        │
│                                     │ (400px)      │
│                                     │              │
└─────────────────────────────────────┴──────────────┘
```

## 📊 Metrics Tracking

When solving, the following metrics are displayed:
- **Nodes Explored**: Total states evaluated
- **Path Cost**: Number of moves in solution
- **Execution Time**: Time taken to find solution
- **Algorithm**: Which solver was used

## ⚙️ Configuration

Board size can be changed via:
1. Slider in the UI (2×2 to 9×9)
2. Modify `n = 4` in `main.py` for default size

Animation speed can be adjusted via the speed slider (0.5Hz - 20Hz):
- Lower values = slower animations
- Higher values = faster animations

## 🚀 Performance Notes

- A* algorithm typically solves 4×4 puzzles in <1s
- BFS may take longer for larger board sizes
- Larger boards (8×8, 9×9) require more computational time
- Window resizing is smooth at 60 FPS with any board size

## 🧪 Testing

Run tests with:
```bash
python3 -m pytest tests/
```

## 🎓 Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|-----------------|------------------|----------|
| A* | O(b^d) | O(b^d) | Small-medium puzzles (faster) |
| BFS | O(b^d) | O(b^d) | Optimal solution guarantee |

*b = branching factor (~3 for sliding puzzle), d = solution depth*

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Feel free to fork, modify, and improve! Potential enhancements:
- Additional heuristics (Linear Conflict, etc.)
- Greedy Best-First Search
- Iterative Deepening A*
- Solution replay system
- Statistics and benchmarking

## 🐛 Known Issues

- Large boards (9×9) may take significant time to solve
- Text rendering may need adjustment on very high DPI displays

## 📧 Support

For issues or questions, please open an issue in the repository.
