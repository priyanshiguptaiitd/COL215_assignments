----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 21.10.2024 15:03:28
-- Design Name: 
-- Module Name: tb_ROMSBOX - tb
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tb_ROMSBOX is
end tb_ROMSBOX;

architecture tb of tb_ROMSBOX is

    -- Component Declaration for the Unit Under Test (UUT)
    component ROM_SBOX
        Generic ( DATA_WIDTH : integer := 8;
                  ADDR_WIDTH : integer := 8);
        Port ( addr : in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
               data_out : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0) );
    end component;

    -- Signals for connecting to UUT
    signal addr : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');
    signal data_out : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: ROM_SBOX
        Generic map (
            DATA_WIDTH => 8,
            ADDR_WIDTH => 8
        )
        Port map (
            addr => addr,
            data_out => data_out
        );

    -- Stimulus process
    stim_proc: process
    begin
        -- Test different addresses
        for i in 0 to 255 loop
            addr <= std_logic_vector(to_unsigned(i, 8));
            wait for 10 ns;
        end loop;

        -- End simulation
        wait;
    end process;

end tb;