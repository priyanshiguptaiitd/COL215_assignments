## COL215 (24-25 Sem I) Software Assignments

This directory contains the Software assignment submissions

## Brief Descriptions of Assignments

### SW Assignment 1 - Rectangular Gate Packing

Automatic generation of a compact physical layout of a gate-level circuit.
Assume that all gates are rectangular, and the final layout is also rectangular. In a compact layout, blank space is minimized. The input to the program is a list of gates with their positions and sizes. The output is the final layout of the circuit.

### HW Assignment 2 - Wire Aware Gate Packing

The assignment built upon A1, now involving I/O pin coordinates for each gate. The input also involved "wires" connecting input pins to output pins.The output was expected to be a non-overlapping packing of gates which minimised a particular heuristic for measuring "wire-cost" of the packing. We used an approach based on simulataed annealing to generate an initial packing and achieve an optimal packing by "annealing" the packing. Analysis was done by tweaking over 5-6 parameters in order to achieve an effecient run time as well as low-cost configuration for test cases in the given bounds.

### HW Assignment 2 - Wire Aware Gate Packing

The assignment built upon A1,A2, now involving Gate Delay's and a universal Wire Delay, the expected output being a non-overlapping packing of gates that minimised the "critical-path" (Primary Input Pin to Primary Output Pin via intermediate connections) cost. A similar approach to assignment 2 was taken involving a DP based approach to calculate the maximum path delay and minimising it thereafter.
