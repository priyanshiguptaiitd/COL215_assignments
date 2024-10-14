----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/14/2024 03:07:52 PM
-- Design Name: 
-- Module Name: ROM - Behavioral
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
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity ROM is

    Port ( 
           address : in STD_LOGIC_VECTOR(7 downto 0);
           data_out : out STD_LOGIC_VECTOR(7 downto 0)
         );
         
end ROM;

architecture Behavioral of ROM is

    component dist_mem_gen_256_8_rom
        Port ( a : in STD_LOGIC_VECTOR(7 downto 0);
               spo : out STD_LOGIC_VECTOR(7 downto 0));
    end component;

    signal address_internal : STD_LOGIC_VECTOR(7 downto 0);
    signal data_out_internal : STD_LOGIC_VECTOR(7 downto 0);
    
begin

    UDATA : dist_mem_gen_256_8_rom port map ( a => address_internal, spo => data_out_internal);
    address_internal <= address;
    data_out <= data_out_internal;
    
end Behavioral;












 