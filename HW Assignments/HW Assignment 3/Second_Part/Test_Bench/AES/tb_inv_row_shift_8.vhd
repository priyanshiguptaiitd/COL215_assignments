library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_inv_row_shift_8 is
end tb_inv_row_shift_8;

architecture Behavioral of tb_inv_row_shift_8 is

    -- Component declaration for the Unit Under Test (UUT)
    component inv_row_shift
        generic (
            S : integer := 4
        );
        port (
            input_data : in std_logic_vector(8 * S - 1 downto 0);
            shift_bytes : in integer;
            output_data : out std_logic_vector(8 * S - 1 downto 0)
        );
    end component;

    -- Signals to connect to the UUT
    signal input_data : std_logic_vector(8 * 4 - 1 downto 0);
    signal shift_bytes : integer;
    signal output_data : std_logic_vector(8 * 4 - 1 downto 0);

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: inv_row_shift
        generic map (
            S => 4
        )
        port map (
            input_data => input_data,
            shift_bytes => shift_bytes,
            output_data => output_data
        );

    -- Stimulus process
    stim_proc: process
    begin
        -- Test case 1
        input_data <= x"01020304";
        shift_bytes <= 1;
        wait for 10 ns;
        
        -- Test case 2
        input_data <= x"01020304";
        shift_bytes <= 2;
        wait for 10 ns;
        
        -- Test case 3
        input_data <= x"01020304";
        shift_bytes <= 3;
        wait for 10 ns;
        
        -- Test case 4
        input_data <= x"01020304";
        shift_bytes <= 4;
        wait for 10 ns;

        -- Add more test cases as needed

        -- End simulation
        wait;
    end process;

end Behavioral;