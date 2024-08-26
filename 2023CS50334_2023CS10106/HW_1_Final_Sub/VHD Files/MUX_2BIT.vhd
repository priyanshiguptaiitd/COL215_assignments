----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/05/2024 03:07:11 PM
-- Design Name: 
-- Module Name: MUX_2BIT - Behavioral
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

entity MUX_2BIT is
    Port ( d1 : in STD_LOGIC;
           d2 : in STD_LOGIC;
           s : in STD_LOGIC;
           o : out STD_LOGIC);
end MUX_2BIT;

architecture Behavioral of MUX_2BIT is
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

begin
    DUT1 : NOT_gate port map (S,NOT_S);
    DUT2 : AND_gate port map (D1,S,M1);
    DUT3 : AND_gate port map (D2,NOT_S,M2);
    DUT4 : OR_gate port map (M1,M2,O);
    
    d1  <= '0', '1' after 20 ns, '0' after 40 ns, '1' after 60 ns;
    d2  <= '0', '0' after 20 ns, '1' after 40 ns, '1' after 60 ns;
    s  <= '1';
    


end Behavioral;
