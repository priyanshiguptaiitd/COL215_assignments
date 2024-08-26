----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/29/2024 04:32:13 PM
-- Design Name: 
-- Module Name: tb_BASIC_gates - tb
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

entity tb_BASIC_gates is
end tb_BASIC_gates;

architecture tb of tb_BASIC_gates is
    -- In this TB modeling Style, the test bench instantiates the DUT as a component
-- and passes the inputs from a separate VHDL process via signals
    component BASIC_gates
        Port ( a_and_in : in STD_LOGIC;
           b_and_in : in STD_LOGIC;
           c_and_out : out STD_LOGIC;
           d_or_in : in STD_LOGIC;
           e_or_in : in STD_LOGIC;
           f_or_out : out STD_LOGIC;
           g_not_in : in STD_LOGIC;
           h_not_out : out STD_LOGIC);
    end component;
    signal a_and_in: std_logic; -- inputs
    signal b_and_in : std_logic; -- inputs
    signal c_and_out: std_logic; -- signals
    signal d_or_in: std_logic; -- inputs
    signal e_or_in : std_logic; -- inputs
    signal f_or_out : std_logic; -- signals
    signal g_not_in: std_logic; -- inputs
    signal h_not_out: std_logic; -- signals

     
    begin
        -- connecting testbench signals with AND_gate.vhd
        UUT : BASIC_gates port map (a_and_in  => a_and_in ,b_and_in  => b_and_in, c_and_out  => c_and_out,
                                    d_or_in => d_or_in , e_or_in => e_or_in,f_or_out => f_or_out,
                                    g_not_in => g_not_in , h_not_out => h_not_out );
        -- inputs
        -- 00 at 0 ns
        -- 01 at 20 ns, as b is 0 at 20 ns and a is changed to 1 at 20 ns
        -- 10 at 40 ns
        -- 11 at 60 ns
        a_and_in  <= '0', '1' after 20 ns, '0' after 40 ns, '1' after 60 ns;
        b_and_in  <= '0', '0' after 20 ns, '1' after 40 ns, '1' after 60 ns;
        d_or_in  <= '0', '1' after 20 ns, '0' after 40 ns, '1' after 60 ns;
        e_or_in  <= '0', '0' after 20 ns, '1' after 40 ns, '1' after 60 ns;
        g_not_in  <= '0', '1' after 20 ns, '0' after 40 ns, '1' after 60 ns;
        
       
end tb;
