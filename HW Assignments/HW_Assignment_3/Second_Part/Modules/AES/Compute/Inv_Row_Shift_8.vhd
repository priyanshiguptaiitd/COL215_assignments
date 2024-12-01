library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity inv_row_shift is
  generic (
    S : integer := 4; -- Number of Bytes in a row
  ); 

  port (
    input_data : in std_logic_vector(8 * S - 1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
    shift_bytes : in integer; -- Number of bytes to shift
    output_data : out std_logic_vector(8 * S - 1 downto 0) -- Output result array (16 bytes)
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

begin

  -- Apply the inverse row shift to the input data and assign to output
  output_data <= mux_shift(shift_bytes,input_data);

end Behavioral;
