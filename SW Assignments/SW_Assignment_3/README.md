# Software Assignment 3: Delay-Optimized Gate Packing

This assignment extends the previous gate-packing problems by adding timing.
Each gate now has an intrinsic delay, every wire has a delay per unit length, and
the objective is to place gates so that the circuit's critical path delay is
minimized.

The final implementation combines randomized non-overlapping gate placement with
a dynamic programming pass over the circuit DAG to compute the critical path for
each candidate packing. A simulated annealing prototype is also present in the
codebase, but the submitted driver primarily uses randomized multi-start search:
generate many valid packings within a time budget, evaluate each with DP, and
retain the packing with the lowest critical-path delay.

## Problem

Each testcase describes:

- rectangular gates with width, height, and gate delay,
- input and output pins on gate boundaries,
- a global wire delay per unit length,
- directed pin-level wires between gate output pins and gate input pins.

The output must include:

```text
bounding_box <width> <height>
critical_path <pin sequence from primary input to primary output>
critical_path_delay <delay>
g1 <x> <y>
g2 <x> <y>
...
```

The circuit is assumed to be combinational. Before solving, the implementation
checks for combinational loops and rejects invalid cases with multiple drivers for
the same input pin.

## Objective

For any path from a primary input to a primary output:

```text
path_delay = sum(gate_delays) + wire_delay * sum(wire_group_lengths)
```

The critical path delay is the maximum delay over all primary-input to
primary-output paths. The placement objective is to minimize that maximum delay.

Wire length is estimated using the assignment's semi-perimeter method. When one
output pin fans out to multiple input pins, the implementation treats that fanout
as a `Wire_Group` and uses the bounding box of the full group.

## Core Approach

The solution has two main phases.

### 1. Generate a Legal Packing

The implementation uses envelope-based packing, inherited from earlier
assignments:

1. Compute an envelope size from the maximum gate width and height.
2. Assign each gate to a unique envelope in a square grid.
3. Place the gate inside the envelope.
4. Randomize the gate order to generate different legal packings.

Because envelopes do not overlap and each gate stays inside its own envelope,
gate overlap is avoided without doing expensive geometric collision checks.

Tradeoff: the bounding box is larger than a tightly packed layout, but legality is
simple and each candidate packing can be evaluated quickly.

### 2. Compute Critical Path by Dynamic Programming

For each packing, the code initializes wire groups and then computes the longest
path delay through the directed acyclic gate graph.

The DP state for each gate stores:

- the previous gate on the best path,
- the input pin used to enter the gate,
- the previous wire group,
- the best delay from any primary input to this gate,
- the current path length.

For a gate `v`, the recurrence considers each predecessor `u`:

```text
best_delay[v] =
    gate_delay[v] + max(best_delay[u] + wire_delay * wire_group_length(u, v))
```

Primary-input gates are base cases. After computing DP states, the code checks
primary-output gates and reconstructs the pin-level critical path by following the
stored predecessor information.

## Data Model

| Class | Role |
|---|---|
| `dp_state` | Stores the best predecessor, entering pin, wire group, delay, and path length for DP. |
| `Heap` | Generic heap used by wire groups to track min/max pin coordinates efficiently. |
| `Gate_Env` | Represents a gate, delay, pins, envelope coordinates, global coordinates, and DP state. |
| `Pin` | Represents an input or output pin, global coordinate access, and directed pin connections. |
| `Wire_Group` | Represents fanout from one output pin to connected input pins; maintains bounding-box extrema. |
| `Gate_Data` | Stores the full netlist, DAGs, primary IO sets, wire groups, packing, and critical path result. |
| `simulated_annealing` | Prototype perturbation-based optimizer retained in `oops.py`; not the main submitted driver. |

This separation keeps timing logic, geometric placement, wire-group accounting,
and input/output parsing reasonably isolated.

## Algorithmic Decisions

### Directed DAG Representation

SW3 needs timing direction, unlike SW2's mostly undirected wire-length objective.
The parser stores both pin-level and gate-level directed graphs:

- `wire_dag_from_to` and `wire_dag_to_from` for pin-level connectivity,
- `gate_dag_from_to` and `gate_dag_to_from` for gate-level DP transitions.

This makes primary input/output detection and predecessor lookup direct.

### Loop and Multiple-Input Validation

The assignment assumes a combinational circuit. `Loop_Pin_Check` detects cycles
before solving. It also checks that an input pin does not receive multiple incoming
wires. Invalid cases are stopped early instead of producing meaningless timing
data.

### Wire Groups for Fanout

If an output pin drives multiple input pins, the signal is assumed to arrive at all
destinations simultaneously. The implementation models this with `Wire_Group`,
which stores all pins in the fanout group and computes the semi-perimeter length
from coordinate extrema.

For each pair of connected gates, the DP transition uses the maximum relevant
wire-group length between them. This keeps timing calculation compact while
respecting fanout delay.

### Randomized Multi-Start Search

The final driver repeatedly generates different randomized packings and evaluates
their critical path. It runs until the global time budget is nearly exhausted:

```text
TIME_BOUND_TOTAL_SEC = 30
TIME_BOUND_BUFFER_SEC = 3
```

This simple strategy works well because a single packing evaluation is relatively
fast, especially compared with searching the full placement space exactly.

### Simulated Annealing Prototype

The file `oops.py` also contains a `simulated_annealing` class with swap/move
perturbations and an acceptance-probability function. This mirrors the SW2
optimization style, but it is not the main path used by `main.py` for the final
submitted execution.

