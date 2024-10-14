library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity tb_RAM is
--  Port ( );
end tb_RAM;

architecture Behavioral of tb_RAM is
    -- Component Declaration for the Unit Under Test (UUT)
    component RAM
    Generic ( DATA_WIDTH : integer := 8;
              ADDR_WIDTH : integer := 8);
    Port ( clk : in  STD_LOGIC;
           we  : in  STD_LOGIC;
           addr: in  STD_LOGIC_VECTOR (ADDR_WIDTH-1 downto 0);
           data_in  : in  STD_LOGIC_VECTOR (DATA_WIDTH-1 downto 0);
           data_out : out STD_LOGIC_VECTOR (DATA_WIDTH-1 downto 0));
    end component;

    -- Signals for UUT
    signal clk : STD_LOGIC := '0';
    signal we  : STD_LOGIC := '0';
    signal addr: STD_LOGIC_VECTOR (7 downto 0) := (others => '0');
    signal data_in  : STD_LOGIC_VECTOR (7 downto 0) := (others => '0');
    signal data_out : STD_LOGIC_VECTOR (7 downto 0);

    -- Clock period definition
    constant clk_period : time := 10 ns;

begin
    -- Instantiate the Unit Under Test (UUT)
    uut: RAM
        Generic map (
            DATA_WIDTH => 8,
            ADDR_WIDTH => 8
        )
        Port map (
            clk => clk,
            we => we,
            addr => addr,
            data_in => data_in,
            data_out => data_out
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
        -- hold reset state for 100 ns.
        wait for 100 ns;	

        -- Write '10101010' to address '00000001'
        addr <= "00000001";
        data_in <= "10101010";
        we <= '1';
        wait for clk_period;
        we <= '0';

        -- Read from address '00000001'
        addr <= "00000001";
        wait for clk_period;

        -- Write '01010101' to address '00000010'
        addr <= "00000010";
        data_in <= "01010101";
        we <= '1';
        wait for clk_period;
        we <= '0';

        -- Read from address '00000010'
        addr <= "00000010";
        wait for clk_period;

        -- End simulation
        wait;
    end process;

end Behavioral;