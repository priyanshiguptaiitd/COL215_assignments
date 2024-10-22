----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 21.10.2024 15:58:12
-- Design Name: 
-- Module Name: Inv_Sub_Bytes - Behavioral
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity Inv_Sub_Bytes is

    Generic ( 
              DATA_WIDTH_SB : integer := 8;  -- Data width -- Depending upon data of a single Entry  (number of bits)
              ADDR_WIDTH_SB : integer := 8   -- Address width -- Depending upon Number of Elements to be processed (number of bits)
            );
    
    Port(
            data_input : in std_logic_vector(ADDR_WIDTH_SB-1 downto 0);
            data_output : out std_logic_vector(DATA_WIDTH_SB-1 downto 0)
    );        
    
end Inv_Sub_Bytes;

architecture Behavioral of Inv_Sub_Bytes is
    component ROM_SBOX
    Generic ( DATA_WIDTH : integer := DATA_WIDTH_SB;  -- Data width -- Depending upon data of a single Entry  (number of bits)
              ADDR_WIDTH : integer := ADDR_WIDTH_SB   -- Address width -- Depending upon Number of Elements to be processed (number of bits)
    );
    Port ( 
            addr : in STD_LOGIC_VECTOR(ADDR_WIDTH_SB-1 downto 0);
            data_out : out STD_LOGIC_VECTOR(DATA_WIDTH_SB-1 downto 0)
    );
    end component;
begin
    uut: ROM_SBOX
        Generic map (
            DATA_WIDTH => DATA_WIDTH_SB,
            ADDR_WIDTH => ADDR_WIDTH_SB
        )
        Port map (
            addr => data_input,
            data_out => data_output
        );
end Behavioral;