library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity Key_Exp is
    Port ( clk : in STD_LOGIC;
           reset : in STD_LOGIC;
           key_in : in STD_LOGIC_VECTOR(127 downto 0);
           round_keys : out STD_LOGIC_VECTOR(1407 downto 0));
end Key_Exp;

architecture Behavioral of Key_Exp is

    -- S-box for SubWord operation
    function SubWord(word : STD_LOGIC_VECTOR(31 downto 0)) return STD_LOGIC_VECTOR is
        variable result : STD_LOGIC_VECTOR(31 downto 0);
    begin
        -- Substitute each byte using S-box (dummy values used here, replace with actual S-box values)
        result(31 downto 24) := "00000000"; -- S-box substitution for word(31 downto 24)
        result(23 downto 16) := "00000000"; -- S-box substitution for word(23 downto 16)
        result(15 downto 8) := "00000000";  -- S-box substitution for word(15 downto 8)
        result(7 downto 0) := "00000000";   -- S-box substitution for word(7 downto 0)
        return result;
    end function;

    -- Rcon for the key schedule
    function Rcon(i : integer) return STD_LOGIC_VECTOR is
        variable result : STD_LOGIC_VECTOR(31 downto 0);
    begin
        -- Dummy values for Rcon (replace with actual Rcon values)
        result := "00000000000000000000000000000001";
        return result;
    end function;

    signal temp_key : STD_LOGIC_VECTOR(1407 downto 0);

begin

    process(clk, reset)
    begin
        if reset = '1' then
            temp_key <= (others => '0');
        elsif rising_edge(clk) then
            -- Initial key
            temp_key(127 downto 0) <= key_in;

            -- Key expansion
            for i in 1 to 10 loop
                variable temp : STD_LOGIC_VECTOR(31 downto 0);
                temp := temp_key((i*128-1) downto (i*128-32));
                temp := SubWord(temp);
                temp := temp xor Rcon(i);
                temp_key((i*128+127) downto (i*128)) <= temp_key((i*128-1) downto (i*128-128)) xor temp;
            end loop;
        end if;
    end process;

    round_keys <= temp_key;

end Behavioral;