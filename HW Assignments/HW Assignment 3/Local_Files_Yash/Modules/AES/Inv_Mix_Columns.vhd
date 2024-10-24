library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gf256_array_multiply_sequential is
  generic (
    S : integer := 4; -- Matrix dimension (4x4 matrix)
    N : integer := 16 -- Total elements (S*S)
  );
  port (
    clk     : in std_logic;
    start   : in std_logic;
    array_a : in std_logic_vector(8 * N - 1 downto 0);
    array_b : in std_logic_vector(8 * N - 1 downto 0);
    done    : out std_logic;
    result  : out std_logic_vector(8 * N - 1 downto 0);
    -- Debug signals
    temp_res : out std_logic_vector(7 downto 0);
    temp_ae : out std_logic_vector(7 downto 0);
    temp_be : out std_logic_vector(7 downto 0);
    temp_lc : out integer
  );
end entity;

architecture Behavioral of gf256_array_multiply_sequential is
  component gf256_multiply is
    port (
      a      : in std_logic_vector(7 downto 0);
      b      : in std_logic_vector(7 downto 0);
      result : out std_logic_vector(7 downto 0)
    );
  end component;

  type state_type is (IDLE, COMPUTING, COMPLETED);
  signal current_state : state_type := IDLE;
  
  signal row : integer range 0 to S-1 := 0;
  signal col : integer range 0 to S-1 := 0;
  signal k   : integer range 0 to S-1 := 0;
  signal first_mult : std_logic := '1';
  
  signal a_element : std_logic_vector(7 downto 0);
  signal b_element : std_logic_vector(7 downto 0);
  signal temp_result : std_logic_vector(7 downto 0);
  signal internal_result : std_logic_vector(8 * N - 1 downto 0) := (others => '0');
  signal result_index : integer range 0 to N-1 := 0;

begin
  -- Calculate indices and select elements combinatorially
  result_index <= row * S + col;
  
  a_element <= array_a((row * S + k) * 8 + 7 downto (row * S + k) * 8);
  b_element <= array_b((k * S + col) * 8 + 7 downto (k * S + col) * 8);

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
            row <= 0;
            col <= 0;
            k <= 0;
            first_mult <= '1';
            internal_result <= (others => '0');
          end if;

        when COMPUTING =>
          -- Accumulate result
          if first_mult = '1' then
            -- For the first multiplication of each element
            internal_result(result_index * 8 + 7 downto result_index * 8) <= temp_result;
            first_mult <= '0';
          else
            -- For subsequent multiplications
            internal_result(result_index * 8 + 7 downto result_index * 8) <=
              internal_result(result_index * 8 + 7 downto result_index * 8) xor temp_result;
          end if;
          
          -- Update indices
          if k = S-1 then
            k <= 0;
            first_mult <= '1';
            if col = S-1 then
              col <= 0;
              if row = S-1 then
                current_state <= COMPLETED;
              else
                row <= row + 1;
              end if;
            else
              col <= col + 1;
            end if;
          else
            k <= k + 1;
          end if;

        when COMPLETED =>
          null;
      end case;
    end if;
  end process;

  -- Output assignments
  done <= '1' when current_state = COMPLETED else '0';
  result <= internal_result;
  
  -- Debug outputs
  temp_res <= temp_result;
  temp_ae <= a_element;
  temp_be <= b_element;
  temp_lc <= k;

end Behavioral;