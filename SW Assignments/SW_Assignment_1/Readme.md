# Software Assignment 1: Rectangular Gate Packing

This assignment implements a heuristic placer for a simplified VLSI-style gate
packing problem. Given a set of fixed-orientation rectangular logic gates, the
program assigns each gate a non-overlapping coordinate in the plane while trying
to minimize the area of the final bounding box.

The assignment is intentionally a stripped-down version of physical design: it
ignores routing and timing, and focuses only on compact geometric placement. The
general rectangle-packing problem is NP-hard, so the implementation uses greedy
and grid-based heuristics rather than an exact exhaustive search.

## Problem

Input gates are rectangular blocks:

```text
g1 <width> <height>
g2 <width> <height>
...
```

The output is a compact bounding box and the bottom-left coordinate of each gate:

```text
bounding_box <width> <height>
g1 <x> <y>
g2 <x> <y>
...
```

Constraints and assumptions:

- Gates cannot be rotated.
- No two gates may overlap.
- The objective is to minimize bounding-box area.
- Wire length, delay, and pin positions are ignored in this first assignment.

## Approach

The project developed three placement strategies, each improving one limitation
of the previous version.

| Algorithm | Idea | Strength | Limitation |
|---|---|---|---|
| Naive row packing | Sort gates by height/width and place them row-wise | Very fast and always constructs a valid layout | Often wastes large blank regions |
| Pixel scan | Maintain an occupancy grid and scan candidate locations pixel by pixel | Finds tighter placements than row packing | Expensive because it checks many occupied cells repeatedly |
| Predictive pixel scan | Store the occupying gate index in each grid cell and jump past already-filled rectangles | Preserves the simple grid model while greatly reducing wasted scans | Still heuristic; quality depends on initial box dimensions and gate order |

The final submitted implementation uses the predictive pixel scan with a
multi-iteration wrapper.

## Key Design Decisions

### 1. Sort large gates first

The parser sorts rectangles by decreasing height and then width before packing.
This makes the greedy placement less likely to leave unusable fragmented gaps
early in the layout.

### 2. Use a finite-growth bounding box search

The first bounding-box guess is derived from total gate area:

```text
initial_width  ~= 1.1 * sqrt(total_gate_area)
initial_height ~= 1.1 * sqrt(total_gate_area)
```

The implementation also enforces lower bounds from the largest gate width and
height. If the current box cannot fit all gates, the width is multiplied by `1.5`
until a feasible packing is found. This guarantees termination because placing
all gates side by side is always a valid upper-bound construction.

### 3. Skip known occupied regions

The predictive scan stores the index of the occupying rectangle in each occupied
grid cell. When the scan reaches an occupied cell, it looks up that rectangle's
right boundary and jumps directly to the first candidate column after it.

This keeps the same loose worst-case `O(n^2)` behavior discussed in the report,
but substantially improves practical runtime by avoiding repeated scans over
filled areas.

### 4. Spend extra iterations only when useful

After the first valid packing is found, the multi-iteration mode perturbs the
candidate width and recomputes the corresponding height. It keeps the best
packing efficiency found, but exits early when:

- packing efficiency crosses `0.95`,
- runtime exceeds the chosen bound,
- or the iteration limit is reached.

This is a deliberate quality/runtime tradeoff. The report found that extra
iterations are most useful for small test cases, especially below roughly 50
gates. For larger cases, the first successful packing is usually already above
95% efficiency, so the multi-iteration and single-iteration behavior converge.

## Metrics

Packing efficiency is measured as:

```text
packing_efficiency = total_gate_area / bounding_box_area
```

### Piazza Sample Cases

| Test case | Gates | Runtime (s) | Packing efficiency |
|---:|---:|---:|---:|
| 1 | 3 | 0.005484 | 0.818181 |
| 2 | 3 | 0.009657 | 0.933333 |
| 3 | 10 | 0.008263 | 0.902778 |
| 4 | 5 | 0.004607 | 0.845238 |
| 5 | 35 | 0.004479 | 0.952381 |

### Generated Stress Tests

The implementation was also evaluated on generated test batches with normally
distributed gate dimensions. The table below reports averages over 100 generated
cases from the assignment report.

| Gates per case | Avg runtime (s), mean=50 std=25 | Avg efficiency, mean=50 std=25 | Avg runtime (s), mean=50 std=10 | Avg efficiency, mean=50 std=10 |
|---:|---:|---:|---:|---:|
| 25 | 0.109190 | 0.898202 | 0.111734 | 0.880246 |
| 100 | 1.802440 | 0.939640 | 1.321254 | 0.927841 |
| 250 | 0.560971 | 0.956785 | 0.984085 | 0.956785 |
| 1000 | 7.327116 | 0.989691 | 4.771615 | 0.977463 |

The runtime curve was observed to be approximately quadratic in the number of
gates for the tested range, matching the grid-search nature of the algorithm.

## Repository Layout

```text
SW_Assignment_1/
+-- COL215_SW_1.pdf
+-- Reading_Resources/
+-- SW_Assignment_1_Files/
    +-- Code/
    |   +-- IO_Parser.py
    |   +-- Pack_by_Pixels.py
    |   +-- Rect.py
    |   +-- test_code.py
    |   +-- testcase_gen.py
    |   +-- txt_analysis.py
    |   +-- project_constants.py
    +-- Reports/
    +-- Sample_Cases/
    +-- Multi_Cases/
    +-- Multi_Single_Comparison/
```

Important files:

| File | Role |
|---|---|
| `COL215_SW_1.pdf` | Original assignment problem statement |
| `SW_Assignment_1_Files/Reports/COL215_SW_Assignment_1_2023CS50334_2023CS10106_Report.pdf` | Final report with design, complexity analysis, graphs, and sample outputs |
| `SW_Assignment_1_Files/Code/Pack_by_Pixels.py` | Implementations of row packing, pixel scan, and predictive pixel scan |
| `SW_Assignment_1_Files/Code/test_code.py` | Main orchestration for single-case and multi-case evaluation |
| `SW_Assignment_1_Files/Code/IO_Parser.py` | Input/output parsing |
| `SW_Assignment_1_Files/Code/testcase_gen.py` | Synthetic testcase generation |
| `SW_Assignment_1_Files/Code/txt_analysis.py` | Plot/report analysis helpers |

## Running the Code

The submitted single-case driver is in:

```text
SW_Assignment_1_Files/Code/test_code.py
```

Expected local workflow:

1. Place `input.txt` in `SW_Assignment_1_Files/Code/`.
2. Ensure `project_constants.py` points `FP_SINGLE_CASE_IN` and
   `FP_SINGLE_CASE_OUT` to the desired local input/output files.
3. Run:

```bash
cd "SW_Assignment_1_Files/Code"
python test_code.py
```

The program writes `output.txt` and prints runtime, bounding-box dimensions, and
packing efficiency. The batch-testing helpers were originally configured with
absolute local Windows paths, so those constants should be updated before
re-running the multi-case experiments on a different machine.

## What This Demonstrates

- Heuristic algorithm design for an NP-hard geometric optimization problem.
- Practical tradeoff analysis between packing quality and runtime.
- Incremental algorithm refinement from a baseline greedy method to a faster
  occupancy-aware grid scan.
- Automated testcase generation and empirical evaluation over varying input
  sizes.
- Clear separation between parsing, geometry representation, packing logic,
  benchmarking, and report generation.

## Authors

Yash Rawat (`2023CS50334`) and Priyanshi Gupta (`2023CS10106`)  
COL215, Semester I 2024-25, IIT Delhi
