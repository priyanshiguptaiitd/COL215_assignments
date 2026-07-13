# COL215 Software Assignments

This directory contains the software assignments for COL215: Digital Logic and
System Design, Semester I 2024-25. The assignments build a small placement
pipeline in stages: compact gate packing, wire-aware placement, and timing-aware
critical-path optimization.

## Assignments

| Assignment | Topic | Summary |
|---|---|---|
| [SW Assignment 1](./SW_Assignment_1/README.md) | Rectangular gate packing | Packs fixed-orientation rectangular gates into a compact non-overlapping bounding box using greedy and grid-based heuristics. |
| [SW Assignment 2](./SW_Assignment_2/README.md) | Wire-aware gate placement | Extends placement with pins and wires, using simulated annealing and custom gate/pin/wire abstractions to reduce estimated wire length. |
| [SW Assignment 3](./SW_Assignment_3/README.md) | Timing-aware gate placement | Adds gate and wire delays, then uses randomized packings and dynamic programming over the circuit DAG to minimize critical-path delay. |

Each assignment directory contains its own detailed README with the problem
statement, implementation notes, tradeoffs, and relevant metrics.

## Authors

Yash Rawat (`2023CS50334`) and Priyanshi Gupta (`2023CS10106`)
