library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.numeric_std.ALL;

entity tb_AES_Display is
end tb_AES_Display;

architecture Behavioral of tb_AES_Display is

    -- Component Declaration for the Unit Under Test (UUT)
    component AES_Display
        Port ( clk : in STD_LOGIC;
               reset : in STD_LOGIC;
               start : in STD_LOGIC;
               an : out STD_LOGIC_VECTOR(3 downto 0);
               seg : out STD_LOGIC_VECTOR(6 downto 0);
               done : out STD_LOGIC
            );
    end component;

    -- Signals for connecting to UUT
    signal clk : STD_LOGIC := '0';
    signal reset : STD_LOGIC := '0';
    signal start : STD_LOGIC := '0';
    signal an : STD_LOGIC_VECTOR(3 downto 0);
    signal seg : STD_LOGIC_VECTOR(6 downto 0);
    signal done : STD_LOGIC;

    -- Clock period definition
    constant clk_period : time := 10 ns;

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: AES_Display
        Port map (
            clk => clk,
            reset => reset,
            start => start,
            an => an,
            seg => seg,
            done => done
        );

    -- Clock process definitions
    clk_process :process
    begin
        clk <= '0';
        wait for clk_period/2;
        clk <= '1';
        wait for clk_period/2;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- hold reset state for 100 ns.
        reset <= '1';
        wait for 100 ns;  
        reset <= '0';
        
        wait for clk_period*10;
        
        -- Start the AES Display
        start <= '1';
        wait for clk_period*10;
        
        -- Wait for the done signal
        wait for clk_period*4000;
        -- Add more stimulus here if needed
        
        -- End simulation
        wait;
    end process;

end Behavioral;