----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/05/2024 04:47:28 PM
-- Design Name: 
-- Module Name: tb_SIM_MUX_4BIT - tb
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity tb_SIM_MUX_4BIT is
end tb_SIM_MUX_4BIT;

architecture tb of tb_SIM_MUX_4BIT is
    component tb_MUX_4BIT is
    Port ( d1 : in STD_LOGIC;
           d2 : in STD_LOGIC;
           d3 : in STD_LOGIC;
           d4 : in STD_LOGIC;
           s1 : in STD_LOGIC;
           s2 : in STD_LOGIC;
           o : out STD_LOGIC);
    end component;
    signal d1,d2,d3,d4,s1,s2,o: std_logic; -- inputs
begin
    UUT : tb_MUX_4BIT port map (d1=>d1,d2=>d2,d3=>d3,d4=>d4,s1=>s1,s2=>s2,o=>o);
    d1 <= '1', '0' after 20 ns;
    d2 <= '0', '1' after 40 ns, '0' after 60 ns;
    d3 <= '0', '1' after 80 ns, '0' after 100 ns;
    d4 <= '0', '1' after 120 ns, '0' after 140 ns;
    s1 <= '1', '0' after 40 ns, '1' after 80 ns, '0' after 120 ns;
    s2 <= '1', '1' after 40 ns, '0' after 80 ns, '0' after 120 ns;


end tb;
