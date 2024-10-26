library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_7Seg_Display is
end tb_7Seg_Display;

architecture tb of tb_7Seg_Display is
    component display_seven_seg is
        Port (
            clock_in : in STD_LOGIC; -- 100 MHz input clock
            reset_timer : in STD_LOGIC; -- Reset signal (Resetting the internal signals to known states)
            input_d: in STD_LOGIC_VECTOR(127 downto 0);
            an : out STD_LOGIC_VECTOR (3 downto 0); -- Anodes signal for display
            seg : out STD_LOGIC_VECTOR (6 downto 0); -- Cathodes signal for display
            mux_sel_out : out STD_LOGIC_VECTOR (1 downto 0);
            d0_out : out STD_LOGIC_VECTOR(7 downto 0);
            d1_out : out STD_LOGIC_VECTOR(7 downto 0);
            d2_out : out STD_LOGIC_VECTOR(7 downto 0);
            d3_out : out STD_LOGIC_VECTOR(7 downto 0);
            tc_clk : out STD_LOGIC;
            timing_scroll_clk : out STD_LOGIC
--            mess_out : out STD_LOGIC_VECTOR(127 downto 0)
        );
    end component;
    
    -- Signals for connecting to the UUT
    signal clock_in : std_logic := '0';
    signal reset_timer : std_logic := '0';
    signal input_d : STD_LOGIC_VECTOR(127 downto 0);
    signal d0_out : std_logic_vector(7 downto 0);
    signal d1_out : std_logic_vector(7 downto 0);
    signal d2_out : std_logic_vector(7 downto 0);
    signal d3_out : std_logic_vector(7 downto 0);
    signal tc_clk_out : std_logic ;
    signal tc_scroll_clk : std_logic;
    signal an : std_logic_vector(3 downto 0);
    signal seg : std_logic_vector(6 downto 0);
    signal mux_o : std_logic_vector(1 downto 0);
--    signal message_out: std_logic_vector(127 downto 0);

    -- Clock period definition
    constant clock_period : time := 10 ns;

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: display_seven_seg
        Port map (
            clock_in => clock_in,
            reset_timer => reset_timer,
            input_d => input_d,
            an => an,
            seg => seg,
            mux_sel_out => mux_o,
            d0_out => d0_out,
            d1_out => d1_out,
            d2_out => d2_out,
            d3_out => d3_out,
            tc_clk => tc_clk_out,
            timing_scroll_clk => tc_scroll_clk
        );

    -- Clock process for generating clock signal
    clock_proc: process
    begin
        while now < 25000 ms loop
            clock_in <= '0';
            wait for clock_period / 2;
            clock_in <= '1';
            wait for clock_period / 2;
        end loop;
        wait;
    end process;
    reset_timer <= '0';
    -- Stimulus process to provide input and reset signals
    input_d <= x"3031323334404142434497989964576d";
    
end tb;
