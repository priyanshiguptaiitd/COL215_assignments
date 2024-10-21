----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 14.10.2024 17:47:09
-- Design Name: 
-- Module Name: RAM - Behavioral
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

entity RAM is
    generic(
        DATA_WIDTH : integer := 8;
        ADDR_WIDTH : integer := 4
    );
    Port ( clk      : in  std_logic;
           we       : in  std_logic;   
           addr     : in  std_logic_vector(ADDR_WIDTH-1 downto 0); -- Address for accessing BRAM
           din      : in  std_logic_vector(DATA_WIDTH-1 downto 0); -- Data to write into BRAM
           dout     : out std_logic_vector(DATA_WIDTH-1 downto 0)  -- Data read from BRAM
         );
end RAM;

architecture Behavioral of RAM is
    type ram_type is array (0 to 2**ADDR_WIDTH-1) of std_logic_vector(DATA_WIDTH-1 downto 0);
    signal ram : ram_type;

begin
    process(clk)
    begin
        if rising_edge(clk) then
            if we = '1' then
                ram(to_integer(unsigned(addr))) <= din;
            elsif we = '0' then
                dout <= ram(to_integer(unsigned(addr)));
            end if;
        end if;
    end process;
end Behavioral;
