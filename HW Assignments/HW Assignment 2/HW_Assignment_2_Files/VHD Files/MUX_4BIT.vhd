library ieee;
use ieee.std_logic_1164.all;

entity MUX_4BIT is
    port(
        mux_s : in std_logic_vector(1 downto 0);
        mux_d0 : in std_logic_vector(3 downto 0);
        mux_d1 : in std_logic_vector(3 downto 0);
        mux_d2 : in std_logic_vector(3 downto 0);
        mux_d3 : in std_logic_vector(3 downto 0);
        mux_out_to : out std_logic_vector(3 downto 0);
    );
end MUX_4BIT;

architecture Behavioral of MUX_4BIT is

begin
    MUX_4BIT: process(mux_s, mux_d0, mux_d1, mux_d2, mux_d4):
    begin
        case mux_s is
            when "00" =>
                mux_out_to <= mux_d0;
            when "01" =>
                mux_out_to <= mux_d1;
            when "10" =>
                mux_out_to <= mux_d2;
            when "11"=>
                mux_out_to <= mux_d4;
        end case;
    end process MUX_4BIT;    

end Behavioral;