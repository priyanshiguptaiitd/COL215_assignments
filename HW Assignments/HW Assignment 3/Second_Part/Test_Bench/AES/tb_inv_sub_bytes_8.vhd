library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use IEEE.MATH_REAL.ALL;  -- For random number generation

entity TB_Inv_SubBytes is
end TB_Inv_SubBytes;

architecture Behavioral of TB_Inv_SubBytes is
    -- Constants
    constant DATA_WIDTH : integer := 8;
    constant ADDR_WIDTH : integer := 4;  -- 16 memory locations

    -- Signals for RAM
    signal clk_ram : std_logic := '0';
    signal we_ram : std_logic := '1';  -- Write enable
    signal addr_ram : std_logic_vector(ADDR_WIDTH-1 downto 0);
    signal din_ram : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal dout_ram : std_logic_vector(DATA_WIDTH-1 downto 0);

    -- Signals for Inverse SubBytes
    signal ctrl_isb : std_logic := '0';
    signal data_input_isb : std_logic_vector(DATA_WIDTH-1 downto 0);
    signal data_output_isb : std_logic_vector(DATA_WIDTH-1 downto 0);

    -- Component Declarations
    component RAM is
        generic(
            DATA_WIDTH_RAM : integer := 8;
            ADDR_WIDTH_RAM : integer := 4
        );
        Port ( 
            clk : in std_logic;
            we : in std_logic;  
            addr : in std_logic_vector(ADDR_WIDTH_RAM-1 downto 0);
            din : in std_logic_vector(DATA_WIDTH_RAM-1 downto 0);
            dout : out std_logic_vector(DATA_WIDTH_RAM-1 downto 0)
        );
    end component;

    component Inv_Sub_Bytes_8 is
        Generic (
            S : integer := 1;
            N : integer := 7
        );
        Port(  
            data_input : in std_logic_vector(S * N - 1 downto 0);
            ctrl_isb : in std_logic;
            data_output : out std_logic_vector(S * N - 1 downto 0)
        );
    end component;

    -- Clock period definition
    constant CLK_PERIOD : time := 10 ns;

begin
    -- RAM Instantiation
    RAM_INST : RAM
    generic map(
        DATA_WIDTH_RAM => DATA_WIDTH,
        ADDR_WIDTH_RAM => ADDR_WIDTH
    )
    port map(
        clk => clk_ram,
        we => we_ram,
        addr => addr_ram,
        din => din_ram,
        dout => dout_ram
    );

    -- Inverse SubBytes Instantiation
    INV_SUB_BYTES_INST : Inv_Sub_Bytes_8
    generic map(
        S => DATA_WIDTH,
        N => 1  -- Changed to process single byte
    )
    port map(
        data_input => data_input_isb,
        ctrl_isb => ctrl_isb,
        data_output => data_output_isb
    );

    -- Clock Process
    clk_process : process
    begin
        clk_ram <= '1';
        wait for CLK_PERIOD/2;
        clk_ram <= '0';
        wait for CLK_PERIOD/2;
    end process;

    -- Stimulus Process
    stim_process: process
        variable seed1, seed2 : positive;
        variable rand : real;
        variable int_rand : integer;
    
    begin
        -- Initialize RAM with random values
        we_ram <= '1';  -- Enable writing
        for i in 0 to 15 loop
            -- Generate random 8-bit value
            uniform(seed1, seed2, rand);
            int_rand := integer(rand * 255.0);
            
            addr_ram <= std_logic_vector(to_unsigned(i, ADDR_WIDTH));
            din_ram <= std_logic_vector(to_unsigned(int_rand, DATA_WIDTH));
            wait for CLK_PERIOD;
        end loop;

        -- Disable writing, prepare for reading and transformation
        we_ram <= '0';
        
        -- Read and transform each RAM location
        for i in 0 to 15 loop
            -- Set RAM address
            addr_ram <= std_logic_vector(to_unsigned(i, ADDR_WIDTH));
            wait for CLK_PERIOD;
            
            -- Use RAM output as input for Inv SubBytes
            data_input_isb <= dout_ram;
            
            -- Trigger Inverse SubBytes
            ctrl_isb <= '1';
            wait for CLK_PERIOD;
            ctrl_isb <= '0';s
            
            -- Write back transformed value
            we_ram <= '1';
            din_ram <= data_output_isb;
            wait for CLK_PERIOD;
            
            -- Prepare for next iteration
            we_ram <= '0';
        end loop;

        -- End simulation
        wait;
    end process;
end Behavioral;