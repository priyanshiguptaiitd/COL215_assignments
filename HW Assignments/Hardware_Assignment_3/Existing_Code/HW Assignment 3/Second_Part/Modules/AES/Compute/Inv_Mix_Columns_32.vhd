library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gf256_controller is
  port (
    clk        : in std_logic;
    reset      : in std_logic;
    start_calc : in std_logic;  -- Trigger new calculation
    input_a    : in std_logic_vector(31 downto 0);  -- Example: 4 bytes
    input_b    : in std_logic_vector(31 downto 0);  -- Example: 4 bytes
    result_out : out std_logic_vector(7 downto 0);  -- One byte result
    calc_done  : out std_logic
  );
end entity;

architecture Behavioral of gf256_controller is
  -- Component declaration
  component gf256_array_mul_sequential is
    generic (
      S : integer := 1;
      N : integer := 4
    );
    port (
      clk     : in std_logic;
      start   : in std_logic;
      array_a : in std_logic_vector(31 downto 0);
      array_b : in std_logic_vector(31 downto 0);
      result  : out std_logic_vector(7 downto 0);
      done    : out std_logic;
      busy    : out std_logic
    );
  end component;

  -- Control signals
  signal mult_start : std_logic := '0';
  signal mult_done  : std_logic;
  signal mult_busy  : std_logic;
  signal result_reg : std_logic_vector(7 downto 0);

  -- State machine
  type state_type is (WAIT_START, PROCESSING, STORE_RESULT);
  signal state : state_type := WAIT_START;

begin
  -- Instantiate the GF256 multiplier
  GF256_MULT: gf256_array_mul_sequential
    generic map (
      S => 1,
      N => 4
    )
    port map (
      clk     => clk,
      start   => mult_start,
      array_a => input_a,
      array_b => input_b,
      result  => result_reg,
      done    => mult_done,
      busy    => mult_busy
    );

  -- Control process
  process(clk, reset)
  begin
    if reset = '1' then
      state <= WAIT_START;
      mult_start <= '0';
      calc_done <= '0';
    elsif rising_edge(clk) then
      case state is
        when WAIT_START =>
          calc_done <= '0';
          if start_calc = '1' then
            mult_start <= '1';
            state <= PROCESSING;
          end if;

        when PROCESSING =>
          if mult_done = '1' then
            mult_start <= '0';
            state <= STORE_RESULT;
          end if;

        when STORE_RESULT =>
          calc_done <= '1';
          if start_calc = '0' then
            state <= WAIT_START;
          end if;

      end case;
    end if;
  end process;

  -- Output assignment
  result_out <= result_reg;

end Behavioral;