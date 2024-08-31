library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity Timing_block is
    Port (
        clk_in : in STD_LOGIC; -- 100 MHz input clock
        reset : in STD_LOGIC; -- Reset signal (Resetting the internal signals to known states)
        mux_select : out STD_LOGIC_VECTOR (1 downto 0); -- Signal for the mux
        anodes_tout : out STD_LOGIC_VECTOR (3 downto 0) -- Anodes signal for display
    );
end Timing_block;

architecture Behavioral of Timing_block is
    constant N : integer := 511;-- <need to select correct value>
    signal counter: integer := 0;
    signal mux_select_counter : STD_LOGIC_VECTOR (1 downto 0) := "00";
    signal new_clk : STD_LOGIC := '0';
begin
--Process 1 for dividing the clock from 100 Mhz to 1Khz - 60hz
    -- Gives rise to a clock with t = 10.24 ms or f = 97.65625 Hz
    CLK_PROC: process(clk_in, reset)
    begin
        if(reset = '1') then
            counter <= 0;
            new_clk <= '0';
        elsif rising_edge(clk_in) then
            if counter = N then
                counter <= 0;
                new_clk <= not new_clk;
            else
                counter <= counter + 1;
            end if;
        end if;
                        
    end process;
    --Process 2 for mux select signal
    MUX_PROC: process(new_clk, reset)
    begin
        if(reset = '1') then
            mux_select_counter <= "00";
        elsif(rising_edge(new_clk)) then
            mux_select_counter <= mux_select_counter + 1;
        end if;
        mux_select <= mux_select_counter;
    end process;
    --Process 3 for anode signal
    ANODE_select: process(mux_select_counter,reset)
    begin
        -- Might need to drive anode to high instead of low
        if(reset = '1') then
            anodes_tout <= "1110";
        elsif(mux_select_counter  = "00") then
            anodes_tout <= "1110";
        elsif (mux_select_counter  = "01") then
            anodes_tout <= "1101";
        elsif (mux_select_counter  = "10") then
            anodes_tout <= "1011";
        elsif (mux_select_counter  = "11") then
            anodes_tout <= "0111";
        end if;
    end process;
end Behavioral;
