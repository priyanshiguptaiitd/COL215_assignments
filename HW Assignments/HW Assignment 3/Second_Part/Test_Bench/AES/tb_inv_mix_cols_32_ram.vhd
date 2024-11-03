library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gf256_controller_tb is
end entity;

architecture sim of gf256_controller_tb is
    -- Component declaration
    component gf256_controller is
        port (
            clk        : in std_logic;
            reset      : in std_logic;
            start_calc : in std_logic;
            input_a    : in std_logic_vector(31 downto 0);
            input_b    : in std_logic_vector(31 downto 0);
            result_out : out std_logic_vector(7 downto 0);
            calc_done  : out std_logic
        );
    end component;

    -- Clock period definitions
    constant CLK_PERIOD : time := 10 ns;

    -- Signals for test bench
    signal tb_clk        : std_logic := '0';
    signal tb_reset      : std_logic := '0';
    signal tb_start_calc : std_logic := '0';
    signal tb_input_a    : std_logic_vector(31 downto 0) := (others => '0');
    signal tb_input_b    : std_logic_vector(31 downto 0) := (others => '0');
    signal tb_result_out : std_logic_vector(7 downto 0);
    signal tb_calc_done  : std_logic;

    -- Additional signals for test control
    signal sim_finished : boolean := false;

begin
    -- Instantiate the Unit Under Test (UUT)
    UUT: gf256_controller
        port map (
            clk        => tb_clk,
            reset      => tb_reset,
            start_calc => tb_start_calc,
            input_a    => tb_input_a,
            input_b    => tb_input_b,
            result_out => tb_result_out,
            calc_done  => tb_calc_done
        );

    -- Clock generation process
    clk_process: process
    begin
        while not sim_finished loop
            tb_clk <= '0';
            wait for CLK_PERIOD/2;
            tb_clk <= '1';
            wait for CLK_PERIOD/2;
        end loop;
        wait;
    end process;

    -- Stimulus process
    stimulus_proc: process
    begin
        -- Initialize signals
        tb_reset <= '1';
        tb_start_calc <= '0';
        wait for CLK_PERIOD * 2;
        
        -- Release reset
        tb_reset <= '0';
        wait for CLK_PERIOD * 2;

        -- Test Case 1: Simple calculation
        -- Set input values
        tb_input_a <= x"0E0B0D09";  -- Example input values
        tb_input_b <= x"8B426DD5";
        
        -- Start calculation
        tb_start_calc <= '1';
        wait for CLK_PERIOD * 2;
        
        -- Wait for calculation to complete
        wait until tb_calc_done = '1';
        wait for CLK_PERIOD;
        
        -- Clear start signal
        tb_start_calc <= '0';
        wait for CLK_PERIOD * 5;

        -- Test Case 2: Back-to-back calculations
        -- First calculation
        tb_input_a <= x"090E0B0D";
        tb_input_b <= x"0C70301F";
        
        tb_start_calc <= '1';
        wait until tb_calc_done = '1';
        wait for CLK_PERIOD;
        
        -- Second calculation immediately after
        tb_input_a <= x"FFFF0000";
        tb_input_b <= x"00FF00FF";
        
        wait for CLK_PERIOD * 2;
        wait until tb_calc_done = '1';
        wait for CLK_PERIOD;
        
        tb_start_calc <= '0';
        wait for CLK_PERIOD * 5;

        -- Test Case 3: Reset during calculation
        tb_input_a <= x"12345678";
        tb_input_b <= x"87654321";
        
        tb_start_calc <= '1';
        wait for CLK_PERIOD * 3;
        
        -- Assert reset mid-calculation
        tb_reset <= '1';
        wait for CLK_PERIOD * 2;
        
        -- Release reset and start new calculation
        tb_reset <= '0';
        wait for CLK_PERIOD * 2;
        
        tb_input_a <= x"AAAAAAAA";
        tb_input_b <= x"55555555";
        wait until tb_calc_done = '1';
        wait for CLK_PERIOD;
        
        tb_start_calc <= '0';
        wait for CLK_PERIOD * 5;

        -- Test Case 4: Multiple cycles between calculations
        tb_input_a <= x"11111111";
        tb_input_b <= x"22222222";
        
        tb_start_calc <= '1';
        wait until tb_calc_done = '1';
        wait for CLK_PERIOD;
        
        tb_start_calc <= '0';
        wait for CLK_PERIOD * 10;  -- Longer wait between calculations
        
        tb_input_a <= x"33333333";
        tb_input_b <= x"44444444";
        
        tb_start_calc <= '1';
        wait until tb_calc_done = '1';
        wait for CLK_PERIOD;
        
        tb_start_calc <= '0';
        wait for CLK_PERIOD * 5;

        -- End simulation
        wait for CLK_PERIOD * 10;
        sim_finished <= true;
        wait;
    end process;

end architecture;