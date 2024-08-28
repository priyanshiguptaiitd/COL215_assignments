`=================================================================================================================`

# Seven Segment Decoder for Decimal Digits 

## Introduction
This VHDL code defines a seven-segment decoder that converts a 4-bit binary input into the corresponding 7-segment display output. This is typically used to display decimal digits (0-9) on a seven-segment display.

## Entity Description
The entity `seven_seg_decoder_decimal` has the following ports:
- `dec_in`: A 4-bit input vector (`std_logic_vector(3 downto 0)`) representing the binary value of the decimal digit to be displayed.
- `dec_out`: A 7-bit output vector (`std_logic_vector(6 downto 0)`) representing the segments (a to g) of the seven-segment display.

## Architecture Description
The architecture `Behavioral` contains:
- Signals `A`, `B`, `C`, and `D` which are used to represent the individual bits of the input `dec_in`.
- A process `Seg_Decoder_DEC` that is sensitive to changes in `dec_in` and computes the values for `dec_out` based on the input.

## Functionality
The process `Seg_Decoder_DEC` performs the following steps:
1. Assigns the individual bits of `dec_in` to signals `A`, `B`, `C`, and `D`.
2. Computes the values for each segment of the seven-segment display (`dec_out(0)` to `dec_out(6)`) using logical expressions.
3. The logical expressions are derived from Karnaugh maps and are designed to produce the correct segment outputs for displaying decimal digits 0-9.
4. The Basys 3 board uses active low pins, so the segment values are inverted.

## Notes
- The seven-segment display is configured for active low operation, meaning a segment is illuminated when the corresponding output bit is `0`.
- The logical expressions for each segment are optimized using the Sum of Min terms method.

This VHDL code is useful for applications where a binary-coded decimal input needs to be displayed on a seven-segment display, such as digital clocks, calculators, and other numeric displays.

`=================================================================================================================`

# Seven Segment Decoder for Hexadecimal Digits 

## Introduction
This VHDL code defines a seven-segment decoder that converts a 4-bit binary input into the corresponding 7-segment display output. This is typically used to display hexadecimal digits (0-9, A-F) on a seven-segment display.

## Entity Description
The entity `seven_seg_decoder_hex` has the following ports:
- `dec_in`: A 4-bit input vector (`std_logic_vector(3 downto 0)`) representing the binary value of the hexadecimal digit to be displayed.
- `dec_out`: A 7-bit output vector (`std_logic_vector(6 downto 0)`) representing the segments (a to g) of the seven-segment display.

## Architecture Description
The architecture `Behavioral` contains:
- Signals `A`, `B`, `C`, and `D` which are used to represent the individual bits of the input `dec_in`.
- A process `Seg_Decoder_HEX` that is sensitive to changes in `dec_in` and computes the values for `dec_out` based on the input.

## Functionality
The process `Seg_Decoder_HEX` performs the following steps:
1. Assigns the individual bits of `dec_in` to signals `A`, `B`, `C`, and `D`.
2. Computes the values for each segment of the seven-segment display (`dec_out(0)` to `dec_out(6)`) using logical expressions.
3. The logical expressions are derived from Karnaugh maps and are designed to produce the correct segment outputs for displaying hexadecimal digits 0-9 and A-F.
4. The Basys 3 board uses active low pins, so the segment values are inverted.

## Notes
- The seven-segment display is configured for active low operation, meaning a segment is illuminated when the corresponding output bit is `0`.
- The logical expressions for each segment are optimized using the Sum of Min terms method.

This VHDL code is useful for applications where a binary-coded hexadecimal input needs to be displayed on a seven-segment display, such as digital clocks, calculators, and other numeric displays.

`=================================================================================================================`

# MUX_4BIT 

## Introduction
This VHDL code defines a 4-bit multiplexer (MUX) that selects one of four 4-bit input data lines based on a 2-bit select signal. The selected data is then output.

