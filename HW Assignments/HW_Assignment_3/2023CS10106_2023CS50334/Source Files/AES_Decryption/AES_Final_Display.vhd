library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.numeric_std.all;

entity AES_FDisplay is
    
    Port ( clk : in STD_LOGIC;
           reset : in STD_LOGIC;
           start : in STD_LOGIC;
           an : out STD_LOGIC_VECTOR(3 downto 0);
           seg : out STD_LOGIC_VECTOR(6 downto 0);
           disp_sig : out STD_LOGIC_VECTOR(127 downto 0);
           cos : out STD_LOGIC_VECTOR(1 downto 0);
           done : out STD_LOGIC
        );

end AES_FDisplay;

architecture Behavioral of AES_FDisplay is
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
    
    signal control_state : std_logic_vector(1 downto 0) := (others => '0');
    
    signal control_reset : std_logic ;
    signal control_start : std_logic ;
    signal control_done : std_logic ;

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
    
    signal to_be_display_signal : std_logic_vector(127 downto 0) := x"30313233343536373839414243444546";


----------------------------------------------------------------------------------------------------
-- FSM Signals Declaration
    type state_type is (S0, Compute, Display, SF);
    signal state : state_type;
    signal we_done : std_logic := '0';





begin

----------------------------------------------------------------------------------------------------
-- Instantiation of AES_Controller
    disp_sig <= display_signal;
    cos <= control_state;
    
    U_AES_Controller: AES_Controller port map (clk => clk, reset => control_reset, start => control_start, result => display_signal , done => control_done);
    
    U_display_seven_seg: display_seven_seg port map (clock_in => clk, reset_timer => reset, input_d => to_be_display_signal, an => an, seg => seg);


process(clk, reset)

begin
    if reset = '1' then
        state <= S0;
        display_signal <= (others => '0');
        done <= '0';
        control_done <= '0';
        we_done <= '0';

    elsif rising_edge(clk) then
        case state is

            when S0 =>
                if (start = '1' and we_done = '0') then
                    state <= Compute;
                end if;

            when Compute =>
                if control_state = "00" then
                    control_reset <= '1';
                    control_state <= "01";
                elsif control_state = "01" then
                    control_state <= "10";
                elsif control_state = "10" then
                    control_reset <= '0';
                    control_start <= '1';
                    control_state <= "11";
                elsif(control_state = "11") then
                    if(control_done = '1') then
                        we_done <= '1';
                        done <= '1';
                        to_be_display_signal <= display_signal;
                        control_state <= "00";
                        state <= Display;
                    end if;
                end if;

            when Display =>
                if we_done = '1' then
                    state <= SF;
                else
                    state <= Display;
                end if;

            when SF =>
                state <= S0;
                
            when others =>
                state <= S0;
        end case;
    end if;
end process;


end Behavioral;