----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/05/2024 03:23:19 PM
-- Design Name: 
-- Module Name: tb_MUX_2BIT - tb
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

entity tb_MUX_2BIT is
    Port ( D1 : in STD_LOGIC;
           D2 : in STD_LOGIC;
           S : in STD_LOGIC;
           O : out STD_LOGIC);
end tb_MUX_2BIT;

architecture tb of tb_MUX_2BIT is
    component AND_gate is
        Port ( a : in STD_LOGIC;
               b : in STD_LOGIC;
               c : out STD_LOGIC);
    end component;
    component OR_gate is
        Port ( d : in STD_LOGIC;
               e : in STD_LOGIC;
               f : out STD_LOGIC);
    end component;
    
    component NOT_gate is
        Port ( g : in STD_LOGIC;
               h : out STD_LOGIC);
    end component;
    
    signal NOT_S,M1,M2 : std_logic ;
    
begin
    DUT1 : NOT_gate port map (S,NOT_S);
    DUT2 : AND_gate port map (D1,S,M1);
    DUT3 : AND_gate port map (D2,NOT_S,M2);
    DUT4 : OR_gate port map (M1,M2,O);
    
    
end tb;
