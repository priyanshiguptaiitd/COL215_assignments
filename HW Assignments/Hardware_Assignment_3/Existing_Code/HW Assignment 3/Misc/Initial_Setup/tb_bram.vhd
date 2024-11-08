library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity tb_bram_access is
end tb_bram_access;

architecture Behavioral of tb_bram_access is
    signal clk     : std_logic := '0';
    signal rst     : std_logic := '1';
    signal ena     : std_logic := '0'; 
    signal we      : std_logic_vector(0 downto 0) := (others => '0'); 
    signal addr    : std_logic_vector(3 downto 0) := (others => '0');
    signal din     : std_logic_vector(15 downto 0) := (others => '0');
    signal dout    : std_logic_vector(15 downto 0);
    
   
    component bram_access
        Port ( clk      : in  std_logic;
               rst      : in  std_logic;
               ena      : in  std_logic;
               we       : in  std_logic_vector(0 downto 0);
               addr     : in  std_logic_vector(3 downto 0);
               din      : in  std_logic_vector(15 downto 0);
               dout     : out std_logic_vector(15 downto 0)
             );
    end component;
    
begin
    -- Instantiate the Design Under Test (DUT)
    uut: bram_access
        port map (
            clk  => clk,
            rst  => rst,
            ena  => ena,  
            we   => we,
            addr => addr,
            din  => din,
            dout => dout
        );
    
    -- Clock generation
    clk_process : process
    begin
        clk <= not clk after 10 ns; -- Clock with 20 ns period (50 MHz)
        wait for 10 ns;
    end process;

    -- Testbench stimulus
    stimulus : process
    begin
        -- Reset sequence
        rst <= '1';
        ena <= '0'; -- Disable memory during reset
        wait for 50 ns;
        rst <= '0';
        
        -- Step 1: Read from preloaded memory
        ena <= '1'; -- Enable memory
        we <= "0";  -- Ensure write enable is low (read mode)
        
        addr <= "0000"; -- Read from address 0
        wait for 20 ns;
        
        addr <= "0001"; -- Read from address 1
        wait for 20 ns;
        
        addr <= "0010"; -- Read from address 2
        wait for 20 ns;
        
        addr <= "0011"; -- Read from address 3
        wait for 20 ns;
        
        addr <= "0100"; -- Read from address 4
        wait for 20 ns;
        
        -- Step 2: Write new data to memory
        we <= "1"; -- Enable write mode
        addr <= "0000"; din <= "1111111111110000"; -- Write new value to address 0
        wait for 20 ns;
        
        addr <= "0001"; din <= "1010101010101010"; -- Write new value to address 1
        wait for 20 ns;
        
        -- Step 3: Read the updated memory values
        we <= "0"; -- Disable write mode (back to read mode)
        addr <= "0000"; -- Read updated value from address 0
        wait for 20 ns;
        
        addr <= "0001"; -- Read updated value from address 1
        wait for 20 ns;

        ena <= '0'; -- Disable memory access after operations
        
        wait; -- Stop simulation
    end process;

end Behavioral;
