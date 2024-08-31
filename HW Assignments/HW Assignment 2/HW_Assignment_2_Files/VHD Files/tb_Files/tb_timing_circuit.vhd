library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_timing_circuit is
end tb_timing_circuit;

architecture tb of tb_timing_circuit is
    -- Component declaration
    component Timing_block is
        Port (
            clk_in : in STD_LOGIC;
            reset : in STD_LOGIC;
            mux_select : out STD_LOGIC_VECTOR (1 downto 0);
            anodes_tout : out STD_LOGIC_VECTOR (3 downto 0)
        );
    end component;

    -- Test signals
    signal clk_in : STD_LOGIC := '0';
    signal reset : STD_LOGIC := '0';
    signal mux_select : STD_LOGIC_VECTOR (1 downto 0);
    signal anodes_tout : STD_LOGIC_VECTOR (3 downto 0);

begin
    uut: Timing_block port map (clk_in => clk_in, reset => reset, mux_select => mux_select, anodes_tout => anodes_tout);
    clk_proc: process
    begin
        while now < 20000 ns loop
            clk_in_tb <= '0';
            wait for 5 ns;
            clk_in_tb <= '1';
            wait for 5 ns;
        end loop;
        wait;
    end process;

end tb;