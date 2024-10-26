library ieee;
use ieee.std_logic_1164.all;

entity bitwise_xor is
	generic (
            DW : integer := 8;  -- Data_Width (1 Byte / 8 bits by default)
            N : integer := 16  -- Number of Elements (16 Bytes by default)
        );
	port (
		input_a : in std_logic_vector(DW*N-1 downto 0);
        input_b : in std_logic_vector(DW*N-1 downto 0);
        res: out std_logic_vector(DW*N-1 downto 0)
	);
end bitwise_xor;

architecture behavioral of bitwise_xor is

begin
	process (input_a,input_b) 
	begin
        res<=input_a xor input_b;
	end process;

end architecture behavioral;
