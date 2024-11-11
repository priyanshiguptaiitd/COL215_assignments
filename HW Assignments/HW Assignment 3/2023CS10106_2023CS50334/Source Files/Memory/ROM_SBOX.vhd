library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity ROM_SBOX is
    
    Generic ( DATA_WIDTH : integer := 8;  
              ADDR_WIDTH : integer := 8   
    );

    Port ( 
        addr : in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
        data_out : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0)
      );
end ROM_SBOX;

architecture Behavioral of ROM_SBOX is       

    component dist_mem_gen_sbox                                        
        Port ( a : in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);                                
               spo : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0));
    end component;

    signal address_internal : STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
    signal data_out_internal : STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0);
    
begin

    UDATA : dist_mem_gen_sbox port map 
            ( 
                a => address_internal, 
                spo => data_out_internal
            );
            
    address_internal <= addr;
    data_out <= data_out_internal;
    
end Behavioral;    