## Entity Description
The entity `MUX_4BIT` has the following ports:
- `mux_s`: A 2-bit input vector (`std_logic_vector(1 downto 0)`) representing the select signal.
- `mux_d0`: A 4-bit input vector (`std_logic_vector(3 downto 0)`) representing the first data input.
- `mux_d1`: A 4-bit input vector (`std_logic_vector(3 downto 0)`) representing the second data input.
- `mux_d2`: A 4-bit input vector (`std_logic_vector(3 downto 0)`) representing the third data input.
- `mux_d3`: A 4-bit input vector (`std_logic_vector(3 downto 0)`) representing the fourth data input.
- `mux_out_to`: A 4-bit output vector (`std_logic_vector(3 downto 0)`) representing the selected data output.

## Architecture Description
The architecture `Behavioral` contains:
- A process `MUX_Process` that is sensitive to changes in the select signal (`mux_s`) and the data inputs (`mux_d0`, `mux_d1`, `mux_d2`, `mux_d3`).

## Functionality
The process `MUX_Process` performs the following steps:
1. Monitors the select signal `mux_s`.
2. Based on the value of `mux_s`, it assigns the corresponding data input (`mux_d0`, `mux_d1`, `mux_d2`, `mux_d3`) to the output `mux_out_to`.
3. If `mux_s` does not match any of the specified cases, it defaults the output `mux_out_to` to "0000".

## Notes
- This multiplexer can be used in digital circuits where multiple data sources need to be routed to a single destination based on a select signal.
- It is commonly used in data routing, signal selection, and control applications.
- Ensure that the VHDL code is properly compiled and simulated using a VHDL simulator like ModelSim.

`=================================================================================================================`

# Timing Circuit

This VHDL module implements a timing circuit that divides a 100 MHz input clock to generate a slower clock signal, and uses this clock to control a multiplexer and anode signals for a display.

## Entity: Timing_block

### Ports
- `clk_in` : `in STD_LOGIC`
  - 100 MHz input clock
- `reset` : `in STD_LOGIC`
  - Reset signal (resets the internal signals to known states)
- `mux_select` : `out STD_LOGIC_VECTOR (1 downto 0)`
  - Signal for the multiplexer
- `anodes_tout` : `out STD_LOGIC_VECTOR (3 downto 0)`
  - Anodes signal for display

## Architecture: Behavioral

### Constants
- `N : integer := 511`
  - Counter limit for clock division (needs to be selected correctly)

### Signals
- `counter : integer := 0`
  - Counter for clock division
- `mux_select_counter : STD_LOGIC_VECTOR (1 downto 0) := "00"`
  - Counter for multiplexer selection
- `new_clk : STD_LOGIC := '0'`
  - Divided clock signal

### Processes

#### 1. Clock Division Process
- **Name**: `NEW_CLK`
- **Sensitivity List**: `clk_in, reset`
- **Function**:
  - Divides the 100 MHz input clock to generate a slower clock signal.
  - Resets the counter and `new_clk` signal when `reset` is high.
  - Toggles `new_clk` when the counter reaches `N`.

#### 2. Multiplexer Select Signal Process
- **Name**: `MUX_select`
- **Sensitivity List**: `new_clk, reset`
- **Function**:
  - Controls the multiplexer selection signal.
  - Resets the `mux_select_counter` when `reset` is high.
  - Increments `mux_select_counter` on the rising edge of `new_clk`.

#### 3. Anode Signal Process
- **Name**: `ANODE_select`
- **Sensitivity List**: `mux_select`
- **Function**:
  - Controls the anode signals for the display based on the `mux_select` signal.
  - Sets `anodes_tout` to different values depending on the value of `mux_select`.

## Notes
- The clock division process generates a clock with a period of 10.24 ms or a frequency of 97.65625 Hz.
- The multiplexer select signal cycles through the values "00", "01", "10", and "11".
- The anode signals are set to "1110", "1101", "1011", and "0111" based on the multiplexer select signal.

`=================================================================================================================`
# 7-Segment Display Controller

