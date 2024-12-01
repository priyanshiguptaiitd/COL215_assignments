library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_ROM_Text is
end tb_ROM_Text;

architecture Behavioral of tb_ROM_Text is

    -- Component Declaration for the Unit Under Test (UUT)
    component ROM_Text
    Generic ( DATA_WIDTH : integer := 8;  
              ADDR_WIDTH : integer := 4   
    );
    Port ( 
        addr : in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
        data_out : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0)
      );
    end component;

    -- Signals for connecting to UUT
    signal addr : STD_LOGIC_VECTOR(3 downto 0) := (others => '0');
    signal data_out : STD_LOGIC_VECTOR(7 downto 0);

    -- Clock period definition
    constant clk_period : time := 10 ns;

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: ROM_Text
    Generic map (
        DATA_WIDTH => 8,
        ADDR_WIDTH => 4
    )
    Port map (
        addr => addr,
        data_out => data_out
    );

    -- Stimulus process
    stim_proc: process
    begin
        -- hold reset state for 100 ns.
        wait for 100 ns;  

        -- Test different addresses
        addr <= "0000";
        wait for clk_period;
        addr <= "0001";
        wait for clk_period;
        addr <= "0010";
        wait for clk_period;
        addr <= "0011";
        wait for clk_period;
        addr <= "0100";
        wait for clk_period;
        addr <= "0101";
        wait for clk_period;
        addr <= "0110";
        wait for clk_period;
        addr <= "0111";
        wait for clk_period;
        addr <= "1000";
        wait for clk_period;
        addr <= "1001";
        wait for clk_period;
        addr <= "1010";
        wait for clk_period;
        addr <= "1011";
        wait for clk_period;
        addr <= "1100";
        wait for clk_period;
        addr <= "1101";
        wait for clk_period;
        addr <= "1110";
        wait for clk_period;
        addr <= "1111";
        wait for clk_period;

        -- End simulation
        wait;
    end process;

end Behavioral;