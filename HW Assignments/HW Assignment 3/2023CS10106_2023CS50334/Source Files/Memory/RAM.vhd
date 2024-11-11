library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity RAM is
    generic (
        DATA_WIDTH : integer := 8;  -- Width of data bus
        ADDR_WIDTH : integer := 4    -- Width of address bus
    );
    port (
        clk     : in std_logic;                                     -- Clock input
        we      : in std_logic;                                     -- Write enable
        addr    : in std_logic_vector(ADDR_WIDTH-1 downto 0);       -- Address input
        data_in : in std_logic_vector(DATA_WIDTH-1 downto 0);       -- Data input
        data_out: out std_logic_vector(DATA_WIDTH-1 downto 0)       -- Data output
    );
end RAM;

architecture Behavioral of RAM is
    -- Defining the RAM type
    type RAM_type is array (0 to (2**ADDR_WIDTH)-1) of std_logic_vector(DATA_WIDTH-1 downto 0);
    -- Declaring the RAM signal
    signal RAM_array : RAM_type;

begin
    process(clk)
    begin
        if rising_edge(clk) then
            if we = '1' then
                -- Write operation only when we = 1
                RAM_array(to_integer(unsigned(addr))) <= data_in;
            end if;
            
            -- Making Read operation (synchronous)
            data_out <= RAM_array(to_integer(unsigned(addr)));
        end if;
    end process;

end Behavioral;