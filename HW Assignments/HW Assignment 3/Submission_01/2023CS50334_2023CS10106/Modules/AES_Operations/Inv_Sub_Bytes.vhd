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
            data_output : out std_logic_vector(S * N - 1 downto 0);
            is_completed : out std_logic 
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
    signal current_byte : std_logic_vector(7 downto 0);
    signal write_index : integer range 0 to N - 1 := 0;
    signal data_valid : std_logic := '0';
    signal temp_output : std_logic_vector(S * N - 1 downto 0) := (others => '0');  -- Initialize temporary output buffer
    
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

    -- Assign the temporary output to the actual output
    data_output <= temp_output;

    -- Process to handle address generation and counter
    addr_process: process(clk)
    begin
        if rising_edge(clk) then
            if is_done = '0' then
                -- Extract current byte for address lookup
                addr_in <= data_input(8 * i + 7 downto 8 * i);
                
                if i < N - 1 then
                    i <= i + 1;
                else
                    is_done <= '1';
                    is_completed <= '1';
                end if;
                
                -- Set data valid for next cycle
                data_valid <= '1';
            else
                data_valid <= '0';
            end if;
        end if;
    end process;

    -- Separate process to handle output writing
    write_process : process(clk)
    begin
        if rising_edge(clk) then
            if data_valid = '1' then
                -- Write the substituted byte to output
                temp_output(8 * write_index + 7 downto 8 * write_index) <= data_o;
                
                if write_index < N - 1 then
                    write_index <= write_index + 1;
                end if;
            end if;
        end if;
    end process;
    
end Behavioral;