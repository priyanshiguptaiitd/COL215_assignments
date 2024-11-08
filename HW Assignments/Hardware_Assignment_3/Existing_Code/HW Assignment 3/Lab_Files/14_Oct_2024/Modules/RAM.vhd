library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.unresolved_unsigned;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;
entity RAM is
    Generic ( DATA_WIDTH : integer := 8;  -- Data width (number of bits)
              ADDR_WIDTH : integer := 8   -- Address width (number of bits)
    );
    Port ( clk : in  STD_LOGIC;                                -- Clock
           we  : in  STD_LOGIC;                                -- Write enable
           addr: in  STD_LOGIC_VECTOR (ADDR_WIDTH-1 downto 0); -- Address
           data_in  : in  STD_LOGIC_VECTOR (DATA_WIDTH-1 downto 0); -- Data input
           data_out : out STD_LOGIC_VECTOR (DATA_WIDTH-1 downto 0)  -- Data output
    );
end RAM;

architecture Behavioral of RAM is
    
    type ram_type is array (0 to 2**ADDR_WIDTH-1) of STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0);
    signal ram : ram_type := (others => (others => '0'));
    
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if we = '1' then
                ram(to_integer(unresolved_unsigned(addr))) <= data_in;
            end if;
                data_out <= ram(to_integer(unresolved_unsigned(addr))); -- Read operation
        end if;
    end process;
end Behavioral;   