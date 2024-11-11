library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity AES_Round_tb is
end AES_Round_tb;

architecture behavior of AES_Round_tb is
    -- Component declaration for the Unit Under Test (UUT)
    component AES_Round
        Port ( 
            clk : in std_logic;
            rst : in std_logic;  
            start : in std_logic;
            data : in std_logic_vector(127 downto 0);
            round_key : in std_logic_vector(127 downto 0);
            tempval : out std_logic_vector(127 downto 0); 
            result : out std_logic_vector(127 downto 0);
            temp_inpisb : out std_logic_vector(7 downto 0);
            temp_outisb : out std_logic_vector(7 downto 0);
            temp_input_data_a_MC : out std_logic_vector(31 downto 0);
            temp_input_data_b_MC : out std_logic_vector(31 downto 0);
            temp_output_data_MC : out std_logic_vector(7 downto 0);
            done : out std_logic
        );
    end component;

    -- Signals to connect to the UUT
    signal clk : std_logic := '0';
    signal rst : std_logic := '1';
    signal start : std_logic := '0';
    signal data : std_logic_vector(127 downto 0) := (others => '0');
    signal round_key : std_logic_vector(127 downto 0) := (others => '0');
    signal result : std_logic_vector(127 downto 0);
    signal done : std_logic;
    signal tb_tempval : std_logic_vector(127 downto 0);
    signal tb_temp_inpisb : std_logic_vector(7 downto 0);
    signal tb_temp_outisb : std_logic_vector(7 downto 0);
    signal temp_input_data_a_MC : std_logic_vector(31 downto 0);
    signal temp_input_data_b_MC : std_logic_vector(31 downto 0);
    signal temp_output_data_MC : std_logic_vector(7 downto 0);
    -- Clock generation process
    constant clk_period : time := 10 ns;  -- 50 MHz clock

    -- Simulation duration
    constant sim_duration : time := 100 * clk_period;  -- 1 microsecond

begin
    -- Instantiate the UUT
    uut: AES_Round
        Port map (
            clk => clk,
            rst => rst,
            start => start,
            data => data,
            round_key => round_key,
            result => result,
            tempval => tb_tempval,
            temp_inpisb => tb_temp_inpisb ,
            temp_outisb => tb_temp_outisb, 
            temp_input_data_a_MC => temp_input_data_a_MC,
            temp_input_data_b_MC => temp_input_data_b_MC,
            temp_output_data_MC => temp_output_data_MC,
            done => done
        );

    -- Clock generation
    clk_process : process
    begin
        clk <= '0';
        wait for clk_period / 2;
        clk <= '1';
        wait for clk_period / 2;
    end process;

    -- Test process
    stimulus_process: process
    begin
        -- Reset the UUT
        rst <= '1';
        wait for 2 * clk_period;
        rst <= '0';
        
        -- Apply test values
        data <= x"59cb573ee8fc36897ed69bf18d31b239";
        round_key <= x"71637c0af2aa1f9ef4ffd1a75e85c0c3";
        start <= '1';
        
        -- Start the FSM
        wait for 100*clk_period;
        start <= '0';
        
--        -- Wait for the module to complete
--        wait until done = '1' for sim_duration;
        
        -- End simulation
        wait;
    end process;
end behavior;