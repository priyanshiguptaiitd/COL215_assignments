library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.numeric_std.all;

entity tb_AES_Controller is
end tb_AES_Controller;

architecture Behavioral of tb_AES_Controller is

    -- Component Declaration for the Unit Under Test (UUT)
    component AES_Controller
        Port ( clk : in STD_LOGIC;
               reset : in STD_LOGIC;
               start : in STD_LOGIC;
               result : out STD_LOGIC_VECTOR(127 downto 0);
               an : out STD_LOGIC_VECTOR(3 downto 0);
               seg : out STD_LOGIC_VECTOR(6 downto 0);
               temp_res : out std_logic_vector(127 downto 0);
               temp_key : out std_logic_vector(127 downto 0);
                td0_out : out STD_LOGIC_VECTOR (7 downto 0);
                td1_out : out STD_LOGIC_VECTOR (7 downto 0);
                td2_out : out STD_LOGIC_VECTOR (7 downto 0);
                td3_out : out STD_LOGIC_VECTOR (7 downto 0);
               done : out STD_LOGIC);
    end component;

    -- Signals for the testbench
    signal clk_tb : STD_LOGIC := '0';
    signal reset_tb : STD_LOGIC := '0';
    signal start_tb : STD_LOGIC := '0';
    signal result_tb : STD_LOGIC_VECTOR(127 downto 0);
    signal done_tb : STD_LOGIC;
    signal an_tb : STD_LOGIC_VECTOR(3 downto 0);
    signal seg_tb : STD_LOGIC_VECTOR(6 downto 0);
    signal tb_temp_res : STD_LOGIC_VECTOR(127 downto 0);
    signal tb_td0_out :  STD_LOGIC_VECTOR (7 downto 0);
    signal tb_td1_out :  STD_LOGIC_VECTOR (7 downto 0);
    signal tb_td2_out :  STD_LOGIC_VECTOR (7 downto 0);
    signal tb_td3_out :  STD_LOGIC_VECTOR (7 downto 0);
    signal tb_temp_key : std_logic_vector(127 downto 0);
    -- Clock period definition
    constant clk_period : time := 10 ns;

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: AES_Controller
        Port map (
            clk => clk_tb,
            reset => reset_tb,
            start => start_tb,
            result => result_tb,
            an => an_tb,
            seg => seg_tb,
            temp_res => tb_temp_res,
            td0_out => tb_td0_out,
            td1_out => tb_td1_out,
            td2_out => tb_td2_out,
            td3_out => tb_td3_out,
            temp_key => tb_temp_key,
            done => done_tb
        );

    -- Clock process definitions
    clk_process :process
    begin
        clk_tb <= '0';
        wait for clk_period/2;
        clk_tb <= '1';
        wait for clk_period/2;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- hold reset state for 100 ns.
        reset_tb <= '1';
        wait for 10 ns;
        reset_tb <= '0';

        wait for clk_period*2;
        
        -- Start the AES Controller
        start_tb <= '1';

        -- Wait for the done signal
        wait until done_tb = '1';

        -- Add stimulus here if needed

        -- Wait for a while and then finish
        wait for 100 ns;    
        wait;
    
    end process;

end Behavioral;