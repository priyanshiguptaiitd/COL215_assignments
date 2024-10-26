library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity display_seven_seg is
    Port (
        clock_in : in STD_LOGIC; -- 100 MHz input clock
        reset_timer : in STD_LOGIC; -- Reset signal (Resetting the internal signals to known states)
        input_d: in STD_LOGIC_VECTOR(127 downto 0);
        an : out STD_LOGIC_VECTOR (3 downto 0); -- Anodes signal for display
        seg : out STD_LOGIC_VECTOR (6 downto 0); -- Cathodes signal for display
        mux_sel_out : out STD_LOGIC_VECTOR (1 downto 0);
        d0_out : out STD_LOGIC_VECTOR (3 downto 0);
        d1_out : out STD_LOGIC_VECTOR (3 downto 0);
        d2_out : out STD_LOGIC_VECTOR (3 downto 0);
        d3_out : out STD_LOGIC_VECTOR (3 downto 0);
        tc_clk : out STD_LOGIC;
        timing_scroll_clk : out STD_LOGIC;
        mess_out : out STD_LOGIC_VECTOR(127 downto 0)
    );
end display_seven_seg;

architecture Behavioral of display_seven_seg is
    
    component Timing_block is
        Port (
            clk_in : in STD_LOGIC; -- 100 MHz input clock
            reset : in STD_LOGIC; -- Reset signal (Resetting the internal signals to known states)
            mux_select : out STD_LOGIC_VECTOR (1 downto 0); -- Signal for the mux
            anodes_tout : out STD_LOGIC_VECTOR (3 downto 0); -- Anodes signal for display
            timing_circ_clk : out STD_LOGIC
        );
    end component;

    component seven_seg_decoder_hex is
        port (
            dec_in : in std_logic_vector(3 downto 0);
            dec_out : out std_logic_vector(6 downto 0)
        );
    end component;

    component MUX_4BIT is
        port(
            mux_s : in std_logic_vector(1 downto 0);
            mux_d0 : in std_logic_vector(3 downto 0);
            mux_d1 : in std_logic_vector(3 downto 0);
            mux_d2 : in std_logic_vector(3 downto 0);
            mux_d3 : in std_logic_vector(3 downto 0);
            mux_out_to : out std_logic_vector(3 downto 0)
        );
    end component;
    
    constant N : integer := 512000;
    signal mux_sel: std_logic_vector(1 downto 0);
    signal mux_out_dec: std_logic_vector(3 downto 0);
    signal d0: std_logic_vector(3 downto 0);
    signal d1: std_logic_vector(3 downto 0);
    signal d2: std_logic_vector(3 downto 0);
    signal d3: std_logic_vector(3 downto 0);
    signal time_circ_clk : std_logic;
    signal message: std_logic_vector(127 downto 0) := input_d(127 downto 0);
    signal new_clk : STD_LOGIC := '0';
    signal counter : integer  := 0;
 
    
begin
    
    mux_sel_out <= mux_sel;
    tc_clk <= time_circ_clk;
    timing_scroll_clk <= new_clk;
    mess_out <= message;
    d0_out <= d0;
    d1_out <= d1;
    d2_out <= d2;
    d3_out <= d3;
    
    
    Timer_Block : Timing_Block port map (
        clk_in => clock_in,
        reset => reset_timer,
        mux_select => mux_sel,
        anodes_tout => an,
        timing_circ_clk => time_circ_clk
    );

    MUX_Block : MUX_4BIT port map (
        mux_s => mux_sel,
        mux_d0 => d0,
        mux_d1 => d1,
        mux_d2 => d2,
        mux_d3 => d3,
        mux_out_to => mux_out_dec
    );

    Decoder_Block : seven_seg_decoder_hex port map (
        dec_in => mux_out_dec,
        dec_out => seg
    );  

    NEW_CLK_PROC: process(clock_in, reset_timer)
    begin
        if(reset_timer = '1') then
            counter <= 0;
            new_clk <= '0';
        elsif rising_edge(clock_in) then
            if counter = N then
                counter <= 0;
                new_clk <= not new_clk;
            else
                counter <= counter + 1;
            end if;
        end if;
    end process;


    SCROLL_PROC: process(new_clk,reset_timer)
    begin
        if rising_edge(new_clk) then
            d3 <= message(127 downto 124);
            d2 <= message(123 downto 120);
            d1 <= message(119 downto 116);
            d0 <= message(115 downto 112);
            message(127 downto 4) <= message(123 downto 0);
            message(3 downto 0) <= message(127 downto 124);
        end if;
    end process;
    

end Behavioral;



