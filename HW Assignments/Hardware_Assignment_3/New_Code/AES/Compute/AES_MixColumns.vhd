library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Accepts 4 Bytes of input data and shifts the bytes by a given amount


entity AES_MixColumns is
    
    generic (
        S : integer := 4 -- Number of Bytes in a row
        );

    port (
        en : in std_logic;
        input_data_a : in std_logic_vector(8 * S - 1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
        input_data_b : in std_logic_vector(8 * S - 1 downto 0); -- Number of bytes to shift (Must lie from 0 to S-1)
        output_data : out std_logic_vector(8 - 1 downto 0) -- Output result array (1 Byte)
    );

end AES_MixColumns;

architecture inv_mix_cols of AES_MixColumns is

    component AES_GF_256 is
        port (
            a : in std_logic_vector(7 downto 0);
            b : in std_logic_vector(7 downto 0);
            result : out std_logic_vector(7 downto 0)
        );
    end component;

    signal td_0,td_1,td_2,td_3 : std_logic_vector(7 downto 0);


-- Making this process clock independent

begin

    uut_0 : AES_GF_256 port map (a => input_data_a(7 downto 0), b => input_data_b(7 downto 0), result => td_0);
    uut_1 : AES_GF_256 port map (a => input_data_a(15 downto 8), b => input_data_b(15 downto 8), result => td_1);
    uut_2 : AES_GF_256 port map (a => input_data_a(23 downto 16), b => input_data_b(23 downto 16),result => td_2);
    uut_3 : AES_GF_256 port map (a => input_data_a(31 downto 24),b => input_data_b(31 downto 24), result => td_3);

    process (en, td_0, td_1, td_2, td_3)
    begin
        if en = '1' then
            output_data <= (td_0 xor td_1) xor (td_2 xor td_3);
        end if;
    end process;

end inv_mix_cols;
