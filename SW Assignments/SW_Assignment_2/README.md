# Software Assignment 2: Wire-Aware Gate Packing

This assignment extends the rectangular gate-packing problem from Assignment 1
by adding pin locations and wire connections. The goal is no longer just to pack
rectangular gates compactly; the placement must also minimize the estimated
wire length between connected pins.

The implementation uses simulated annealing over a custom gate/pin/wire
abstraction. This is a practical choice for a VLSI-style placement problem where
the exact global optimum is computationally expensive, especially with up to
1000 gates and tens of thousands of pins.

## Problem

Each input file describes:

- rectangular gates with fixed width and height,
- boundary pins with coordinates relative to each gate,
- pin-level wire connections between gates.

The output gives a non-overlapping placement for every gate, the bounding box of
the final layout, and the final estimated wire length.

The assignment uses horizontal/vertical routing estimates. For a connected set of
pins, the estimated wire length is computed using the semi-perimeter of the
bounding box enclosing those pins.

## Core Idea

The search space is too large for exhaustive placement. Instead, the solution
starts from a deterministic non-overlapping placement and then improves it using
simulated annealing:

1. Parse gates, pins, and wires into structured objects.
2. Place every gate inside a fixed-size envelope.
3. Arrange envelopes in a square grid to get an initial legal packing.
4. Repeatedly perturb the placement by swapping or moving gates.
5. Accept better placements immediately and sometimes accept worse placements
   based on the current annealing temperature.
6. Cool the system until the iteration budget or time budget is exhausted.
7. Recompute the final wire length using the assignment-compatible evaluator.

This lets the algorithm escape shallow local minima early, then become more
selective as the temperature falls.

## Data Model

The implementation uses explicit classes instead of keeping the netlist as loose
tuples and dictionaries everywhere.

| Class | Role |
|---|---|
| `Pin` | Stores a pin's parent gate, local coordinate, pin index, and connected pins. |
| `Gate_Env` | Represents a gate plus its enclosing envelope, global coordinates, relative coordinates inside the envelope, and pin dictionary. |
| `Gate_Data` | Stores the full netlist: gates, wires, pin connected components, bounding box, max gate dimensions, and wire-cost state. |
| `Simulated_Annealing` | Owns the annealing state, cost functions, perturbation logic, cooling schedule, and final best packing. |

This structure is useful because wire-cost updates need fast access from a gate
to its pins, from a pin to connected pins, and from a moved gate to the connected
components affected by that move.

## Algorithmic Decisions

### Envelope-Based Non-Overlap Guarantee

Each gate is placed inside an envelope whose dimensions are based on the maximum
gate width and height in the testcase. Envelopes are arranged in a grid and never
overlap. Swapping gates swaps envelope positions, while moving a gate only moves
it inside its own envelope.

This makes the non-overlap invariant simple: if each gate always remains inside
its unique envelope, two gates cannot overlap.

Tradeoff: the bounding box may be larger than a tightly packed layout, but the
search can focus on reducing wire length without repeatedly solving geometric
collision checks.

### Simulated Annealing Instead of Greedy Descent

A purely greedy method would reject every locally worse swap and can get stuck
quickly. Simulated annealing accepts all improving moves and accepts some worse
moves with probability depending on temperature and cost increase.

The implementation uses:

```text
initial_temp = 1e5
min_temp = 0.1
cooling_rate = 0.99
```

The practical result is a controlled search: noisy exploration early, more stable
optimization later.

### Delta Cost Instead of Full Wire Recalculation

The first swap perturbation recomputed the full wire cost after every gate swap.
That was too slow. The improved `perturb_packing_swap_v2` uses
`cost_delta_function`, which recalculates only the connected pin components
affected by the swapped gates.

Measured effect from the report:

| Test setup | Full recomputation | Delta-cost swap |
|---|---:|---:|
| 100 gates, 5474 pins, 20000 wires | 67.1676 s | 2.477151 s |

This is the most important performance improvement in the assignment.

### Adaptive Perturbation Frequency

The number of perturbations per temperature step is controlled by
`perturb_freq_per_iter`. More perturbations usually improve wire cost, but runtime
increases roughly linearly.

The `anneal_routine` performs one trial call, estimates runtime, then chooses a
perturbation frequency using `select_perturb_freq`:

| One-call runtime | Perturbations per temperature step |
|---:|---:|
| `< 0.5 s` | 6 |
| `< 2 s` | 4 |
| `<= 5 s` | 2 |
| `> 5 s` | 1 or 2 depending on size |

This keeps small cases aggressive while avoiding runaway runtime on large cases.

### Swap and Move Perturbations

Two perturbation types were explored:

- `swap`: exchange two gates' envelope positions.
- `move`: move a gate within its own envelope.

The move perturbation can improve smaller testcases by giving the search another
way to reduce wire length, but the report notes that it was not useful enough for
very high pin counts. In the final routine, move perturbations are disabled when
the pin count is above roughly 20000.

### Two Wire-Cost Modes

The annealing loop uses a faster internal connected-component wire heuristic.
The final placement is then evaluated with `wire_cost_function_piazza`, matching
the corrected assignment/evaluator interpretation.

Tradeoff: calling the evaluator-compatible cost inside every annealing step would
be too expensive, so the implementation optimizes a correlated cheaper objective
and recomputes the final cost at the end.

## Complexity Notes

Let:

- `G` = number of gates,
- `P` = number of pins,
- `W` = number of wires,
- `alpha` = perturbations per temperature step.

