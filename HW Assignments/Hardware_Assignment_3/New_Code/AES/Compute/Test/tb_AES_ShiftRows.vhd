library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_AES_ShiftRows is
end tb_AES_ShiftRows;

architecture Behavioral of tb_AES_ShiftRows is

  -- Component Declaration for the Unit Under Test (UUT)
  component AES_ShiftRows
    generic (
      S : integer := 4
    );
    port (
      input_data : in std_logic_vector(8 * S - 1 downto 0);
      shift_bytes : in integer;
      output_data : out std_logic_vector(8 * S - 1 downto 0)
    );
  end component;

  -- Testbench signals
  signal tb_input_data : std_logic_vector(8 * 4 - 1 downto 0);
  signal tb_shift_bytes : integer;
  signal tb_output_data : std_logic_vector(8 * 4 - 1 downto 0);

begin

  -- Instantiate the Unit Under Test (UUT)
  uut: AES_ShiftRows
    port map (
      input_data => tb_input_data,
      shift_bytes => tb_shift_bytes,
      output_data => tb_output_data
    );

  -- Stimulus process
  stim_proc: process
  begin
    -- Test case 1
    tb_input_data <= x"0123456789ABCDEF";
    tb_shift_bytes <= 1;
    wait for 10 ns;
    
    -- Test case 2
    tb_input_data <= x"0123456789ABCDEF";
    tb_shift_bytes <= 2;
    wait for 10 ns;

    -- Test case 3
    tb_input_data <= x"0123456789ABCDEF";
    tb_shift_bytes <= 3;
    wait for 10 ns;

    -- Test case 4
    tb_input_data <= x"0123456789ABCDEF";
    tb_shift_bytes <= 0;
    wait for 10 ns;

    -- End simulation
    wait;
  end process;

end Behavioral;