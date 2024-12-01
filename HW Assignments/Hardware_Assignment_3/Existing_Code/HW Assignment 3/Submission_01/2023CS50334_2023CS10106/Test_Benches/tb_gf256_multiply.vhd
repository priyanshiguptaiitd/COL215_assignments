library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_gf256_multiply is
-- No ports in a testbench
end entity tb_gf256_multiply;

architecture Behavioral of tb_gf256_multiply is
  -- Component declaration of the unit under test (UUT)
  component gf256_multiply is
    port (
      a       : in std_logic_vector(7 downto 0);  -- First 8-bit input
      b       : in std_logic_vector(7 downto 0);  -- Second 8-bit input
      result  : out std_logic_vector(7 downto 0)  -- Result of GF(2^8) multiplication
    );
  end component;

  -- Test signals
  signal a       : std_logic_vector(7 downto 0) := (others => '0');
  signal b       : std_logic_vector(7 downto 0) := (others => '0');
  signal result  : std_logic_vector(7 downto 0);

begin
  -- Instantiate the Unit Under Test (UUT)
  UUT: gf256_multiply port map (
    a => a,
    b => b,
    result => result
  );

  -- Stimulus process to apply test vectors
  stimulus_process: process
  begin
    -- Test case 1: Multiply 0x57 by 0x83
    a <= "01010111";  -- 0x57
    b <= "10000011";  -- 0x83
    wait for 10 ns;
    
    -- Test case 2: Multiply 0x1D by 0xC3
    a <= "00011101";  -- 0x1D
    b <= "11000011";  -- 0xC3
    wait for 10 ns;

    -- Test case 3: Multiply 0x00 by 0xAB (result should be 0)
    a <= "00000000";  -- 0x00
    b <= "10101011";  -- 0xAB
    wait for 10 ns;

    -- Test case 4: Multiply 0xFF by 0xFF (result should be reduced modulo polynomial)
    a <= "11111111";  -- 0xFF
    b <= "11111111";  -- 0xFF
    wait for 10 ns;
    
    a<= x"0B";
    b<= x"DA";
    wait for 10 ns;
    
    a<= x"0D";
    b<= x"4E";
    wait for 10 ns;
    
    a<= x"09";
    b<= x"D7";
    wait for 10 ns;
    
    a<= x"0E";
    b<= x"EE";
    wait for 10 ns;
    -- End of simulation
    wait;
  end process;

end architecture Behavioral;