Key costs:

| Operation | Complexity |
|---|---:|
| Finding connected pin components | `O(P + W)` |
| Generating initial envelope packing | `O(G)` plus initial wire-cost computation |
| Internal wire-cost computation | `O(P)` |
| Delta-cost swap update | proportional to affected connected components; worst-case `O(P)` |
| One annealing call | approximately `O(P * alpha * temperature_steps + P + W + G)` |
| Final evaluator-compatible wire cost | can be much more expensive, up to `O(P^2)` in the worst case |

The report's experiments found that runtime is much more sensitive to pin count
and perturbation frequency than to wire count alone.

## Metrics

### Moodle Testcases

| Test case | Gates | Pins | Wires | Final wire cost |
|---:|---:|---:|---:|---:|
| 1 | 8 | 32 | 11 | 40 |
| 2 | 4 | 14 | 7 | 36 |
| 3 | 25 | 59 | 25 | 98 |
| 4 | 5 | 16 | 9 | 45 |

### Self-Generated Testcases

| Test case | Gates | Pins | Wires | Final wire cost |
|---:|---:|---:|---:|---:|
| 1 | 60 | 194 | 8946 | 14534 |
| 2 | 49 | 169 | 6951 | 11109 |
| 3 | 100 | 335 | 27070 | 36116 |
| 4 | 432 | 1448 | 51585 | 338412 |

### Larger Attached Test Runs

The attached testcase report also includes larger stress cases. A few examples:

| Gates | Pins | Wires | Initial evaluator cost | Final evaluator cost | Runtime |
|---:|---:|---:|---:|---:|---:|
| 10 | 35 | 305 | 1299 | 805 | 15.59 s |
| 100 | 619 | 15332 | 68337 | 64127 | 11.66 s |
| 200 | 1342 | 63110 | 220518 | 214026 | 15.26 s |
| 300 | 15045 | 49740 | 21343116 | 20818515 | 26.85 s |
| 500 | 25093 | 86326 | 46805294 | 46156783 | 18.88 s |

These runs show the intended behavior: the annealing loop consistently reduces
the internal objective, and the final evaluator-compatible wire cost usually drops
as well, while staying within a bounded runtime.

## Relevant Repository Layout

Only the main submitted package and selected analysis artifacts are listed here.
Older working copies, caches, generated bulk testcases, and compressed duplicates
are intentionally omitted.

```text
SW_Assignment_2/
+-- Misc/
|   +-- COL215_SW_2-1.pdf
+-- 2023CS50334_2023CS10106/
|   +-- Assignment Report/
|   |   +-- COL215_SW_Assignment_2_2023CS50334_2023CS10106.pdf
|   +-- Code/
|   |   +-- code.py
|   |   +-- oops.py
|   |   +-- utils.py
|   |   +-- visualization.py
|   |   +-- input.txt
|   |   +-- output.txt
|   +-- Test Cases/
|       +-- Attached/
+-- Report/
|   +-- Graphs/
|   +-- Snaps/
+-- Test_Cases/
    +-- Analysis/
    +-- Moodle/
    +-- Attached/
```

Important files:

| File | Role |
|---|---|
| `Misc/COL215_SW_2-1.pdf` | Updated assignment problem statement |
| `2023CS50334_2023CS10106/Assignment Report/COL215_SW_Assignment_2_2023CS50334_2023CS10106.pdf` | Final report with design, complexity analysis, graphs, and testcase results |
| `2023CS50334_2023CS10106/Code/code.py` | Input/output parsing and main driver |
| `2023CS50334_2023CS10106/Code/oops.py` | Gate, pin, netlist, and simulated annealing classes |
| `2023CS50334_2023CS10106/Code/utils.py` | Constants, timing wrappers, testcase generation, cooling and perturbation helpers |
| `2023CS50334_2023CS10106/Code/visualization.py` | Visualization helper for gate placements |
| `Test_Cases/Analysis/readme.txt` | Notes on performance experiments and algorithm comparisons |
| `Test_Cases/Moodle/Moodle_Final_Report.txt` | Moodle testcase logs |
| `Test_Cases/Attached/attached_tc_report.txt` | Larger attached testcase logs |

## Running the Submitted Code

The submitted single-case entry point is:

```text
2023CS50334_2023CS10106/Code/code.py
```

Expected workflow:

1. Put the testcase in `input.txt`.
2. Ensure `FP_SINGLE_IN` and `FP_SINGLE_OUT` in `utils.py` point to the desired
   local files.
3. Run:

```bash
cd "2023CS50334_2023CS10106/Code"
python code.py
```

The program prints annealing progress and writes `output.txt` with the final
gate coordinates and wire length.

Note: the submitted code keeps the original absolute Windows paths in `utils.py`.
Those paths should be replaced with local relative paths before re-running the
code on another machine.

## What This Demonstrates

- Simulated annealing for a discrete VLSI-style placement problem.
- Object-oriented modelling of gates, envelopes, pins, wires, and netlists.
- Cost-function engineering: fast internal heuristic during search, final
  evaluator-compatible cost at output time.
- Performance optimization through delta-cost updates instead of full cost
  recomputation.
- Empirical tradeoff analysis across pin count, wire count, perturbation
  frequency, and runtime.
- Automated generation and analysis of large synthetic netlists.

## Authors

Yash Rawat (`2023CS50334`) and Priyanshi Gupta (`2023CS10106`)  
COL215, Semester I 2024-25, IIT Delhi
