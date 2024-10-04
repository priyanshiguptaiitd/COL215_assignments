
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity tb_seven_seg_decoder_hex is
end tb_seven_seg_decoder_hex;

architecture tb of tb_seven_seg_decoder_hex is
    component seven_seg_decoder_hex is
        port (
        dec_in : in std_logic_vector(3 downto 0);
        dec_out : out std_logic_vector(6 downto 0)
        );
    end component;
    signal dec_in : std_logic_vector(3 downto 0);
    signal dec_out : std_logic_vector(6 downto 0);
    
begin
    UUT : seven_seg_decoder_hex port map(dec_in => dec_in, dec_out => dec_out);
    dec_in  <= "0000", "0001" after 20 ns, "0010" after 40 ns, "0011" after 80 ns ,
               "0100" after 100 ns, "0101" after 120 ns, "0110" after 140 ns, "0111" after 160 ns,
               "1000" after 180 ns, "1001" after 200 ns, "1010" after 220 ns, "1011" after 240 ns,
               "1100" after 260 ns, "1101" after 280 ns, "1110" after 300 ns, "1111" after 320 ns; 

end tb;