This VHDL module implements a 7-segment display controller that takes a 100 MHz input clock and four 4-bit binary inputs, and drives a 4-digit 7-segment display.

## Entity: display_seven_seg

### Ports
- `clock_in` : `in STD_LOGIC`
  - 100 MHz input clock
- `reset_timer` : `in STD_LOGIC`
  - Reset signal (resets the internal signals to known states)
- `d0` : `in STD_LOGIC_VECTOR(3 downto 0)`
  - 4-bit binary input for the first digit
- `d1` : `in STD_LOGIC_VECTOR(3 downto 0)`
  - 4-bit binary input for the second digit
- `d2` : `in STD_LOGIC_VECTOR(3 downto 0)`
  - 4-bit binary input for the third digit
- `d3` : `in STD_LOGIC_VECTOR(3 downto 0)`
  - 4-bit binary input for the fourth digit
- `an` : `out STD_LOGIC_VECTOR(3 downto 0)`
  - Anodes signal for the display
- `seg` : `out STD_LOGIC_VECTOR(6 downto 0)`
  - Cathodes signal for the display

## Architecture: Behavioral

### Components

#### 1. Timing_block
- **Ports**:
  - `clk_in` : `in STD_LOGIC`
    - 100 MHz input clock
  - `reset` : `in STD_LOGIC`
    - Reset signal (resets the internal signals to known states)
  - `mux_select` : `out STD_LOGIC_VECTOR(1 downto 0)`
    - Signal for the multiplexer
  - `anodes_tout` : `out STD_LOGIC_VECTOR(3 downto 0)`
    - Anodes signal for the display

#### 2. seven_seg_decoder_decimal
- **Ports**:
  - `dec_in` : `in STD_LOGIC_VECTOR(3 downto 0)`
    - 4-bit binary input
  - `dec_out` : `out STD_LOGIC_VECTOR(6 downto 0)`
    - 7-segment display output

#### 3. MUX_4BIT
- **Ports**:
  - `mux_s` : `in STD_LOGIC_VECTOR(1 downto 0)`
    - Multiplexer select signal
  - `mux_d0` : `in STD_LOGIC_VECTOR(3 downto 0)`
    - 4-bit binary input for the first digit
  - `mux_d1` : `in STD_LOGIC_VECTOR(3 downto 0)`
    - 4-bit binary input for the second digit
  - `mux_d2` : `in STD_LOGIC_VECTOR(3 downto 0)`
    - 4-bit binary input for the third digit
  - `mux_d3` : `in STD_LOGIC_VECTOR(3 downto 0)`
    - 4-bit binary input for the fourth digit
  - `mux_out_to` : `out STD_LOGIC_VECTOR(3 downto 0)`
    - Multiplexer output

### Signals
- `mux_sel` : `STD_LOGIC_VECTOR(1 downto 0)`
  - Multiplexer select signal
- `mux_out_dec` : `STD_LOGIC_VECTOR(3 downto 0)`
  - Multiplexer output

### Processes

#### 1. Timer_Block
- **Function**:
  - Instantiates the `Timing_block` component.
  - Maps the input clock and reset signals to the component.
  - Outputs the multiplexer select signal and anodes signal.

#### 2. MUX_Block
- **Function**:
  - Instantiates the `MUX_4BIT` component.
  - Maps the multiplexer select signal and 4-bit binary inputs to the component.
  - Outputs the selected 4-bit binary input.

#### 3. Decoder_Block
- **Function**:
  - Instantiates the `seven_seg_decoder_decimal` component.
  - Maps the multiplexer output to the decoder input.
  - Outputs the 7-segment display signals.

## Notes
- The `Timing_block` component generates a slower clock signal from the 100 MHz input clock.
- The `MUX_4BIT` component selects one of the four 4-bit binary inputs based on the multiplexer select signal.
- The `seven_seg_decoder_decimal` component converts the 4-bit binary input to the corresponding 7-segment display output.

`=================================================================================================================`

# Made by 2023CS50334 