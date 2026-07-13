# Hardware Assignment 2: 4-Digit Seven-Segment Display Controller

This assignment implements a complete 4-digit hexadecimal display controller for the Basys 3 FPGA board. The design takes four 4-bit inputs from the board switches, selects one digit at a time using a 4:1 multiplexer, decodes the selected hexadecimal digit into seven-segment cathode signals, and cycles through the four display anodes fast enough that all digits appear continuously lit.

The assignment is a useful step beyond single-output combinational circuits: it combines minimized Boolean logic, module composition, clock division, reset handling, board constraints, simulation, synthesis, and hardware validation.

## Problem Statement

The goal was to design a circuit that:

1. Accepts a 4-bit hexadecimal or decimal digit and generates the corresponding 7-bit seven-segment output.
2. Extends the decoder to drive all four seven-segment displays on the Basys 3 board.
3. Uses the shared cathode bus correctly by time-multiplexing the active anode.
4. Divides the onboard 100 MHz clock to a practical display refresh rate.
5. Produces VHDL source files, testbenches, constraints, bitstream, report, and resource utilization data.

## Architecture

The final top-level design is `display_seven_seg`, which connects three main modules:

| Module | Role |
| --- | --- |
| `MUX_4BIT.vhd` | Selects one of four 4-bit switch inputs based on the timing circuit's 2-bit select signal. |
| `seven_seg_decoder_hex.vhd` | Converts the selected 4-bit hexadecimal digit into active-low seven-segment cathode signals. |
| `timing_circuit.vhd` | Divides the 100 MHz board clock, cycles the mux select lines, and activates one anode at a time. |
| `7Seg_Display.vhd` | Top-level wrapper connecting the mux, decoder, timing block, switch inputs, anodes, and cathodes. |

The display pipeline is:

```text
16 board switches -> 4x1 digit mux -> hex decoder -> shared cathodes
100 MHz clock -----> timing block ----> mux select + active-low anodes
```

## Design and Hardware Decisions

| Decision | Rationale | Tradeoff |
| --- | --- | --- |
| Hexadecimal decoder instead of decimal-only decoder | Uses all 16 possible 4-bit inputs and displays `0`-`F`. | Requires a larger truth table and more minimized expressions than decimal-only BCD. |
| Karnaugh-map minimized segment logic | Matches the assignment requirement to derive combinational logic rather than using a lookup-style decoder. | The resulting Boolean expressions are less immediately readable than a `case` table. |
| Active-low segment outputs | Matches the Basys 3 seven-segment hardware, where cathodes and anodes are active low. | Logic must be inverted carefully to avoid reversed display behavior. |
| Time-multiplexed four-digit display | Uses the board's shared cathode lines while still displaying four independent digits. | Requires a refresh/timing circuit; too slow causes flicker, too fast can make debugging harder. |
| Separate timing, mux, and decoder modules | Keeps the design modular and easy to simulate at component level. | Adds integration complexity in the wrapper module. |
| Explicit reset behavior | Places counters and anodes into known states on reset. | Consumes an additional button input and reset path in the design. |

## Timing Strategy

The Basys 3 provides a 100 MHz clock, but the four displays must be refreshed at a human-visible rate. The timing circuit uses a counter to generate a slower internal clock, then increments a 2-bit mux/anode select counter on that divided clock.

In the updated submission, `timing_circuit.vhd` uses:

```vhdl
constant N : integer := 256000;
```

With the implemented toggle-and-rising-edge structure, this produces a mux-select step of roughly 5.12 ms from the 100 MHz input clock. The select counter cycles through `00`, `01`, `10`, and `11`, and the anode outputs cycle through the active-low patterns:

| Select | Active-Low Anode Pattern |
| --- | --- |
| `00` | `1110` |
| `01` | `1101` |
| `10` | `1011` |
| `11` | `0111` |

This lets the physical display show one digit at a time while persistence of vision makes the four digits appear stable together.

## Verification

The design was validated through:

1. **Truth-table and K-map derivation:** Segment equations were derived for hexadecimal digits `0` through `F`.
2. **Module-level simulation:** Testbenches exercise the mux, decoder, timing circuit, and top-level display controller.
3. **Vivado synthesis and schematics:** The synthesized design was checked through Vivado-generated schematic and utilization output.
4. **Board execution:** The bitstream was tested on the Basys 3 board using 16 switches for the four input digits and the four seven-segment displays as output.

## Resource Utilization

Vivado utilization report for top-level design `display_seven_seg` on `xc7a35tcpg236-1`:

| Resource | Used | Available | Utilization |
| --- | ---: | ---: | ---: |
| Slice LUTs | 52 | 20,800 | 0.25% |
| Slice Registers | 35 | 41,600 | 0.08% |
| Block RAM Tiles | 0 | 50 | 0.00% |
| DSPs | 0 | 90 | 0.00% |
| Bonded IOBs | 29 | 106 | 27.36% |
| BUFGCTRL | 1 | 32 | 3.13% |

The main FPGA cost comes from the minimized decoder logic, clock-divider counter, select counter, and board I/O. The design uses no BRAM or DSP blocks, which is expected for a small display controller.

## Repository Guide

| Path | Description |
| --- | --- |
| [`Misc/COL215_HW_Assignment_2.pdf`](./Misc/COL215_HW_Assignment_2.pdf) | Original assignment statement. |
| [`Report/Ver/COL215_HW_Assignment_2_2023CS50334_2023CS10106_Draft_Ver_1_5.pdf`](./Report/Ver/COL215_HW_Assignment_2_2023CS50334_2023CS10106_Draft_Ver_1_5.pdf) | Detailed report with truth table, K-map reductions, design explanation, simulation snapshots, board outputs, and utilization evidence. |
| [`Updated_Sub`](./Updated_Sub) | Updated source files, constraint file, bitstream, and timing/testbench snapshots. |
| [`HW_Assignment_Final_Files_Vivado`](./HW_Assignment_Final_Files_Vivado) | Vivado-oriented final bundle with VHDL files, constraints, bitstream, utilization report, simulation snapshots, schematics, and board photos. |
| [`HW_Assignment_2_Files/HW_2_Final_sub`](./HW_Assignment_2_Files/HW_2_Final_sub) | Earlier final-submission mirror retained for reference. |

Older draft folders, reference PDFs, generated tables, and previous submissions are not needed to understand or reproduce the final design.

## Reproducing the Design

1. Open Vivado 2022.1 or a compatible version.
2. Create a project for the Basys 3 target device `xc7a35tcpg236-1`.
3. Import the VHDL files from `Updated_Sub` or `HW_Assignment_Final_Files_Vivado`.
4. Set `display_seven_seg` as the top-level module.
5. Import `basys3_7SegD.xdc` for the switch, clock, reset, cathode, and anode pin mappings.
6. Run behavioral simulation using the included testbenches.
7. Run synthesis, implementation, and bitstream generation.
8. Program the Basys 3 board and test four hexadecimal digits using the 16 slide switches.

## Authors

- Yash Rawat (`2023CS50334`)
- Priyanshi Gupta (`2023CS10106`)
