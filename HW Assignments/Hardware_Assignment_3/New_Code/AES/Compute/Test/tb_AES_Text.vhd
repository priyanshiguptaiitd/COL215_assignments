library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_AES_Text is
end tb_AES_Text;

architecture Behavioral of tb_AES_Text is

    -- Component Declaration for the Unit Under Test (UUT)
    component AES_Text
        Generic ( 
                  S : integer := 4;  -- Input Data width (bits per entry)
                  N : integer := 8  -- Output Data width (bits per entry)
                );
        
        Port(   
                data_input : in std_logic_vector(S - 1 downto 0);
                en : in std_logic;
                data_output : out std_logic_vector(N - 1 downto 0)
        );
    end component;

    -- Signals for connecting to UUT
    signal data_input : std_logic_vector(3 downto 0) := (others => '0');
    signal en : std_logic := '0';
    signal data_output : std_logic_vector(7 downto 0);

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: AES_Text
        Generic map (
            S => 4,
            N => 8
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
        wait for 100 ns;  

        -- Test case 1
        data_input <= "0000";
        en <= '1';
        wait for 10 ns;
        en <= '0';
        wait for 10 ns;

        -- Test case 2
        data_input <= "0001";
        en <= '1';
        wait for 10 ns;
        en <= '0';
        wait for 10 ns;

        -- Test case 3
        data_input <= "0010";
        en <= '1';
        wait for 10 ns;
        en <= '0';
        wait for 10 ns;

        -- Test case 4
        data_input <= "0011";
        en <= '1';
        wait for 10 ns;
        en <= '0';
        wait for 10 ns;

        -- Add more test cases as needed

        -- End simulation
        wait;
    end process;

end Behavioral;