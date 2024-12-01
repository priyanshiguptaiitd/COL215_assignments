library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_AES_FSM01 is
end tb_AES_FSM01;

architecture tb of tb_AES_FSM01 is
    -- Component Declaration for the Unit Under Test (UUT)
    component AES_FSM_01
        Port ( clk      : in  std_logic;
               rst      : in  std_logic;
               start    : in  std_logic;
               data_in  : in  std_logic_vector(127 downto 0);
               done     : out std_logic;
               debug_we    : out std_logic;
               debug_addr  : out std_logic_vector(4-1 downto 0);
               debug_din   : out std_logic_vector(8-1 downto 0);
               debug_dout  : out std_logic_vector(8-1 downto 0);
               debug_bcount : out integer;
               debug_state : out integer
             );
    end component;

    -- Signals for the testbench
    signal clk      : std_logic := '0';
    signal rst      : std_logic := '0';
    signal start    : std_logic := '0';
    signal data_in  : std_logic_vector(127 downto 0) := (others => '0');
    signal done     : std_logic;
    signal dbg_we : std_logic;
    signal dbg_addr : std_logic_vector(4-1 downto 0);
    signal dbg_din : std_logic_vector(8-1 downto 0);
    signal dbg_dout : std_logic_vector(8-1 downto 0);
    signal dbg_count : integer;
    signal dbg_state : integer;


    -- Clock period definition
    constant clk_period : time := 10 ns;

begin
    -- Instantiate the Unit Under Test (UUT)
    uut: AES_FSM_01
        Port map (
            clk => clk,
            rst => rst,
            start => start,
            data_in => data_in,
            done => done,
            debug_we => dbg_we,
            debug_addr => dbg_addr,
            debug_din => dbg_din,
            debug_dout => dbg_dout,
            debug_bcount => dbg_count,
            debug_state => dbg_state
        );

    -- Clock process definitions
    clk_process :process
    begin
        clk <= '0';
        wait for clk_period/2;
        clk <= '1';
        wait for clk_period/2;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- hold reset state for 20 ns.
        rst <= '1';
        wait for 20 ns;
        rst <= '0';
        wait for 20 ns;

        -- Insert stimulus here
        start <= '1';
        data_in <= x"00112233445566778899AABBCCDDEEFF";
        wait for 20 ns;
        start <= '0';

        -- Wait for the done signal
        wait until done = '1';

        -- Add more test cases if needed

        -- End simulation
        wait;
    end process;

end tb;