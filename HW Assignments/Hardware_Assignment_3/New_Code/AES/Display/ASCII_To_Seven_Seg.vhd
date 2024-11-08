library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity ASCII_To_Seg is
    Port (
        ascii_char : in  STD_LOGIC_VECTOR (7 downto 0);
        dec_out    : out STD_LOGIC_VECTOR (6 downto 0)
    );
end ASCII_To_Seg;

architecture Behavioral of ASCII_To_Seg is
    component seven_seg_decoder_hex is
        port (
            dec_in : in std_logic_vector(3 downto 0);
            dec_out : out std_logic_vector(6 downto 0)
        );
    end component;

    signal hex_value : std_logic_vector(3 downto 0);
    signal legal_value : std_logic;  -- To flag legal hex values
    signal temp_dec_out : std_logic_vector(6 downto 0);

begin
    HEX_DEC : seven_seg_decoder_hex port map (
        dec_in => hex_value,
        dec_out => temp_dec_out
    );

    HEX_VAL : process(ascii_char)
    begin
        case ascii_char is
            when "00110000" => hex_value <= "0000"; legal_value <= '1'; -- '0'
            when "00110001" => hex_value <= "0001"; legal_value <= '1'; -- '1'
            when "00110010" => hex_value <= "0010"; legal_value <= '1'; -- '2'
            when "00110011" => hex_value <= "0011"; legal_value <= '1'; -- '3'
            when "00110100" => hex_value <= "0100"; legal_value <= '1'; -- '4'
            when "00110101" => hex_value <= "0101"; legal_value <= '1'; -- '5'
            when "00110110" => hex_value <= "0110"; legal_value <= '1'; -- '6'
            when "00110111" => hex_value <= "0111"; legal_value <= '1'; -- '7'
            when "00111000" => hex_value <= "1000"; legal_value <= '1'; -- '8'
            when "00111001" => hex_value <= "1001"; legal_value <= '1'; -- '9'
            when "01000001" => hex_value <= "1010"; legal_value <= '1'; -- 'A'
            when "01000010" => hex_value <= "1011"; legal_value <= '1'; -- 'B'
            when "01000011" => hex_value <= "1100"; legal_value <= '1'; -- 'C'
            when "01000100" => hex_value <= "1101"; legal_value <= '1'; -- 'D'
            when "01000101" => hex_value <= "1110"; legal_value <= '1'; -- 'E'
            when "01000110" => hex_value <= "1111"; legal_value <= '1'; -- 'F'
            when "01100001" => hex_value <= "1010"; legal_value <= '1'; -- 'a'
            when "01100010" => hex_value <= "1011"; legal_value <= '1'; -- 'b'
            when "01100011" => hex_value <= "1100"; legal_value <= '1'; -- 'c'
            when "01100100" => hex_value <= "1101"; legal_value <= '1'; -- 'd'
            when "01100101" => hex_value <= "1110"; legal_value <= '1'; -- 'e'
            when "01100110" => hex_value <= "1111"; legal_value <= '1'; -- 'f'
            when others => hex_value <= "0000"; legal_value <= '0'; -- Default
        end case;
    end process;

    -- Assign `dec_out` based on `legal_value`
    dec_out <= temp_dec_out when legal_value = '1' else "0111111";  -- Only middle segment ON for illegal values

end Behavioral;
