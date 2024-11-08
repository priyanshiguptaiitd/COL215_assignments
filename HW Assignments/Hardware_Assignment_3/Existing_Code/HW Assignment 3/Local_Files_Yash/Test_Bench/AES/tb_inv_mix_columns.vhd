library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_inv_mix_columns is
end entity tb_inv_mix_columns;

architecture Behavioral of tb_inv_mix_columns is
    -- Component declaration for the Unit Under Test (UUT)
    component gf256_array_multiply_sequential is
        generic (
            S : integer := 4;  -- Length of the arrays (can be changed)
            N : integer := 16  -- Length of the arrays (can be changed)
        );
        port (
            clk     : in std_logic;                               -- Clock signal for sequential operations
            start   : in std_logic;                               -- Start signal to begin multiplication
            array_a : in std_logic_vector(8 * N - 1 downto 0);    -- Input array A (N x 8-bit elements)
            array_b : in std_logic_vector(8 * N - 1 downto 0);    -- Input array B (N x 8-bit elements)
            done    : out std_logic;                              -- Signal indicating completion
            result  : out std_logic_vector(8 * N - 1 downto 0)    -- Output result array (N x 8-bit elements)
        );
    end component;

    -- Signals to connect to the UUT
    signal clk     : std_logic := '0';
    signal start   : std_logic := '0';
    signal array_a : std_logic_vector(8 * 16 - 1 downto 0) := (others => '0');
    signal array_b : std_logic_vector(8 * 16 - 1 downto 0) := (others => '0');
    signal done    : std_logic := '0';
    signal result  : std_logic_vector(8 * 16 - 1 downto 0);

    -- Clock period definition
    constant clk_period : time := 10 ns;

begin
    -- Instantiate the Unit Under Test (UUT)
    uut: gf256_array_multiply_sequential
        port map (
            clk     => clk,
            start   => start,
            array_a => array_a,
            array_b => array_b,
            done    => done,
            result  => result
        );

    -- Clock generation process
    clk_process : process
    begin
        while true loop
            clk <= '0';
            wait for clk_period / 2;
            clk <= '1';
            wait for clk_period / 2;
        end loop;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize inputs
        array_a <= x"0E0B0D09090E0B0D0D090E0B0B0D090E";  -- Example values for array A
        array_b <= x"8B0C68DA4270434E6D3000D7D51F8AEE";  -- Example values for array B

        -- Start the multiplication process
        start <= '1';  -- Start the operation
        wait for clk_period;  -- Let the start signal be active for 1 clock cycle
        start <= '0';  -- De-assert start
        
        -- Wait for the `done` signal
        wait until done = '1';  -- Wait for the process to complete
        
        -- Observe the result after done is asserted
        wait for clk_period * 2;  -- Let the result settle
        
        -- Add more test cases if needed
        wait;
    end process;

end Behavioral;
