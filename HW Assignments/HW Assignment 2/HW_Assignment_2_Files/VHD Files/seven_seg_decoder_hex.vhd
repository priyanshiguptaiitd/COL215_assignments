library ieee;
use ieee.std_logic_1164.all;

entity seven_seg_decoder_hex is
    port (
        dec_in : in std_logic_vector(3 downto 0);
        dec_out : out std_logic_vector(6 downto 0)
    );
end seven_seg_decoder_hex;

architecture Behavioral of seven_seg_decoder_hex is
    signal A, B, C, D : std_logic;

begin
    Seg_Decoder_HEX : process(dec_in)
    begin
        D <= dec_in(0);
        C <= dec_in(1);
        B <= dec_in(2);
        A <= dec_in(3);
        -- 0 1 2 3 4 5 6  
        -- a b c d e f g
        -- Basys 3 board uses Active Low Pins hence the values are inverted 
        -- from actual reduced expression using K-map (Sum of Min terms method)
        dec_out(0) <= not ((not A and not B and not C and D) or (not A and B and not C and not D) 
                         or (A and B and not C and D) or (A and not B and C and D));
        dec_out(1) <= not ((not A and not C and D) or (A and C and D) or (A and B and not D) or (B and C and not D));
        dec_out(2) <= not ((not A and not B and C and not D) or (A and B and not D) or (A and B and C));
        dec_out(3) <= not ((not A and not B and not C and D) or (not A and B and not C and not D) or (B and C and D)
                         or (A and not B and C and not D));
        dec_out(4) <= not ((not A and D) or (not A and B and not C) or (not B and not C and D));
        dec_out(5) <= not ((not A and not B and D) or (not A and not B and C) or (not A and C and D) or (A and B and not C and D));
        dec_out(6) <= not ((not A and not B and not C) or (A and B and not C and not D) or (not A and B and C and D));
         
    end process;
end Behavioral;