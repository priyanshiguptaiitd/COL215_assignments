library ieee;
use ieee.std_logic_1164.all;

entity tb_bitwise_xor is
end tb_bitwise_xor;

architecture testbench of tb_bitwise_xor is

    -- Component Declaration for the Unit Under Test (UUT)
    component bitwise_xor
        generic (
            DW : integer := 8;  -- Data_Width (1 Byte / 8 bits by default)
            N : integer := 16  -- Number of Elements (16 Bytes by default)
        );
        port (
            input_a : in std_logic_vector(DW*N-1 downto 0);
            input_b : in std_logic_vector(DW*N-1 downto 0);
            res     : out std_logic_vector(DW*N-1 downto 0)
        );
    end component;

    -- Constants for the generic parameters
    constant DW : integer := 8;
    constant N : integer := 16;

    -- Signals to connect to UUT
    signal input_a : std_logic_vector(DW*N-1 downto 0) := (others => '0');
    signal input_b : std_logic_vector(DW*N-1 downto 0) := (others => '0');
    signal res     : std_logic_vector(DW*N-1 downto 0);

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: bitwise_xor
        generic map (
            DW => DW,
            N => N
        )
        port map (
            input_a => input_a,
            input_b => input_b,
            res     => res
        );

    -- Stimulus process
    stim_proc: process
    begin
        -- Test case 1
        -- Test case 1
        input_a <= x"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF";
        input_b <= x"00000000000000000000000000000000";
        wait for 10 ns;

        -- Test case 2
        input_a <= x"A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5";
        input_b <= x"5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A";
        wait for 10 ns;

        -- Test case 3
        input_a <= x"1234567890ABCDEF1234567890ABCDEF";
        input_b <= x"FEDCBA0987654321FEDCBA0987654321";
        wait for 10 ns;

        -- Test case 4
        input_a <= x"1234567890ABCDEF1234567890ABCDEF";
        input_b <= x"FEDCBA0987654321FEDCBA0987654321";
        wait for 10 ns;

        -- Add more test cases as needed

        -- End simulation
        wait;
    end process;

end architecture testbench;