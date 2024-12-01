library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_AES_MixColumns is
end tb_AES_MixColumns;

architecture behavior of tb_AES_MixColumns is

    -- Component Declaration for the Unit Under Test (UUT)
    component AES_MixColumns
        generic (
            S : integer := 4
        );
        port (
            en : in std_logic;
            input_data_a : in std_logic_vector(8 * S - 1 downto 0);
            input_data_b : in std_logic_vector(8 * S - 1 downto 0);
            output_data : out std_logic_vector(8 - 1 downto 0)
        );
    end component;

    -- Signals for the UUT
    signal en : std_logic := '0';
    signal input_data_a : std_logic_vector(31 downto 0) := (others => '0');
    signal input_data_b : std_logic_vector(31 downto 0) := (others => '0');
    signal output_data : std_logic_vector(7 downto 0);

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: AES_MixColumns
        port map (
            en => en,
            input_data_a => input_data_a,
            input_data_b => input_data_b,
            output_data => output_data
        );

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize Inputs
        en <= '0';
        input_data_a <= x"00112233";
        input_data_b <= x"44556677";
        wait for 10 ns;

        -- Enable the operation
        en <= '1';
        wait for 10 ns;

        -- Change input data
        input_data_a <= x"89abcdef";
        input_data_b <= x"01234567";
        wait for 10 ns;

        -- Disable the operation
        en <= '0';
        wait for 10 ns;

        -- Finish simulation
        wait;
    end process;

end behavior;