library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_inv_sub_bytes is
end tb_inv_sub_bytes;

architecture Behavioral of tb_inv_sub_bytes is

    -- Component Declaration for the Unit Under Test (UUT)
    component Inv_Sub_Bytes
        Generic ( 
                  S : integer := 8;  -- Data width
                  N: integer := 16   -- Address width
                  );
        Port(   
            clk : in std_logic;
            data_input : in std_logic_vector(8*N-1 downto 0);
            data_output : out std_logic_vector(8*N-1 downto 0);
            is_completed : out std_logic
        );
    end component;

    -- Signals for the testbench
    signal clk_tb : std_logic := '0';
    signal data_input_tb : std_logic_vector(8*16-1 downto 0);
    signal data_output_tb : std_logic_vector(8*16-1 downto 0);
    signal is_completed_tb : std_logic := '0';
    -- Clock period definition
    constant clk_period : time := 10 ns;

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: Inv_Sub_Bytes
        Generic map (
            S => 8,
            N => 16
        )
        Port map (
            clk => clk_tb,
            data_input => data_input_tb,
            data_output => data_output_tb,
            is_completed => is_completed_tb
        );

    -- Clock process definitions
    clk_process :process
    begin
        clk_tb <= '0';
        wait for clk_period/2;
        clk_tb <= '1';
        wait for clk_period/2;
    end process;

    -- Stimulus process
    stim_proc: process
    begin
        -- Initialize Inputs
        data_input_tb <= x"00112233445566778899AABBCCDDEEFF";
        
        wait until is_completed_tb = '1';

        -- End simulation
        wait;
    end process;

end Behavioral;