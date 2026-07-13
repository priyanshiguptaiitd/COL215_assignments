# Hardware Assignment 3: AES Decryption on Basys 3

This assignment implements an FPGA-oriented AES decryption pipeline for the Basys 3 board. Given ciphertext and precomputed round keys, the design reconstructs plaintext through inverse AES transformations and routes the final 128-bit result to a scrolling four-digit seven-segment display.

The repository contains both the original deadline-era submission and a cleaner rewrite. For understanding the final implementation, use `New_Code` as the main source tree. The older `Existing_Code` and sibling `../HW_Assignment_3` directories are useful historical references, reports, screenshots, and submitted artifacts, but they include drafts and intermediate experiments.

## Problem Statement

The assignment asked for an AES decryption unit built from FPGA memory and logic blocks:

1. Store ciphertext, round keys, and lookup tables using memory modules.
2. Implement the inverse AES operations required for decryption.
3. Coordinate the decryption sequence using a controller/FSM.
4. Display the resulting plaintext on the Basys 3 seven-segment display.

The assignment handout used an AES-128-style 128-bit state and provided round keys through memory initialization files, so the hardware did not need to implement key expansion.

## Implementation Overview

The cleaned implementation is organized into three layers:

| Layer | Location | Responsibility |
| --- | --- | --- |
| AES compute datapath | [`New_Code/AES/Compute`](./New_Code/AES/Compute) | AES inverse transformations, round controller, top-level controller, debug/test helpers. |
| Memory modules | [`New_Code/Memory/Modules`](./New_Code/Memory/Modules) | Generic RAM and ROM wrappers for ciphertext, keys, text, and inverse S-box lookup tables. |
| Display pipeline | [`New_Code/AES/Display`](./New_Code/AES/Display) | ASCII-to-seven-segment conversion, byte muxing, timing, and scrolling output display. |

At a high level:

```text
Ciphertext ROM + Round-key ROM + Inv-SBOX ROM
                    |
                    v
            AES_Controller FSM
                    |
        inverse AES round modules
                    |
                    v
          128-bit plaintext result
                    |
                    v
      scrolling seven-segment display
```

## Core Modules

| Module | Role |
| --- | --- |
| `AES_Controller.vhd` | Top-level decryption controller. Loads text/key bytes, applies initial/final AddRoundKey stages, invokes round logic, and drives display output signals. |
| `AES_Round.vhd` | Implements one inverse AES round using AddRoundKey, InvMixColumns, InvShiftRows, and InvSubBytes. |
| `AES_AddRoundKey.vhd` | Byte-level XOR block used for AddRoundKey. |
| `AES_ShiftRows.vhd` | Implements inverse row shifting by rotating each row by the required byte offset. |
| `AES_SubBytes.vhd` | Performs inverse S-box lookup through `ROM_SBOX`. |
| `AES_MixColumns.vhd` | Implements inverse MixColumns by combining GF(2^8) multiplications with XOR reduction. |
| `AES_GF_256.vhd` | GF(2^8) multiplier using the AES irreducible polynomial `0x11B`. |
| `AES_Key.vhd` | Reads precomputed round-key bytes from key ROM. |
| `AES_Text.vhd` | Reads text/ciphertext bytes from text ROM. |
| `AES_FDisplay.vhd` / `AES_Display.vhd` | Wrappers connecting the AES controller to the seven-segment display pipeline. |

## Design and Hardware Decisions

| Decision | Rationale | Tradeoff |
| --- | --- | --- |
| FSM-driven AES controller | Makes a multi-stage decryption process manageable on FPGA hardware. | More control-state complexity than a single combinational datapath. |
| Byte-serial processing for key/text/SubBytes/AddRoundKey | Reduces duplicated hardware and keeps the design closer to available board resources. | Increases latency because 128-bit state operations are assembled byte by byte. |
| ROM-backed key, text, and S-box data | Matches the assignment requirement to use FPGA memory elements and COE-initialized data. | Reproduction requires Vivado distributed-memory IP blocks with matching names. |
| GF(2^8) multiplication in VHDL | Keeps InvMixColumns portable and transparent instead of relying on a black-box multiplier. | Consumes LUT logic; no DSPs are used. |
| Separate compute, memory, and display folders | Makes the system easier to reason about despite the assignment's large scope. | Integration requires careful project setup in Vivado. |
| Reused HW2 display ideas | Builds on the earlier seven-segment controller and adds scrolling ASCII output. | The display path supports hex-style ASCII cleanly and falls back to a dash for unsupported characters. |

## AES Decryption Flow

The controller applies AES decryption as a sequence of smaller hardware operations:

1. Fetch the initial 128-bit ciphertext block from text memory.
2. Fetch the appropriate 128-bit round key from key memory.
3. Apply AddRoundKey using byte-wise XOR.
4. For intermediate rounds, apply inverse MixColumns, inverse ShiftRows, inverse SubBytes, and AddRoundKey.
5. For the final round, skip inverse MixColumns and apply the final AddRoundKey stage.
6. Forward the 128-bit plaintext result to the display pipeline.

The design uses precomputed round keys, so the hardware focuses on decryption datapath control rather than key schedule generation.

## Display Pipeline

The display module treats the 128-bit result as 16 ASCII bytes and scrolls four bytes at a time across the Basys 3 seven-segment displays.

