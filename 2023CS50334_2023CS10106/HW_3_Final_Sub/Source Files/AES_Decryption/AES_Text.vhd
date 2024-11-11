library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

-- Accepts an 8-bit Address as input and returns the corresponding value from the S-Box

entity AES_Text is
    Generic ( 
              S : integer := 4;  -- Input Data width (bits per entry)
              N : integer := 8  -- Output Data width (bits per entry)
            );
    
    Port(   
            -- clk : in std_logic;
            data_input : in std_logic_vector(S - 1 downto 0);
            en : in std_logic;
            data_output : out std_logic_vector(N - 1 downto 0)
    );

end AES_Text;

architecture Behavioral of AES_Text is

    component ROM_Text is
    
        Generic ( DATA_WIDTH : integer := 8;  
                  ADDR_WIDTH : integer := 4   
        );
    
        Port ( 
            addr : in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
            data_out : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0)
          );
    end component;

    -- signal i : integer range 0 to N - 1 := 0;
    -- signal is_done : std_logic := '0';
    signal addr_in : std_logic_vector(3 downto 0) := (others => '0');
    signal data_out : std_logic_vector(7 downto 0) := (others => '0');

begin
    
    uut: ROM_Text
        Generic map (
            DATA_WIDTH => 8,
            ADDR_WIDTH => 4
        )
        Port map (
            addr => addr_in,
            data_out => data_out
        );
    
    addr_in <= data_input;  -- Extract byte for address lookup
    data_output <= data_out;  -- Assign output byte by byte
    
end Behavioral;
