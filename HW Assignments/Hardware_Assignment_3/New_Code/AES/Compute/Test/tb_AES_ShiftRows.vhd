library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_AES_ShiftRows is
end tb_AES_ShiftRows;

architecture behavior of tb_AES_ShiftRows is

  -- Component Declaration for the Unit Under Test (UUT)
  component AES_ShiftRows
    generic (
      S : integer := 4
    );
    port (
      en : in std_logic;
      input_data : in std_logic_vector(8 * S - 1 downto 0);
      shift_bytes : in integer;
      output_data : out std_logic_vector(8 * S - 1 downto 0)
    );
  end component;

  -- Signals for the UUT
  signal en : std_logic := '0';
  signal input_data : std_logic_vector(8 * 4 - 1 downto 0) := (others => '0');
  signal shift_bytes : integer := 0;
  signal output_data : std_logic_vector(8 * 4 - 1 downto 0);

begin

  -- Instantiate the Unit Under Test (UUT)
  uut: AES_ShiftRows
    port map (
      en => en,
      input_data => input_data,
      shift_bytes => shift_bytes,
      output_data => output_data
    );

  -- Stimulus process
  stim_proc: process
  begin
    -- Test case 1
    en <= '1';
    input_data <= x"01020304";
    shift_bytes <= 1;
    wait for 10 ns;
    
    -- Test case 2
    input_data <= x"11223344";
    shift_bytes <= 2;
    wait for 10 ns;
    
    -- Test case 3
    input_data <= x"55667788";
    shift_bytes <= 3;
    wait for 10 ns;
    
    -- Test case 4
    input_data <= x"99AABBCC";
    shift_bytes <= 0;
    wait for 10 ns;

    -- End simulation
    wait;
  end process;

end behavior;