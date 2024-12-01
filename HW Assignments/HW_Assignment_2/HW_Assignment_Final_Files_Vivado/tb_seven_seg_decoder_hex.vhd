
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
    component MUX_4BIT is
        port(
            mux_s : in std_logic_vector(1 downto 0);
            mux_d0 : in std_logic_vector(3 downto 0);
            mux_d1 : in std_logic_vector(3 downto 0);
            mux_d2 : in std_logic_vector(3 downto 0);
            mux_d3 : in std_logic_vector(3 downto 0);
            mux_out_to : out std_logic_vector(3 downto 0)
        );
    end component;
    signal mux_s: std_logic_vector(1 downto 0);
    signal mux_d0 : std_logic_vector(3 downto 0);
    signal mux_d1 : std_logic_vector(3 downto 0);
    signal mux_d2 : std_logic_vector(3 downto 0);
    signal mux_d3 : std_logic_vector(3 downto 0);
begin
    UUT : MUX_4BIT port map (mux_s=>mux_s,mux_d0=>mux_d0,mux_d1=>mux_d1,mux_d2=>mux_d2,mux_d3=>mux_d3);
    mux_s <= "00", "01" after 80 ns, "10" after 160 ns, "11" after 240 ns;
    mux_d0 <= "0000", "0010" after 20 ns, "0100" after 40 ns, "0110" after 60 ns, "0000" after 80 ns;
    mux_d1 <= "0000", "0001" after 80 ns, "0011" after 100 ns, "0101" after 120 ns, "0111" after 140 ns , "0000" after 160 ns;
    mux_d2 <= "0000", "1000" after 160 ns , "1010" after 180 ns, "1100" after 200 ns, "1110" after 220 ns, "0000" after 240 ns;
    mux_d3 <= "0000", "1001" after 240 ns, "1011" after 260 ns, "1101" after 280 ns, "1111" after 300 ns, "0000" after 320 ns;    
end tb;
