library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity tb_Inv_Sub_Bytes is
end tb_Inv_Sub_Bytes;

architecture tb of tb_Inv_Sub_Bytes is

    -- Component Declaration for the Unit Under Test (UUT)
    component Inv_Sub_Bytes
    
    Generic ( DATA_WIDTHSB : integer := 8;  -- Data width -- Depending upon data of a single Entry  (number of bits)
              ADDR_WIDTHSB : integer := 8;   -- Address width -- Depending upon Number of Elements to be processed (number of bits)
              DATA_WIDTH_O : integer := 8;
              ADDR_WIDTH_O : integer := 8
              );

    Port ( 
        addr_in : in STD_LOGIC_VECTOR(ADDR_WIDTH_O-1 downto 0);
        data_out : out STD_LOGIC_VECTOR(DATA_WIDTH_O-1 downto 0)

    );

    

    -- Signal declarations
    signal input_byte : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');
    signal output_byte : STD_LOGIC_VECTOR(7 downto 0);

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: Inv_Sub_Bytes
        Port map (
            addr_in => input_byte,
            data_out => output_byte
        );

    -- Stimulus process
    stim_proc: process
    begin
        -- Test case 1
        input_byte <= "00000001";
        wait for 10 ns;
        assert (output_byte = "EXPECTED_OUTPUT_1") report "Test case 1 failed" severity error;

        -- Test case 2
        input_byte <= "00000010";
        wait for 10 ns;
        assert (output_byte = "EXPECTED_OUTPUT_2") report "Test case 2 failed" severity error;

        -- Add more test cases as needed

        wait;
    end process;

end tb;