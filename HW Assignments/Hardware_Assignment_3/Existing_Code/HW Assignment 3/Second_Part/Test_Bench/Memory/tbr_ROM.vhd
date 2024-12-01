----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 16.10.2024 00:06:06
-- Design Name: 
-- Module Name: tb_ROM - tb
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

entity tbr_ROM is
end tbr_ROM;

architecture tb of tbr_ROM is

    -- Component Declaration for the Unit Under Test (UUT)
    component ROM
        Generic ( DATA_WIDTH : integer := 8;
                  ADDR_WIDTH : integer := 4 );
        Port ( addr : in STD_LOGIC_VECTOR(ADDR_WIDTH-1 downto 0);
               data_out : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0) );
    end component;

    -- Signals for connecting to UUT
    signal addr : STD_LOGIC_VECTOR(4-1 downto 0) := (others => '0');
    signal data_out : STD_LOGIC_VECTOR(8-1 downto 0) := (others => '0');

begin

    -- Instantiate the Unit Under Test (UUT)
    uut: ROM
        Generic map (
            DATA_WIDTH => 8,
            ADDR_WIDTH => 4
        )
        Port map (
            addr => addr,
            data_out => data_out
        );

    -- Stimulus process
    stim_proc: process
    begin
        -- Test different addresses
        for i in 0 to 15 loop
            addr <= std_logic_vector(to_unsigned(i, 4));
            wait for 10 ns;
        end loop;

        -- End simulation
        wait;
    end process;

end tb;