library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity AES_Key is
    
    Port ( 
        clk : in STD_LOGIC;                                   -- Clock input
        reset : in STD_LOGIC;                                 -- Reset input
        round_num : in STD_LOGIC_VECTOR(3 downto 0);          -- Round number input (0-10)
        round_key : out STD_LOGIC_VECTOR(127 downto 0)        -- 128-bit round key output
    );
        
end AES_Key;

architecture Behavioral of AES_Key is

    -- ROM component declaration remains the same
    component ROM_Key is
        Generic ( 
            DATA_WIDTH : integer := 8;
            ADDR_WIDTH : integer := 8
        );
        Port ( 
            addr : in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
            data_out : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0)
        );
    end component;

    -- Signals for ROM addressing and data collection
    signal byte_counter : unsigned(3 downto 0);  -- Counts from 0 to 15
    signal temp_key : STD_LOGIC_VECTOR(127 downto 0);
    signal rom_data : STD_LOGIC_VECTOR(7 downto 0);

begin
    -- Single ROM instance
    ROM_inst : ROM_Key 
        generic map (
            DATA_WIDTH => 8,
            ADDR_WIDTH => 8
        )
        port map (
            addr => STD_LOGIC_VECTOR(unsigned(round_num) * 16 + byte_counter),
            data_out => rom_data
        );

    -- Process to build the key byte by byte
    process(clk, reset)
    begin
        if reset = '1' then
            byte_counter <= (others => '0');
            temp_key <= (others => '0');
        elsif rising_edge(clk) then
            if byte_counter < 16 then
                temp_key((to_integer(byte_counter) * 8 + 7) downto (to_integer(byte_counter) * 8)) <= rom_data;
                byte_counter <= byte_counter + 1;
            end if;
        end if;
    end process;

    -- Assign the temporary key to output
    round_key <= temp_key;

end Behavioral;