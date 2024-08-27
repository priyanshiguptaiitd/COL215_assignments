library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity Timing_block is
    Port (
        clk_in : in STD_LOGIC; -- 100 MHz input clock
        reset : in STD_LOGIC; -- Reset signal (Resetting the internal signals to known states)
        mux_select : out STD_LOGIC_VECTOR (1 downto 0); -- Signal for the mux
        anodes : out STD_LOGIC_VECTOR (3 downto 0) -- Anodes signal for display
    );
end Timing_block;

architecture Behavioral of Timing_block is
    constant N : integer := 511;-- <need to select correct value>
    signal counter: integer := 0;
    signal new_clk : STD_LOGIC := '0';
begin
--Process 1 for dividing the clock from 100 Mhz to 1Khz - 60hz
    NEW_CLK: process(clk_in, reset)
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
    MUX_select: process(new_clk)
    begin

    end process;
    --Process 3 for anode signal
    ANODE_select: process(mux_select)
    begin
    end process;
end Behavioral;