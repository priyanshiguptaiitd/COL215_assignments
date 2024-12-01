----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 24.10.2024 14:49:56
-- Design Name: 
-- Module Name: Inv_Row_Shift - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: Implements InvRowShift operation
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity inv_row_shift is
  generic (
    S : integer := 4; -- Number of rows (AES is 4 rows)
    N : integer := 16 -- Total number of bytes (4x4 matrix for AES = 16 bytes)
  );
  port (
    input_data : in std_logic_vector(8 * N - 1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
    output_data : out std_logic_vector(8 * N - 1 downto 0) -- Output result array (16 bytes)
  );
end inv_row_shift;

architecture Behavioral of inv_row_shift is

  -- Function to perform circular shift on a row (8*S bits = 4 bytes)
  function mux_shift(shift_val : integer; row : std_logic_vector(8*S-1 downto 0)) return std_logic_vector is
    variable shifted_row : std_logic_vector(8*S-1 downto 0); -- Correctly constrained row
    variable i : integer;
  begin
    -- Initialize with zeros
    shifted_row := (others => '0');
    
    -- Perform circular shift
    for i in 0 to S-1 loop
      shifted_row(8*i+7 downto 8*i) := row(8*((i + shift_val) mod S) + 7 downto 8*((i + shift_val) mod S));
    end loop;
    
    return shifted_row;
  end function mux_shift;

  -- Function to apply row shifts for InvRowShift (shift rows 0, 1, 2, and 3 differently)
  function row_shift (x : std_logic_vector(8*N-1 downto 0)) return std_logic_vector is
    variable shifted_data: std_logic_vector(8*N-1 downto 0); -- Output data after shifting
    variable i: integer;
  begin
    -- Initialize output with zeros
    shifted_data := (others => '0');
    
    -- Apply row shifts for AES (row 0: no shift, row 1: shift by 1, row 2: shift by 2, row 3: shift by 3)
    for i in 0 to S-1 loop
      shifted_data(8*S*(i+1)-1 downto 8*S*i) := mux_shift(S-i-1, x(8*S*(i+1)-1 downto 8*S*i));
    end loop;
    
    return shifted_data;
  end function row_shift;

begin

  -- Apply the inverse row shift to the input data and assign to output
  output_data <= row_shift(input_data);

end Behavioral;
