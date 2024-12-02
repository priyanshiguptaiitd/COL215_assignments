library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;
entity ROM_Key is
    
    Generic ( DATA_WIDTH : integer := 256;  -- Data width -- Depending upon data of a single Entry  (number of bits)
              ADDR_WIDTH : integer := 8   -- Address width -- Depending upon Number of Elements to be processed (number of bits)
    );

    Port ( 
        addr : in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
        data_out : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0)
      );
end ROM_Key;

architecture Behavioral of ROM_Key is       

    component dist_mem_gen_Key                                        -- Component Declaration -- This is the name of the IP Block memory on the Board
        Port ( a : in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);                               -- Which is pre-loaded with test-case data 
               spo : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0));
    end component;

    signal address_internal : STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
    signal data_out_internal : STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0);
    
begin

    UDATA : dist_mem_gen_Key port map ( a => address_internal, spo => data_out_internal);
    address_internal <= addr;
    data_out <= data_out_internal;
    
end Behavioral;    