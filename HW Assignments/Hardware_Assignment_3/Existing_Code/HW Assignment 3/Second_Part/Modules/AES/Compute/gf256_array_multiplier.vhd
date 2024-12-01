library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gf256_array_mul_sequential is
  generic (
    S : integer := 1;  -- Number of Byte elements in output
    N : integer := 4   -- Total Byte elements
  );
  port (
    clk     : in std_logic;
    start   : in std_logic;
    array_a : in std_logic_vector(8 * N - 1 downto 0);
    array_b : in std_logic_vector(8 * N - 1 downto 0);
    result  : out std_logic_vector(8 * S - 1 downto 0);
    done    : out std_logic;
    busy    : out std_logic  -- New signal to indicate processing
  );
end entity;

architecture Behavioral of gf256_array_mul_sequential is
  component gf256_multiply is
    port (
      a      : in std_logic_vector(7 downto 0);
      b      : in std_logic_vector(7 downto 0);
      result : out std_logic_vector(7 downto 0)
    );
  end component;

  type state_type is (IDLE, COMPUTING, COMPLETED);
  signal current_state : state_type := IDLE;

  signal k   : integer range 0 to N-1 := 0;
  signal a_element : std_logic_vector(7 downto 0);
  signal b_element : std_logic_vector(7 downto 0);
  signal temp_result : std_logic_vector(7 downto 0);
  signal internal_result : std_logic_vector(7 downto 0) := (others => '0');
  signal result_index : integer range 0 to N-1 := 0;

begin
  -- Calculate indices and select elements combinatorially
  result_index <= k;
  a_element <= array_a(8*(k+1) - 1 downto 8*k);
  b_element <= array_b(8*(k+1) - 1 downto 8*k);

  -- GF(256) multiplier instantiation
  GF_MULT: gf256_multiply
  port map (
    a => a_element,
    b => b_element,
    result => temp_result
  );

  -- Main process for matrix multiplication
  process(clk)
  begin
    if rising_edge(clk) then
      case current_state is
        when IDLE =>
          if start = '1' then
            current_state <= COMPUTING;
            k <= 0;
            internal_result <= (others => '0');
          end if;

        when COMPUTING =>
          -- Accumulate result
          internal_result <= internal_result xor temp_result;
          
          -- Update indices
          if k = N-1 then
            k <= 0;
            current_state <= COMPLETED;
          else
            k <= k + 1;
          end if;
       
        when COMPLETED =>
          -- Return to IDLE when start is deasserted
          if start = '0' then
            current_state <= IDLE;
          end if;
       
      end case;
    end if;
  end process;

  -- Output assignments
  done <= '1' when current_state = COMPLETED else '0';
  busy <= '1' when current_state = COMPUTING else '0';
  result <= internal_result;

end Behavioral;