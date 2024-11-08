library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity register_n_bit is
    generic (
        N : integer := 8  -- Default width is 8 bits, but can be changed during instantiation
    );
    port (
        clk     : in  std_logic;                     -- Clock input
        reset   : in  std_logic;                     -- Synchronous reset
        enable  : in  std_logic;                     -- Enable signal
        d_in    : in  std_logic_vector(N-1 downto 0);  -- Input data
        q_out   : out std_logic_vector(N-1 downto 0)   -- Output data
    );
end register_n_bit;

architecture behavioral of register_n_bit is
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if reset = '1' then
                q_out <= (others => '0');    -- Reset all bits to 0
            elsif enable = '1' then
                q_out <= d_in;              -- Load new data when enabled
            end if;
        end if;
    end process;
end behavioral;