library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity inv_row_shift is
  generic (
    S : integer := 4; -- Length of the arrays (can be changed)
    N : integer := 16  -- Length of the arrays (can be changed)
  );
  port (
    input_data : in std_logic_vector(8 * N - 1 downto 0);    -- Input array A (N x 8-bit elements)
    output_data : out std_logic_vector(8 * N - 1 downto 0)    -- Output result array (N x 8-bit elements)
  );
end inv_row_shift;

architecture Behavioral 