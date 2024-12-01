library ieee;
use ieee.std_logic_1164.all;

entity seven_seg_decoder_decimal is
    port (
        dec_in : in std_logic_vector(3 downto 0);
        dec_out : out std_logic_vector(6 downto 0)
    );
end seven_seg_decoder_decimal;

architecture Behavioral of seven_seg_decoder_decimal is
    signal A, B, C, D : std_logic;
    
begin
    Seg_Decoder_DEC : process(dec_in)
    begin
        D <= dec_in(0);
        C <= dec_in(1);
        B <= dec_in(2);
        A <= dec_in(3);
        
        -- Segment a
        dec_out(0) <= not (A or C or (B and D) or (not B and not D));
        -- Segment b
        dec_out(1) <= not (not B or (not C and not D) and (C and D));
        -- Segment c
        dec_out(2) <= not (B or not C or D);
        -- Segment d
        dec_out(3) <= not ((not B and not D) or (C and not D) or (B and not C and D) or (not B and C) or A);
        -- Segment e
        dec_out(4) <= not ((not B and not D) or (C and not D));
        -- Segment f
        dec_out(5) <= not (A or (not C and not D) or (B and not C) or (B and not D));
        -- Segment g
        dec_out(6) <= not (A or (B and not C) or (not B and C) or (C and not D));
        
    end process;
end Behavioral;