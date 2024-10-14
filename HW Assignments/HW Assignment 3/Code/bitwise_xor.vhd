library ieee;
use ieee.std_logic_1164.all;

entity bitwise_xor is
	port (
		input_byte : in std_logic_vector(7 downto 0);
		output_byte : out std_logic_vector(7 downto 0)
	);
end bitwise_xor;

architecture behavioral of inv_sbox is

begin
	lut : process (input_byte) is
	begin
		case input_byte is
			
			when others => null; -- GHDL complains without this statement
		end case;

	end process lut;

end architecture behavioral;
