library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity Inv_Sub_Bytes is
    Generic ( 
              S : integer := 8;  -- Data width (bits per entry)
              N : integer := 16   -- Number of elements to be processed
            );
    
    Port(   
            clk : in std_logic;
            data_input : in std_logic_vector(S * N - 1 downto 0);
            data_output : out std_logic_vector(S * N - 1 downto 0)
    );        
end Inv_Sub_Bytes;

architecture Behavioral of Inv_Sub_Bytes is

    component ROM_SBOX
        Generic ( 
            DATA_WIDTH : integer := 8;
            ADDR_WIDTH : integer := 8
        );
        Port ( 
            addr : in STD_LOGIC_VECTOR(ADDR_WIDTH - 1 downto 0);
            data_out : out STD_LOGIC_VECTOR(DATA_WIDTH - 1 downto 0)
        );
    end component;

    signal i : integer range 0 to N - 1 := 0;
    signal is_done : std_logic := '0';
    signal addr_in : std_logic_vector(7 downto 0);
    signal data_o : std_logic_vector(7 downto 0);

begin

    uut: ROM_SBOX
        Generic map (
            DATA_WIDTH => 8,
            ADDR_WIDTH => 8
        )
        Port map (
            addr => addr_in,
            data_out => data_o
        );

    -- Update addr_in based on the current byte being processed
    addr_process: process(clk)
    begin
        if rising_edge(clk) and is_done = '0' then
            addr_in <= data_input(8 * i + 7 downto 8 * i);  -- Extract byte for address lookup

            if i < N - 1 then
                i <= i + 1;
            else
                is_done <= '1';
            end if;
        end if;
    end process;

    -- Write the output based on data from ROM_SBOX
    write_process : process(clk)
    begin
        if rising_edge(clk) and is_done = '0' then
            data_output(8 * i + 7 downto 8 * i) <= data_o;  -- Assign output byte by byte
        end if;
    end process;

end Behavioral;
