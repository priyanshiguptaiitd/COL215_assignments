library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gf256_array_multiply_sequential is
  generic (
    S : integer := 4; -- Length of the arrays (can be changed)
    N : integer := 16  -- Length of the arrays (can be changed)
  );
  port (
    clk     : in std_logic;                               -- Clock signal for sequential operations
    start   : in std_logic;                               -- Start signal to begin multiplication
    array_a : in std_logic_vector(8 * N - 1 downto 0);    -- Input array A (N x 8-bit elements)
    array_b : in std_logic_vector(8 * N - 1 downto 0);    -- Input array B (N x 8-bit elements)
    done    : out std_logic;                              -- Signal indicating completion
    result  : out std_logic_vector(8 * N - 1 downto 0);    -- Output result array (N x 8-bit elements)
    temp_res : out std_logic_vector(7 downto 0);
    temp_ae : out std_logic_vector(7 downto 0);
    temp_be : out std_logic_vector(7 downto 0);
    temp_lc : out integer
  );
end entity gf256_array_multiply_sequential;

architecture Behavioral of gf256_array_multiply_sequential is
  -- Component declaration for GF(2^8) multiplier
  component gf256_multiply is
    port (
      a       : in std_logic_vector(7 downto 0);  -- First 8-bit input
      b       : in std_logic_vector(7 downto 0);  -- Second 8-bit input
      result  : out std_logic_vector(7 downto 0)  -- Result of GF(2^8) multiplication
    );
  end component;

  -- Internal signals
  signal processing : std_logic := '0';  -- Signal to indicate processing state
  signal current_index : integer range 0 to N-1;  -- Index to track current element
  signal current_index_rem : integer range 0 to S-1;  -- Internal signal to track current element
  signal current_index_quo : integer range 0 to S-1;  -- Internal signal to track current element
  signal a_index : integer range 0 to N-1;  -- Index to track current element of array A
  signal b_index : integer range 0 to N-1;  -- Index to track current element of array B
  signal a_element : std_logic_vector(7 downto 0);  -- Signal to hold current element of array A
  signal b_element : std_logic_vector(7 downto 0);  -- Signal to hold current element of array B
  signal temp_result : std_logic_vector(7 downto 0);
  signal internal_result : std_logic_vector(8 * N - 1 downto 0) := (others => '0');  -- Array for the result
  signal done_int : std_logic := '0';  -- Internal signal for completion
  signal loop_count : integer range 0 to S-1 := 0;  -- Internal signal to track loop count

begin

  -- Instantiate the GF(2^8) multiplier
  UUT: gf256_multiply
  port map (
    a => a_element,  -- Select element from array A
    b => b_element,  -- Select element from array B
    result => temp_result  -- Output result for current pair
  );

  -- Sequential process to perform array multiplication
  process (clk)
  begin
    if rising_edge(clk) and done_int = '0' then
      if start = '1' and processing = '0' then
        -- Start processing
        processing <= '1';
        current_index <= 0;
        --current_index_rem <= current_index mod S;
        --current_index_quo <= current_index / S;
        
        --a_index <= current_index_quo*S + loop_count;  -- Track index for array A
        --b_index <= current_index_rem + S*loop_count;  -- Track index for array B
        -- internal_result <= (others => '0');  -- Reset the internal result
        -- done_int <= '0';
      elsif processing = '1' then
        -- Perform multiplication for the current index
        current_index_rem <= current_index mod S;
        current_index_quo <= current_index / S;
        
        a_index <= current_index_quo*S + loop_count;  -- Track index for array A
        b_index <= current_index_rem + S*loop_count;  -- Track index for array B

        -- Select the elements from array A and array B based on current_index
        a_element <= array_a(8 * (a_index + 1) - 1 downto 8 * a_index);
        b_element <= array_b(8 * (b_index + 1) - 1 downto 8 * b_index);
        temp_ae <= a_element;
        temp_be <= b_element;
        temp_lc <= loop_count;
        -- Store result of multiplication into the result array (accumulation using XOR)
        internal_result(8 * (current_index + 1) - 1 downto 8 * current_index) <= internal_result(8 * (current_index + 1) - 1 downto 8 * current_index) xor temp_result;
        
        temp_res <= temp_result;
        -- Move to the next element pair
        if(loop_count < S-1) then
          loop_count <= loop_count + 1;
        else
          loop_count <= 0;
          if current_index < N-1 then
            current_index <= current_index + 1;
          else
            -- All elements processed
            processing <= '0';
            done_int <= '1';  -- Indicate completion
          end if;
        end if;
      end if;
    end if;
  end process;

  -- Assign final result and done signal
  result <= internal_result;
  done <= done_int;

end Behavioral;
