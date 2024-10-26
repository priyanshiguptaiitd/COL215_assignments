library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_7seg_display is
end tb_7seg_display;

architecture Behavioral of tb_7seg_display is

    -- Component Declaration for the Unit Under Test (UUT)
    component display_seven_seg
        Port (
            clock_in : in STD_LOGIC;
            reset_timer : in STD_LOGIC;
            input_d: in STD_LOGIC_VECTOR(127 downto 0);
            an : out STD_LOGIC_VECTOR (3 downto 0);
            seg : out STD_LOGIC_VECTOR (6 downto 0);
            d0_out : out STD_LOGIC_VECTOR(3 downto 0);
            d1_out : out STD_LOGIC_VECTOR(3 downto 0);
            d2_out : out STD_LOGIC_VECTOR(3 downto 0);
            d3_out : out STD_LOGIC_VECTOR(3 downto 0)
        );
    end component;

    -- Signals for the UUT
    signal clock_in : STD_LOGIC := '0';
    signal reset_timer : STD_LOGIC := '0';
    signal input_d : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal an : STD_LOGIC_VECTOR (3 downto 0);
    signal seg : STD_LOGIC_VECTOR (6 downto 0);
    signal d0_out : STD_LOGIC_VECTOR(3 downto 0);
    signal d1_out : STD_LOGIC_VECTOR(3 downto 0);
    signal d2_out : STD_LOGIC_VECTOR(3 downto 0);
    signal d3_out : STD_LOGIC_VECTOR(3 downto 0);

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
            d0_out => d0_out,
            d1_out => d1_out,
            d2_out => d2_out,
            d3_out => d3_out
        );

    -- Clock process definitions
    clock_process :process
    begin
        while now < 20 sec loop
            clock_in <= '0';
            wait for clock_period/2;
            clock_in <= '1';
            wait for clock_period/2;
        end loop;
        wait;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- hold reset state for 100 ns.
        reset_timer <= '1';
        wait for 100 ns;
        reset_timer <= '0';

        -- Insert stimulus here
        input_d <= X"0123456789ABCDEF0123456789ABCDEF";
        wait for 20 sec;
        -- Finish simulation
        wait;
    end process;

end Behavioral;