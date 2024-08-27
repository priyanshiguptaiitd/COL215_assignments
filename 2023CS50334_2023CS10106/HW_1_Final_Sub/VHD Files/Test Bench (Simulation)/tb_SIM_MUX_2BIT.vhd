----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/05/2024 04:30:46 PM
-- Design Name: 
-- Module Name: tb_SIM_MUX_2BIT - tb
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

entity tb_SIM_MUX_2BIT is
end tb_SIM_MUX_2BIT;

architecture tb of tb_SIM_MUX_2BIT is
    component  tb_MUX_2BIT is
        Port ( D1 : in STD_LOGIC;
               D2 : in STD_LOGIC;
               S : in STD_LOGIC;
               O : out STD_LOGIC);
    end component;
    signal D1: std_logic; -- inputs
    signal D2 : std_logic;
    signal S : std_logic;
    signal O : std_logic;
begin
    UUT : tb_MUX_2BIT port map (D1=>D1,D2=>D2,S=>S,O=>O);
    D1 <= '0', '1' after 20 ns, '0' after 40 ns, '1' after 80 ns;
    D2 <= '0', '0' after 20 ns, '1' after 40 ns, '1' after 60 ns;
    S <= '0', '1' after 20 ns, '0' after 40 ns, '1' after 60 ns;
end tb;
