----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/29/2024 02:55:15 PM
-- Design Name: 
-- Module Name: tb_AND_gate - tb
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity tb_AND_gate is
end tb_AND_gate;

architecture tb of tb_AND_gate is
    -- In this TB modeling Style, the test bench instantiates the DUT as a component
-- and passes the inputs from a separate VHDL process via signals
    component NOT_gate
        Port ( a : in STD_LOGIC;
                c : out STD_LOGIC);
    end component;
    signal a: std_logic; -- inputs
    signal c : std_logic; -- signal 

    begin
        -- connecting testbench signals with AND_gate.vhd
        UUT : NOT_gate port map (a => a,c => c);
        -- inputs
        -- 00 at 0 ns
        -- 01 at 20 ns, as b is 0 at 20 ns and a is changed to 1 at 20 ns
        -- 10 at 40 ns
        -- 11 at 60 ns
        a <= '0', '1' after 20 ns, '0' after 40 ns, '1' after 60 ns;
        
end tb;
