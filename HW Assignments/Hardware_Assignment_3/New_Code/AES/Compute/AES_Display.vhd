library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.numeric_std.all;

entity AES_Display is
    
    Port ( clk : in STD_LOGIC;
           reset : in STD_LOGIC;
           start : in STD_LOGIC;
           an : out STD_LOGIC_VECTOR(3 downto 0);
           seg : out STD_LOGIC_VECTOR(6 downto 0);
           done : out STD_LOGIC
        );

end AES_Display;

architecture Behavioral of AES_Display is
----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_Controller

    component AES_Controller is
        
        Port (  clk : in STD_LOGIC;
                reset : in STD_LOGIC;
                start : in STD_LOGIC;
                result : out STD_LOGIC_VECTOR(127 downto 0);
                done : out STD_LOGIC
                );

    end component;

    signal display_signal : std_logic_vector(127 downto 0) := (others => '0');
    

----------------------------------------------------------------------------------------------------
-- Component Declaration for 7SegmentDisplay

    component display_seven_seg is

        Port (
            clock_in : in STD_LOGIC; -- 100 MHz input clock
            reset_timer : in STD_LOGIC; -- Reset signal (Resetting the internal signals to known states)
            input_d: in STD_LOGIC_VECTOR(127 downto 0);
            an : out STD_LOGIC_VECTOR (3 downto 0); -- Anodes signal for display
            seg : out STD_LOGIC_VECTOR (6 downto 0) -- Cathodes signal for display
        );
    end component;

----------------------------------------------------------------------------------------------------
 
begin

----------------------------------------------------------------------------------------------------
-- Instantiation of AES_Controller

    U_AES_Controller: AES_Controller port map (clk => clk, reset => reset, start => start, result => display_signal , done => done);
    U_display_seven_seg: display_seven_seg port map (clock_in => clk, reset_timer => reset, input_d => display_signal, an => an, seg => seg);

end Behavioral;