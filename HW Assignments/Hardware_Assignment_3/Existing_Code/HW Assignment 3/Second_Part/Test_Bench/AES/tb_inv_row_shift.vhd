library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_inv_row_shift is
end tb_inv_row_shift;

architecture Behavioral of tb_inv_row_shift is

    -- Constants
    constant S : integer := 4;
    constant N : integer := 16;

    -- Signals
    signal input_data : std_logic_vector(8 * N - 1 downto 0);
    signal output_data : std_logic_vector(8 * N - 1 downto 0);

    -- Component declaration
    component inv_row_shift
        generic (
            S : integer := 4;
            N : integer := 16
        );
        port (
            input_data : in std_logic_vector(8 * N - 1 downto 0);
            output_data : out std_logic_vector(8 * N - 1 downto 0)
        );
    end component;

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: inv_row_shift
        generic map (
            S => S,
            N => N
        )
        port map (
            input_data => input_data,
            output_data => output_data
        );

    -- Stimulus process
    stim_proc: process
    begin
        -- Test case 1
        input_data <= x"00112233445566778899AABBCCDDEEFF";
        wait for 10 ns;
        
        -- Test case 2
        input_data <= x"FFEEDDCCBBAA99887766554433221100";
        wait for 10 ns;

        -- Test case 3
        input_data <= x"0123456789ABCDEF0123456789ABCDEF";
        wait for 10 ns;

        -- Test case 4
        input_data <= x"FEDCBA9876543210FEDCBA9876543210";
        wait for 10 ns;

        -- End simulation
        wait;
    end process;

end Behavioral;