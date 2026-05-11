# Search and Pathfinding Visualizer

Interactive weighted pathfinding visualizer implementing Dijkstra’s shortest path algorithm using Python and Tkinter.

## Overview

This project is an interactive visualization tool designed to demonstrate how Dijkstra’s shortest path algorithm works in weighted environments. Users can create custom mazes, place walls and weighted swamp cells, and visualize how the algorithm explores nodes and finds the minimum-cost path.

The application was developed using Python and Tkinter for graphical user interface design.

---

## Features

* Interactive grid-based maze editor
* Adjustable start and destination nodes
* Wall and swamp terrain generation
* Weighted shortest path calculation
* Real-time visualization of visited nodes
* Minimum-cost path highlighting
* Dijkstra’s shortest path algorithm implementation
* User-friendly GUI using Tkinter

---

## Technologies Used

* Python
* Tkinter
* heapq

---

## Algorithm

The project uses Dijkstra’s Algorithm to calculate the minimum-cost path between two nodes in a weighted graph.

### Cell Costs

| Cell Type  | Cost            |
| ---------- | --------------- |
| Empty Cell | 1               |
| Swamp Cell | 5               |
| Wall       | Not Traversable |

The algorithm evaluates neighboring nodes and always selects the path with the lowest cumulative traversal cost.

---

## Project Structure

```bash
Search-and-Pathfinding-Visualizer/
│
├── main.py
├── Search & Pathfinding Visualizer Using Dijkstra’s Algorithm.pdf
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/BTec-lab/Search-and-Pathfinding-Visualizer.git
```

Navigate to the project folder:

```bash
cd Search-and-Pathfinding-Visualizer
```

Run the application:

```bash
python main.py
```

---

## Usage

1. Select the start node.
2. Select the destination node.
3. Draw walls or swamp regions.
4. Run the algorithm.
5. Observe visited nodes and the minimum-cost path visualization.

---

## Demonstration Video

YouTube Demo:

[https://youtu.be/_9VBjD6drO4](https://youtu.be/_9VBjD6drO4)

---

## Screenshots

You can add screenshots of the application here.

---

## Author

Berkan Tuncel

Electrical and Electronics Engineering Student

---

## License

This project is intended for educational and academic purposes.
