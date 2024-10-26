----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 14.10.2024 17:53:09
-- Design Name: 
-- Module Name: tb_RAM - tb
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_RAM is
--  Port ( );
end tb_RAM;

architecture Behavioral of tb_RAM is
    -- Component Declaration for the Unit Under Test (UUT)
    component RAM
        Generic ( DATA_WIDTH_RAM : integer := 8;
                  ADDR_WIDTH_RAM : integer := 4);
        Port ( clk : in  STD_LOGIC;
               we  : in  STD_LOGIC;
               addr: in  STD_LOGIC_VECTOR (ADDR_WIDTH_RAM-1 downto 0);
               din  : in  STD_LOGIC_VECTOR (DATA_WIDTH_RAM-1 downto 0);
               dout : out STD_LOGIC_VECTOR (DATA_WIDTH_RAM-1 downto 0));
    end component;

    -- Signals for UUT
    constant data_width : integer := 8;
    constant addr_width : integer := 4;
    signal clk : STD_LOGIC := '0';
    signal we  : STD_LOGIC := '0';
    signal addr: STD_LOGIC_VECTOR (addr_width -1 downto 0) := (others => '0');
    signal data_in  : STD_LOGIC_VECTOR (data_width-1 downto 0) := (others => '0');
    signal data_out : STD_LOGIC_VECTOR (data_width-1 downto 0) := (others => '0');

    -- Clock period definition
    constant clk_period : time := 10 ns;

begin
    -- Instantiate the Unit Under Test (UUT)
    uut: RAM
        Generic map (
            DATA_WIDTH_RAM => data_width,
            ADDR_WIDTH_RAM => addr_width
        )
        Port map (
            clk => clk,
            we => we,
            addr => addr,
            din => data_in,
            dout => data_out
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
        -- Test Case 1: Write '10101010' to address '0001' and read back
        we <= '1';
        addr <= "0000";
        data_in <= "10101010";
        wait for clk_period;
        we <= '0';
        wait for clk_period;
        
        -- Test Case 2: Overwrite '01010101' to address '0001' and read back
        we <= '1';
        addr <= "0001";
        data_in <= "01010101";
        wait for clk_period;
        we <= '0';
        wait for clk_period;
        
        -- Test Case 3: Write '11110000' to address '0010' and read back
        we <= '1';
        addr <= "0010";
        data_in <= "11110000";
        wait for clk_period;
        we <= '0';
        wait for clk_period;
        
        -- Test Case 4: Write '00001111' to address '0011' and read back
        we <= '1';
        addr <= "0011";
        data_in <= "00001111";
        wait for clk_period;
        we <= '0';
        wait for clk_period;
        
        -- End simulation
        wait;
    end process;

end Behavioral;