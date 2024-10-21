library ieee;
use ieee.std_logic_1164.all;

entity bitwise_xor is
	port (
		input_a : in std_logic_vector(127 downto 0);
        input_b : in std_logic_vector(127 downto 0);
        res: out std_logic_vector(127 downto 0)
	);
end bitwise_xor;

architecture behavioral of bitwise_xor is

begin
	process (input_a,input_b) 
	begin
        res <= input_a xor input_b
	end process;

end architecture behavioral;
