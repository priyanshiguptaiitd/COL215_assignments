library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity mux_4bit is
    Port ( a : in STD_LOGIC_VECTOR (3 downto 0);
           b : in STD_LOGIC_VECTOR (3 downto 0);
           sel : in STD_LOGIC;
           y : out STD_LOGIC_VECTOR (3 downto 0));
end mux_4bit;

architecture Behavioral of mux_4bit is
begin
    y <= a when sel = '0' else b;
end Behavioral;