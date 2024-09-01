library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity tb_7Seg_Display is
end tb_7Seg_Display;

architecture tb of tb_7Seg_Display is
    component display_seven_seg is
        Port (
            clock_in : in STD_LOGIC; -- 100 MHz input clock
            reset_timer : in STD_LOGIC; -- Reset signal (Resetting the internal signals to known states)
            d0: in std_logic_vector(3 downto 0);
            d1: in std_logic_vector(3 downto 0);
            d2: in std_logic_vector(3 downto 0);
            d3: in std_logic_vector(3 downto 0);
            an : out STD_LOGIC_VECTOR (3 downto 0); -- Anodes signal for display
            seg : out STD_LOGIC_VECTOR (6 downto 0) -- Cathodes signal for display
        );
    end component;
    signal clock_in : std_logic;
    signal reset_timer : std_logic;
    signal d0 : std_logic_vector(3 downto 0);
    signal d1 : std_logic_vector(3 downto 0);
    signal d2 : std_logic_vector(3 downto 0);
    signal d3 : std_logic_vector(3 downto 0);
    signal an : std_logic_vector(3 downto 0);
    signal seg : std_logic_vector(6 downto 0);
begin
    UUT : display_seven_seg port map (clock_in => clock_in, reset_timer => reset_timer,
                                      d0 => d0, d1 => d1, d2 => d2, d3 => d3, an => an, seg => seg);
    clock_proc: process
    begin
        while now < 40000 ns loop
            clk_in_tb <= '0';
            wait for 5 ns;
            clk_in_tb <= '1';
            wait for 5 ns;
        end loop;
        wait;
    end process;

    d0 <= "0000", "0001" after 1024 ns, "0010" after 2048 ns;
    d1 <= "0000", "0001" after 1024 ns, "0010" after 2048 ns;
    d2 <= "0000", "0001" after 1024 ns, "0010" after 2048 ns;
    d3 <= "0000", "0001" after 1024 ns, "0010" after 2048 ns;

    end tb;
