# Curses Based Cellular Automata

![Demo image](assets/homescreen.gif)

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/github/license/Zadeson/Curses-Based-Cellular-Automata?color=blue)](https://opensource.org/licenses/MIT)
[![Repo Size](https://img.shields.io/github/repo-size/Zadeson/Curses-Based-Cellular-Automata)](https://github.com/Zadeson/Curses-Based-Cellular-Automata)
[![Commit Activity](https://img.shields.io/github/commit-activity/y/Zadeson/Curses-Based-Cellular-Automata)](https://github.com/Zadeson/Curses-Based-Cellular-Automata)

Immerse yourself in an intriguing cellular automata world that simulates life using ASCII characters. Now featuring real-time commentary, leaderboard, and more! 

This Python script provides a real-time simulation of cellular automata, displayed within a terminal window using the `curses` library. The simulation includes various families of cells that evolve over time according to the rules set. The project also incorporates features like live commentary, leaderboards, and a graphical representation of cell populations over generations.

## Features

- Customizable characters
- Real-time generation and death rate tracking
- Dynamic commentary feed
- Leaderboard stats
- In-game drawing and erasing
- Clean and divided UI
- Pause and resume functionality

## Who Uses This?

- **Researchers**: For studying cellular automata behavior.
- **Educators**: As a teaching tool for explaining the concept of cellular automata.
- **Hobbyists**: For fun and to appreciate the complexity that can arise from simple rules.

## How It Works

The script uses the `curses` library for rendering the cellular automata in the terminal window in real-time. The families of cells are initialized based on user input, and they evolve over generations according to specific rules:

1. **Initialization**: The grid is initialized with cells from different families based on user input.
2. **Evolution**: In each generation, every cell's neighborhood is checked, and the cell evolves based on a set of rules.
3. **Commentary and Leaderboard**: A live commentary and leaderboard are updated based on events and family statistics.
4. **Graph**: At the end, a graph plotting the population of each family over time is displayed using `matplotlib`.


## Todo

- [ ] Optimize performance for larger grids
- [ ] Add sound effects for events like extinction and domination
- [ ] Implement save and load functionality for game states
- [ ] Add more cellular automata rules and behaviors
- [ ] Improve UI aesthetics and responsiveness

## Usage

1. **Installation**: Ensure Python 3.x and required libraries (`curses`, `matplotlib`, `questionary`) are installed.
2. **Running the Script**: Run the script using the command `python3 CellularAutomata.py`.
3. **Initial Configuration**: Answer the prompt questions to configure the cellular automata.
4. **Controls**: 
   - Press 'q' to quit.
   - Press 'space' to pause/unpause.
   - Press 'tab' to toggle the drawing character.

For detailed code implementation, please refer to the source code.

## Bugs and Feature Requests

Found a bug or want to request a feature? Please open an issue on the [issue tracker](https://github.com/Zadeson/Curses-Based-Cellular-Automata/issues).

