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
    UUT : display_seven_seg port map (
        clock_in => clock_in,
        reset_timer => reset_timer,
        d0 => d0,
        d1 => d1,
        d2 => d2,
        d3 => d3,
        an => an,
        seg => seg
    );

    clock_proc: process
    begin
        while true loop
            clock_in <= '0';
            wait for 5 ns;
            clock_in <= '1';
            wait for 5 ns;
        end loop;
    end process;
    
    sim_proc: process
    begin
        reset_timer <= '1';
        d0 <= "0000";
        d1 <= "0000";
        d2 <= "0000";
        d3 <= "0000";
        wait for 100 ns;
        reset_timer <= '0';
        d0 <= "0000";
        d1 <= "0000";
        d2 <= "0000";
        d3 <= "0000";
        wait for 100 ns;
        d0 <= "0001";
        d1 <= "0001";
        d2 <= "0001";
        d3 <= "0001";
        wait for 100 ns;
        d0 <= "0010";
        d1 <= "0010";
        d2 <= "0010";
        d3 <= "0010";
        wait for 100 ns;
        d0 <= "0011";
        d1 <= "0011";
        d2 <= "0011";
        d3 <= "0011";
        wait for 100 ns;
        d0 <= "0100";
        d1 <= "0100";
        d2 <= "0100";
        d3 <= "0100";
        wait for 100 ns;
        d0 <= "0101";
        d1 <= "0101";
        d2 <= "0101";
        d3 <= "0101";
        wait for 100 ns;
        d0 <= "0110";
        d1 <= "0110";
        d2 <= "0110";
        d3 <= "0110";
        wait for 100 ns;
        d0 <= "0111";
        d1 <= "0111";
        d2 <= "0111";
        d3 <= "0111";
        wait for 100 ns;
        d0 <= "1000";
        d1 <= "1000";
        d2 <= "1000";
        d3 <= "1000";
        wait for 100 ns;
        d0 <= "1001";
        d1 <= "1001";
        d2 <= "1001";
        d3 <= "1001";
        wait for 100 ns;
        d0 <= "1010";
        d1 <= "1010";
        d2 <= "1010";
        d3 <= "1010";
        wait for 100 ns;

    end process;
end tb;    
    
