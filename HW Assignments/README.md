# COL215 Hardware Assignments

This directory contains the hardware assignments for COL215, focused on VHDL-based digital design, FPGA implementation on the Basys 3 board, simulation, synthesis, and board-level validation.

The assignments progress from basic combinational circuits to display controllers and finally to an AES decryption datapath with memory-backed lookup tables and a scrolling seven-segment output.

## Assignments

| Assignment | Topic | Highlights |
| --- | --- | --- |
| [HW Assignment 1](./HW_Assignment_1/README.md) | Structural multiplexers on Basys 3 | Basic gates, structural VHDL, 2x1 and 4x1 mux design, simulation, bitstream generation, and resource utilization. |
| [HW Assignment 2](./HW_Assignment_2/README.md) | 4-digit seven-segment display controller | K-map minimized hex decoder, 4:1 digit mux, clock-divider timing circuit, active-low anode/cathode control, and board testing. |
| [HW Assignment 3](./Hardware_Assignment_3/README.md) | AES decryption on FPGA | AES inverse transformations, FSM controller, ROM/RAM-backed data lookup, GF(2^8) arithmetic, and scrolling plaintext display. |

## Repository Notes

- `HW_Assignment_1` and `HW_Assignment_2` contain the assignment-specific documentation and final artifacts for the first two hardware assignments.
- `Hardware_Assignment_3` contains the cleaned HW3 implementation and is the recommended entry point for the AES decryption assignment.
- `HW_Assignment_3` is retained as the older HW3 submission/archive tree with reports, snapshots, and submitted mirrors.
- `Basys_3` contains board-related reference material.

## Authors

Yash Rawat (`2023CS50334`) and Priyanshi Gupta (`2023CS10106`)
