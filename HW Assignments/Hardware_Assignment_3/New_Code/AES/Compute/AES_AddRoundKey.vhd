library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity AES_AddRoundKey is
    Port (
        en : in STD_LOGIC;
        input1 : in STD_LOGIC_VECTOR(7 downto 0);
        input2 : in STD_LOGIC_VECTOR(7 downto 0);
        output : out STD_LOGIC_VECTOR(7 downto 0)
    );
end AES_AddRoundKey;

architecture Behavioral of AES_AddRoundKey is
begin
    -- Simple XOR operation between two 8-bit inputs
    process (en, input1, input2)
    begin
        if en = '1' then
            output <= input1 xor input2;
        end if;
    end process;

end Behavioral;