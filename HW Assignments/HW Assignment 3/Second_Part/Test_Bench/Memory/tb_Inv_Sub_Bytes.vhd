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

    end component;

    component RAM
    
    Generic ( DATA_WIDTH_RAM : integer := 8;
              ADDR_WIDTH_RAM : integer := 4);

    Port ( clk : in  STD_LOGIC;
           we  : in  STD_LOGIC;
           addr: in  STD_LOGIC_VECTOR (ADDR_WIDTH_RAM - 1 downto 0);
           din  : in  STD_LOGIC_VECTOR (DATA_WIDTH_RAM - 1 downto 0);
           dout : out STD_LOGIC_VECTOR (DATA_WIDTH_RAM - 1 downto 0));

    end component;

    -- Signals for UUT
    constant  data_width_ram : integer := 8;
    constant addr_width_ram : integer := 4;
    signal clk : STD_LOGIC := '0';
    signal we  : STD_LOGIC := '0';
    signal addr: STD_LOGIC_VECTOR (addr_width_ram -1 downto 0) := (others => '0');
    signal data_in  : STD_LOGIC_VECTOR (data_width_ram -1 downto 0) := (others => '0');
    signal data_out : STD_LOGIC_VECTOR (data_width_ram -1 downto 0) := (others => '0');

    -- Clock period definition
    constant clk_period : time := 10 ns;
    

    -- Signal declarations
    signal input_byte : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');
    signal output_byte : STD_LOGIC_VECTOR(7 downto 0);

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: RAM
        Generic map (
            DATA_WIDTH => data_width_ram,
            ADDR_WIDTH => addr_width_ram
        )
        Port map (
            clk => clk,
            we => we,
            addr => addr,
            din => data_in,
            dout => data_out
        );

    -- Clock process definitions
    clk_process :process
    begin
        clk <= '0';
        wait for clk_period/2;
        clk <= '1';
        wait for clk_period/2;
    end process;



    uut: Inv_Sub_Bytes
        Port map (
            addr_in => input_byte,
            data_out => output_byte
        );

    -- Stimulus process
    stim_proc: process
    begin

        we <= '1';
        
        addr <= "0000";
        data_in <= "10101010";
        wait for clk_period;

        -- Read from address '00000001'
        addr <= "0001";
        wait for clk_period;

        -- Write '01010101' to address '00000010'
        addr <= "0001";
        data_in <= "01010101";
        we <= '1';
        wait for clk_period;

        -- Read from address '00000010'
        addr <= "0010";
        wait for clk_period;
        data_in <= "11110000";
        wait for clk_period;


        -- End simulation
        wait;
    end process;

end tb;