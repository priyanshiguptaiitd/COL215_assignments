----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/05/2024 04:01:39 PM
-- Design Name: 
-- Module Name: tb_MUX_4BIT - tb
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

entity tb_MUX_4BIT is
    Port ( d1 : in STD_LOGIC;
           d2 : in STD_LOGIC;
           d3 : in STD_LOGIC;
           d4 : in STD_LOGIC;
           s1 : in STD_LOGIC;
           s2 : in STD_LOGIC;
           o : out STD_LOGIC);
end tb_MUX_4BIT;

architecture tb of tb_MUX_4BIT is
    component tb_MUX_2BIT is
        Port ( D1 : in STD_LOGIC;
               D2 : in STD_LOGIC;
               S : in STD_LOGIC;
               O : out STD_LOGIC);
    end component;
    signal m1,m2: std_logic;
begin
    MUX1 : tb_MUX_2BIT port map (d1,d2,s1,m1);
    MUX2 : tb_MUX_2BIT port map (d3,d4,s1,m2);
    MUXF: tb_MUX_2BIT port map (m1,m2,s2,o);
    

end tb;
