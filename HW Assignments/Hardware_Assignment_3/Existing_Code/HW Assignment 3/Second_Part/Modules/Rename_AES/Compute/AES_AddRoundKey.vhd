library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity AES_AddRoundKey is
    Port ( 
        input1 : in STD_LOGIC_VECTOR(7 downto 0);
        input2 : in STD_LOGIC_VECTOR(7 downto 0);
        output : out STD_LOGIC_VECTOR(7 downto 0)
    );
end AES_AddRoundKey;

architecture Behavioral of AES_AddRoundKey is
begin
    -- Simple XOR operation between two 8-bit inputs
    output <= input1 xor input2;
    
end Behavioral;