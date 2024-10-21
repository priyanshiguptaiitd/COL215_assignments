library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;
entity Inv_Sub_Bytes is
    
    
    Generic ( DATA_WIDTHSB : integer := 8;  -- Data width -- Depending upon data of a single Entry  (number of bits)
              ADDR_WIDTHSB : integer := 8;   -- Address width -- Depending upon Number of Elements to be processed (number of bits)
              DATA_WIDTH_O : integer := 8;
              ADDR_WIDTH_O : integer := 8
              );

    Port ( 
        addr_in : in STD_LOGIC_VECTOR(ADDR_WIDTH_O-1 downto 0);
        data_out : out STD_LOGIC_VECTOR(DATA_WIDTH_O-1 downto 0)

    );
end Inv_Sub_Bytes;

architecture Behavioral of Inv_Sub_Bytes is
    component ROM_SBOX
        Generic ( DATA_WIDTH : integer := DATA_WIDTHSB;
                ADDR_WIDTH : integer := ADDR_WIDTHSB);
        Port ( addr : in STD_LOGIC_VECTOR(A_WIDTH-1 downto 0);
               data_out : out STD_LOGIC_VECTOR(D_WIDTH-1 downto 0) );
    end component;

-- Signals for connecting to UUT
    -- signal addr_input : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');
    -- signal data_output : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');
    signal addr_width : integer := ADDR_WIDTH_O;
    signal data_width : integer := DATA_WIDTH_o;

begin
    UUT : ROM_SBOX
        Generic map (
            DATA_WIDTH => data_width,
            ADDR_WIDTH => addr_width
        )
        Port map (
            addr => addr_in,
            data_out => data_out
        );
    -- addr_input <= addr_in;
    -- data_out <= data_output;
end Behavioral;