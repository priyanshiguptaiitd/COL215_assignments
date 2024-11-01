library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gf256_multiply is
  port (
    a       : in std_logic_vector(7 downto 0);  -- First 8-bit input
    b       : in std_logic_vector(7 downto 0);  -- Second 8-bit input
    ctrl_gf256     : in std_logic; 
    result  : out std_logic_vector(7 downto 0)  -- Result of GF(2^8) multiplication
  );
end entity gf256_multiply;

architecture Behavioral of gf256_multiply is
  -- Declare the irreducible polynomial for GF(2^8)
  constant reduction_poly : std_logic_vector(8 downto 0) := "100011011";  -- x^8 + x^4 + x^3 + x + 1 (0x11B)
  
  -- Function to perform GF(2^8) multiplication
  function gf256_mult (x, y: std_logic_vector(7 downto 0)) return std_logic_vector is
    variable product: std_logic_vector(15 downto 0) := (others => '0');  -- Intermediate 16-bit result
    variable a_temp: std_logic_vector(7 downto 0) := x;  -- Copy of 'x'
    variable i: integer;
  begin
    -- Perform the multiplication using shift-and-add method
    for i in 0 to 7 loop
      if y(i) = '1' then
        product(7 downto 0) := product(7 downto 0) xor a_temp;  -- Add shifted value of 'x'
      end if;
      
      -- Shift 'a_temp' left by 1 (multiply by x) and reduce if necessary
      if a_temp(7) = '1' then  -- Check if highest bit is set
        a_temp := (a_temp(6 downto 0) & '0') xor reduction_poly(7 downto 0);  -- Shift left and apply reduction
      else
        a_temp := a_temp(6 downto 0) & '0';  -- Just shift left
      end if;
    end loop;
    
    -- Return the lower 8 bits of the product (since we are in GF(2^8))
    return product(7 downto 0);
  end function gf256_mult;

begin
  -- Call the GF(2^8) multiplication function
  process (a, b, ctrl_gf256)
  begin
    if(ctrl_gf256 = '1') then
      result <= gf256_mult(a, b);
    else
      result <= (others => '0');
    end if;
  end process;
  
end architecture Behavioral;
