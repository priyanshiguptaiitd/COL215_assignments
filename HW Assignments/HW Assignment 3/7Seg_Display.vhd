library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity display_seven_seg is
    Port (
        clock_in : in STD_LOGIC; -- 100 MHz input clock
        reset_timer : in STD_LOGIC; -- Reset signal (Resetting the internal signals to known states)
        input_d: in STD_LOGIC_VECTOR(127 downto 0);
        an : out STD_LOGIC_VECTOR (3 downto 0); -- Anodes signal for display
        seg : out STD_LOGIC_VECTOR (6 downto 0) -- Cathodes signal for display
    );
end display_seven_seg;

architecture Behavioral of display_seven_seg is
    
    component Timing_block is
        Port (
            clk_in : in STD_LOGIC; -- 100 MHz input clock
            reset : in STD_LOGIC; -- Reset signal (Resetting the internal signals to known states)
            mux_select : out STD_LOGIC_VECTOR (1 downto 0); -- Signal for the mux
            anodes_tout : out STD_LOGIC_VECTOR (3 downto 0) -- Anodes signal for display
        );
    end component;

    component seven_seg_decoder_decimal is
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
    
    constant N : integer := 50000000;
    signal mux_sel: std_logic_vector(1 downto 0);
    signal mux_out_dec: std_logic_vector(3 downto 0);
    signal d0: in std_logic_vector(3 downto 0);
    signal d1: in std_logic_vector(3 downto 0);
    signal d2: in std_logic_vector(3 downto 0);
    signal d3: in std_logic_vector(3 downto 0);
    signal message: in std_logic_vector(127 downto 0) := ;
    signal new_clk : STD_LOGIC := '0';
 
    
begin
    Timer_Block : Timing_Block port map (
        clk_in => clock_in,
        reset => reset_timer,
        mux_select => mux_sel,
        anodes_tout => an
    );

    MUX_Block : MUX_4BIT port map (
        mux_s => mux_sel,
        mux_d0 => d0,
        mux_d1 => d1,
        mux_d2 => d2,
        mux_d3 => d3,
        mux_out_to => mux_out_dec
    );

    Decoder_Block : seven_seg_decoder_decimal port map (
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


    SCROLL_PROC: process(clock_in,reset_timer)
    begin
        if rising_edge(clock_in)
            d3=>message(127 downto 120);
            d2=>message(119 downto 112);
            d1=>message(111 downto 104);
            d0=>message(103 downto 96);
            message(127 downto 8) <= message(119 downto 0);
            message(7 downto 0) <= message(127 downto 120);
        end if;
    end process;
    

end Behavioral;



