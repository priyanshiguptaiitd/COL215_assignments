## COL215 (24-25 Sem I) Hardware Assignments

This directory contains the Hardware assignment submissions

## Brief Descriptions of Assignments

### HW Assignment 1 - 2x1 and 4x1 MUX on Basys 3 Board

Implementing basic gates (AND/OR/NOT) using VHDL on FPGA board.
Combining gate instances to create a 2x1 MUX and then recursively 
to implement a 4x1 MUX

### HW Assignment 2 - 4 Digit Seven Segment Display

Design a combinational circuit that takes a single 4-bit hexadecimal or decimal digit
input from the switches and produces a 7-bit output for the seven-segment display
of Basys 3 FPGA board. Extend the design to create a circuit that drives all 4
displays for displaying 4 digits together.

### HW Assignment 3 - AES Decryption on FPGA

#### This assignment divided into two parts : #####

Part 1 Involved designing the modular components for AES Decryption Operations (Shift_Rows, Inverse_Mix_Columns, etc.) The design was kept generic so that it can be reused depending upon future implementation. This assignment also expected us to make our own ROM and RAM implementations inorder to store temporary calculation data and fetch data for Inv_Sub_Bytes operation which was done using onboard BRAM and LUT's on board ( Block Mem Generation & Dist. Mem Generation )

Part 2 involved making an control module and use an FSM based approach to design the final circuit logic, decrypting 128 bit inputs at a time and decoding the ascii output to make a scrolling display on 7 Segment Display
          


