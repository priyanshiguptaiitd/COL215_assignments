library ieee;
use ieee.std_logic_1164.all;

entity seven_segment_decoder is
    port (
        input : in std_logic_vector(3 downto 0);
        output : out std_logic_vector(6 downto 0)
    );
end entity;

architecture behavioral of seven_segment_decoder is
    signal A, B, C, D : std_logic;
    D <= input(0);
    C <= input(1);
    B <= input(2);
    A <= input(3);
begin
    process(input)
    begin
        -- 0 1 2 3 4 5 6  
        -- a b c d e f g
        -- Basys 3 board uses Active Low Pins hence the values are inverted 
        -- from actual reduced expression using K-map (Sum of Min terms method)
        output(0) <= not (A or C or (B and D) or (not B and not D));
        output(1) <= not (not B or (not C and not D) and (C and D));
        output(2) <= not (B or not C or D);
        output(3) <= not ((not B and not D) or (C and not D) or (B and not C and D) or (not B and C) or A);
        output(4) <= not ((not B and not D) or (C and not D));
        output(5) <= not (A or (not C and not D) or (B and not C) or (B and not D));
        output(6) <= not (A or (B and not C) or (not B and C) or (C and not D));
         
    end process;
end architecture;