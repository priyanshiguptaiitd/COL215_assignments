----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/29/2024 04:10:59 PM
-- Design Name: 
-- Module Name: BASIC_gates - Behavioral
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

entity BASIC_gates is
    Port ( a_and_in : in STD_LOGIC;
           b_and_in : in STD_LOGIC;
           c_and_out : out STD_LOGIC;
           d_or_in : in STD_LOGIC;
           e_or_in : in STD_LOGIC;
           f_or_out : out STD_LOGIC;
           g_not_in : in STD_LOGIC;
           h_not_out : out STD_LOGIC);
end BASIC_gates;

architecture Behavioral of BASIC_gates is

begin
    c_and_out  <= a_and_in  and b_and_in;
    f_or_out  <= d_or_in  or e_or_in;
    h_not_out  <= not g_not_in;

end Behavioral;