| Module | Function |
| --- | --- |
| `display_seven_seg.vhd` | Scrolls through the 16-byte plaintext window and coordinates display refresh. |
| `MUX_4BYTE.vhd` | Selects one of four visible bytes for the shared cathode bus. |
| `ASCII_To_Seven_Seg.vhd` | Converts ASCII `0`-`9`, `A`-`F`, and `a`-`f` into seven-segment patterns. |
| `timing_circuit.vhd` | Generates mux-select and active-low anode signals from the 100 MHz Basys 3 clock. |

Unsupported ASCII characters are displayed as a dash, which is a pragmatic choice for debugging plaintext on a four-digit seven-segment display.

## Verification

The repository includes testbenches for the important blocks:

| Testbench Area | Examples |
| --- | --- |
| AES compute | `tb_AES_Controller.vhd`, `tb_AES_Round.vhd`, `tb_AES_SubBytes.vhd`, `tb_AES_MixColumns.vhd`, `tb_AES_ShiftRows.vhd` |
| Display integration | `tb_AES_Display.vhd`, `tb_AES_Final_Display.vhd` |
| Memory lookup | `tb_ROM_Text.vhd` |
| Helper scripts | `AES_256.py`, `Dec_To_Hex.py`, `coe_writer.py` |

The older reports also include waveform snapshots for RAM/ROM access, inverse S-box lookup, XOR, inverse row shifting, inverse MixColumns, and scrolling display behavior.

## Resource Utilization

The submitted routed Vivado report for `AES_Controller` on `xc7a35tcpg236-1` reports:

| Resource | Used | Available | Utilization |
| --- | ---: | ---: | ---: |
| Slice LUTs | 3,078 | 20,800 | 14.80% |
| Slice Registers | 1,463 | 41,600 | 3.52% |
| Slices | 939 | 8,150 | 11.52% |
| Block RAM Tiles | 0 | 50 | 0.00% |
| DSPs | 0 | 90 | 0.00% |
| Bonded IOBs | 15 | 106 | 14.15% |
| BUFGCTRL | 4 | 32 | 12.50% |

The key metric is that the AES datapath fits comfortably on the Basys 3 without using DSPs or BRAM tiles in the reported build. Most resource usage comes from LUT-based AES transformations, controller state, byte counters, and display/control logic.

## Repository Guide

| Path | Description |
| --- | --- |
| [`New_Code`](./New_Code) | Cleaned implementation tree and the recommended place to start. |
| [`New_Code/AES/Compute`](./New_Code/AES/Compute) | AES datapath, controller, testbenches, XDC, and Python helpers. |
| [`New_Code/AES/Display`](./New_Code/AES/Display) | Scrolling seven-segment display logic. |
| [`New_Code/Memory/Modules`](./New_Code/Memory/Modules) | RAM/ROM wrappers and memory testbench. |
| [`New_Code/Memory/Example`](./New_Code/Memory/Example) | Example COE files and COE generation script. |
| [`Existing_Code`](./Existing_Code) | Older assignment tree retained for reference. |
| [`Part 1 report`](<../HW_Assignment_3/Submission_01/2023CS50334_2023CS10106/Report/COL215_HW3_2023CS50334_2023CS10106_01.pdf>) | First-stage report covering memory and individual AES inverse modules. |
| [`Part 2 report`](<../HW_Assignment_3/2023CS10106_2023CS50334/COL215_HW_Assignment_3_2023CS50334_2023CS10106_Part_2.pdf>) | Later report covering the integrated AES controller and display flow. |
| [`Submitted artifact mirror`](<../HW_Assignment_3/2023CS10106_2023CS50334>) | Older submitted source files, bitfile, constraints, and utilization report. |

## Reproducing the Design

1. Open Vivado 2024.1 or a compatible version.
2. Create a Basys 3 project targeting `xc7a35tcpg236-1`.
3. Add the VHDL files from `New_Code/AES/Compute`, `New_Code/AES/Display`, and `New_Code/Memory/Modules`.
4. Generate or import distributed-memory IP blocks with the names expected by the ROM wrappers:
   - `dist_mem_gen_key`
   - `dist_mem_gen_sbox`
   - `dist_mem_gen_text`
   - `dist_mem_gen_0` if using the generic ROM wrapper
5. Initialize the memory IP with the relevant COE files from `New_Code/Memory/Example` or generated test vectors.
6. Use `AES_Controller` for compute-level synthesis, or `AES_FDisplay`/`AES_Display` for display-integrated testing.
7. Add `New_Code/AES/Compute/basys3_hw3.xdc` for clock, reset, start, done LED, anode, and segment mappings.
8. Run behavioral simulation using the included testbenches before synthesis and implementation.

## Notes

- `New_Code` is the most useful implementation tree; `Existing_Code` and `../HW_Assignment_3` include drafts, snapshots, and submitted mirrors.
- Some files are experimental or backup variants, such as `AES_Control_Copy.vhd` and `AES_Round_Logic.vhd`; the main controller path is `AES_Controller.vhd` plus `AES_Round.vhd`.
- I could not run a local VHDL syntax check in this environment because `ghdl` is not installed. The README was validated against the file structure, reports, module contents, and Vivado utilization report.

## Authors

- Priyanshi Gupta (`2023CS10106`)
- Yash Rawat (`2023CS50334`)
