library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity AES_Round_tb is
end AES_Round_tb;

architecture behavior of AES_Round_tb is

    -- Component declaration for the Unit Under Test (UUT)
    component AES_Round
        Port ( 
            clk : in std_logic;
            rst : in std_logic;  
            start : in std_logic;
            data : in std_logic_vector(127 downto 0);
            round_key : in std_logic_vector(127 downto 0); 
            result : out std_logic_vector(127 downto 0);
            done : out std_logic
        );
    end component;

    -- Signals to connect to the UUT
    signal clk : std_logic := '0';
    signal rst : std_logic := '1';
    signal start : std_logic := '0';
    signal data : std_logic_vector(127 downto 0) := (others => '0');
    signal round_key : std_logic_vector(127 downto 0) := (others => '0');
    signal result : std_logic_vector(127 downto 0);
    signal done : std_logic;

    -- Clock generation process
    constant clk_period : time := 20 ns;  -- 50 MHz clock

begin

    -- Instantiate the UUT
    uut: AES_Round
        Port map (
            clk => clk,
            rst => rst,
            start => start,
            data => data,
            round_key => round_key,
            result => result,
            done => done
        );

    -- Clock generation
    clk_process : process
    begin
        clk <= '0';
        wait for clk_period / 2;
        clk <= '1';
        wait for clk_period / 2;
    end process;

    -- Test process
    stimulus_process: process
    begin
        -- Reset the UUT
        rst <= '1';
        wait for 2 * clk_period;
        rst <= '0';
        
        -- Apply test values
        data <= x"00112233445566778899aabbccddeeff";
        round_key <= x"0f1571c947d9e8590cb7add6af7f6798";
        start <= '1';
        
        -- Start the FSM
        wait for clk_period;
        start <= '0';

        -- Wait until the done signal is asserted
        wait until done = '1';

        -- Check result
        -- End simulation
        wait;
    end process;

end behavior;