The practical choice was to favor many independent randomized packings plus a
fast DP evaluator. That avoids the overhead of repeatedly updating and restoring
state after local perturbations.

## Complexity Notes

Let:

- `G` = number of gates,
- `P` = number of pins,
- `W` = number of wires.

| Operation | Cost |
|---|---:|
| Generate one envelope packing | `O(G)` |
| Initialize wire groups | `O(W)` |
| Identify primary input/output pins | `O(P)` |
| Compute DP states over the gate DAG | approximately `O(G + E_g)` |
| Reconstruct critical path | proportional to critical-path length |

The report summarizes the practical single-packing cost as approximately
`O(P + G + W)`. Empirically, runtime grows roughly linearly as wires, pins, and
gates are varied independently.

## Metrics

### Moodle Testcases

| Test case | Gates | Pins | Wires | Initial delay | Final delay | Runtime |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 6 | 16 | 6 | 96 | 66 | 27.00 s |
| 2 | 5 | 13 | 5 | 227 | 125 | 27.00 s |

### Self-Generated Simulation Cases

| Test case | Initial delay | Final delay | Avg single run | Iterations |
|---:|---:|---:|---:|---:|
| 1 | 13851 | 11664 | 0.0040 s | 6717 |
| 2 | 62278 | 59795 | 0.0149 s | 1814 |
| 3 | 333882 | 306150 | 0.0756 s | 358 |
| 4 | 767233 | 728823 | 0.1751 s | 155 |
| 5 | 881552 | 847698 | 0.1630 s | 166 |

### Larger Attached Stress Runs

| Gates | Pins | Wires | Initial delay | Final delay | Runtime | Iterations |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 5699 | 2000 | 87900 | 81404 | 27.09 s | 358 |
| 200 | 9561 | 2000 | 166252 | 154959 | 27.18 s | 271 |
| 300 | 15286 | 2000 | 230220 | 219063 | 27.26 s | 192 |
| 400 | 20370 | 2000 | 324370 | 291704 | 27.34 s | 160 |
| 500 | 24535 | 2000 | 352255 | 312729 | 27.35 s | 147 |
| 600 | 26189 | 2000 | 367344 | 330513 | 27.48 s | 112 |

The logs also include 1000-gate experiments with up to roughly 38000 pins and
10000 wires. As instance size grows, each evaluation becomes slower, so the
number of randomized packings tested within the same time budget drops.

## Relevant Repository Layout

Only the final submission and useful analysis artifacts are listed here. Branch
experiments, caches, and duplicate working folders are intentionally omitted.

```text
SW_Assignment_3/
+-- Misc/
|   +-- COL215_SW_3.pdf
+-- 2023CS10106_2023CS50334/
|   +-- Assignment_Report/
|   |   +-- COL215_SW_Assignment_3_2023CS10106_2023CS50334.pdf
|   +-- Code/
|   |   +-- main.py
|   |   +-- oops.py
|   |   +-- utils.py
|   |   +-- visualization.py
|   |   +-- input.txt
|   |   +-- output.txt
|   |   +-- report.txt
|   +-- Test_Cases/
|       +-- TC_Moodle/
|       +-- TC_Sim/
+-- Files/
    +-- Test_Case_Reports/
        +-- TC_Attached/
        +-- TC_Moodle/
```

Important files:

| File | Role |
|---|---|
| `Misc/COL215_SW_3.pdf` | Original assignment statement |
| `2023CS10106_2023CS50334/Assignment_Report/COL215_SW_Assignment_3_2023CS10106_2023CS50334.pdf` | Final report with design, complexity analysis, and sample outputs |
| `2023CS10106_2023CS50334/Code/main.py` | Parser, validator, randomized search loop, output writer |
| `2023CS10106_2023CS50334/Code/oops.py` | Gate, pin, wire-group, heap, DP, and prototype annealing classes |
| `2023CS10106_2023CS50334/Code/utils.py` | Constants, timing wrapper, testcase generation, helper functions |
| `2023CS10106_2023CS50334/Test_Cases/TC_Sim/` | Self-generated testcase reports |
| `Files/Test_Case_Reports/TC_Attached/` | Larger stress-test reports |

## Running the Submitted Code

The submitted entry point is:

```text
2023CS10106_2023CS50334/Code/main.py
```

Expected workflow:

1. Put the testcase in `input.txt`.
2. Update `FP_IN`, `FP_OUT`, and `FP_REPORT` in `utils.py` to match the local
   file paths.
3. Run:

```bash
cd "2023CS10106_2023CS50334/Code"
python main.py
```

The program writes:

- `output.txt` with bounding box, critical path, critical path delay, and gate
  coordinates,
- `report.txt` with netlist, pin, wire-group, and primary IO details.

Note: the submitted `utils.py` contains original Windows-style paths and a typo
in the submitted directory name inside those path constants, so local paths should
be corrected before rerunning.

## What This Demonstrates

- Timing-aware gate placement with gate delays, wire delays, and fanout groups.
- Dynamic programming over a combinational circuit DAG to compute critical path.
- Custom abstractions for gates, pins, wire groups, heaps, and DP states.
- Randomized multi-start optimization under a fixed runtime budget.
- Validation of circuit assumptions before optimization.
- Empirical scaling analysis across gates, pins, and wires.

## Authors

Yash Rawat (`2023CS50334`) and Priyanshi Gupta (`2023CS10106`)  
COL215, Semester I 2024-25, IIT Delhi
