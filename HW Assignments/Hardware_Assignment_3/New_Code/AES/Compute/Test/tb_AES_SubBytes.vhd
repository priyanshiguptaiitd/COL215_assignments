library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_AES_SubBytes is
end tb_AES_SubBytes;

architecture Behavioral of tb_AES_SubBytes is

    -- Component Declaration for the Unit Under Test (UUT)
    component AES_SubBytes
        Generic ( 
            S : integer := 1;  -- Data width (bits per entry)
            N : integer := 8  -- Number of elements to be processed
        );
        Port(   
            data_input : in std_logic_vector(S * N - 1 downto 0);
            en : in std_logic;
            data_output : out std_logic_vector(S * N - 1 downto 0)
        );
    end component;

    -- Signals for connecting to UUT
    signal data_input : std_logic_vector(7 downto 0) := (others => '0');
    signal en : std_logic := '0';
    signal data_output : std_logic_vector(7 downto 0);

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: AES_SubBytes
        Generic map (
            S => 8,
            N => 1
        )
        Port map (
            data_input => data_input,
            en => en,
            data_output => data_output
        );

    -- Stimulus process
    stim_proc: process
    begin
        -- hold reset state for 100 ns.
        wait for 10 ns;  

        -- Test case 1
        -- Test case 1
        data_input <= x"26";  -- Example input in hex
        en <= '1';
        wait for 10 ns;
        en <= '0';
        wait for 10 ns;

        -- Test case 2
        data_input <= x"CA";  -- Example input in hex
        en <= '1';
        wait for 10 ns;
        en <= '0';
        wait for 10 ns;

        -- Add more test cases as needed

        -- End simulation
        wait;
    end process;

end Behavioral;