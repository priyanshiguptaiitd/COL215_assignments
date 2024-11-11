library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Accepts 4 Bytes of input data and shifts the bytes by a given amount


entity AES_ShiftRows is
  generic (
    S : integer := 4 -- Number of Bytes in a row
  );
  port (
    en : in std_logic;
    input_data : in std_logic_vector(8 * S - 1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
    shift_bytes : in integer; -- Number of bytes to shift (Must lie from 0 to S-1)
    output_data : out std_logic_vector(8 * S - 1 downto 0) -- Output result array (16 bytes)
  );
end AES_ShiftRows;

architecture inv_row_shift of AES_ShiftRows is
begin
  process (en, input_data, shift_bytes)
  begin
    if en = '1' then
      output_data <= input_data(8 * ((shift_bytes mod S)) - 1 downto 0) & 
                     input_data(8 * S - 1 downto 8 * (shift_bytes mod S));
    end if;
  end process;
end inv_row_shift;
