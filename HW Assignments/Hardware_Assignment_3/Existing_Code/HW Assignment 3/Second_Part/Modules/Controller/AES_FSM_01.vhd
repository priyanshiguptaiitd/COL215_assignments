library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity AES_FSM_01 is
    Port ( clk      : in  std_logic;
           rst      : in  std_logic;
           start    : in  std_logic;
           data_in  : in  std_logic_vector(127 downto 0);
           done     : out std_logic;
           debug_we    : out std_logic;
           debug_addr  : out std_logic_vector(4-1 downto 0);
           debug_din   : out std_logic_vector(8-1 downto 0);
           debug_dout  : out std_logic_vector(8-1 downto 0);
           debug_bcount : out integer;
           debug_state : out integer
         );
end AES_FSM_01;

architecture Behavioral of AES_FSM_01 is
    constant DATA_WIDTH_RAM : integer := 8;
    constant ADDR_WIDTH_RAM : integer := 4;

    signal we       : std_logic;
    signal addr     : std_logic_vector(ADDR_WIDTH_RAM-1 downto 0);
    signal din      : std_logic_vector(DATA_WIDTH_RAM-1 downto 0);
    signal dout     : std_logic_vector(DATA_WIDTH_RAM-1 downto 0);

    component RAM is
        generic(
            DATA_WIDTH_RAM : integer := 8;
            ADDR_WIDTH_RAM : integer := 4
        );
        Port ( clk      : in  std_logic;
               we       : in  std_logic;   
               addr     : in  std_logic_vector(ADDR_WIDTH_RAM-1 downto 0); 
               din      : in  std_logic_vector(DATA_WIDTH_RAM-1 downto 0); 
               dout     : out std_logic_vector(DATA_WIDTH_RAM-1 downto 0)  
             );
    end component;

    signal state : integer := 0;
    signal byte_counter : integer := 0;

begin

    debug_we <= we;
    debug_addr <= addr;
    debug_din <= din;
    debug_bcount <= byte_counter;
    debug_state <= state;
    debug_dout <= dout;

    

    RAM_inst : RAM
        port map (
            clk => clk,
            we => we,
            addr => addr,
            din => din,
            dout => dout
        );

    process(clk, rst)
    begin
        if rst = '1' then
            state <= 0;
            byte_counter <= 0;
            done <= '0';
        elsif rising_edge(clk) then
            case state is
                when 0 =>
                    if start = '1' then
                        state <= 1;
                        byte_counter <= 0;
                    end if;
                when 1 =>
                    if byte_counter < 16 then
                        we <= '1';
                        addr <= std_logic_vector(to_unsigned(byte_counter, ADDR_WIDTH_RAM));
                        din <= data_in((byte_counter+1)*8-1 downto byte_counter*8);
                        byte_counter <= byte_counter + 1;
                    else
                        byte_counter <= 0;
                        we <= '0';
                        state <= 2;
                    end if;
                when 2 =>
--                    we <= '0';
                    if(byte_counter < 16) then
                        we <= '0';
                        addr <= std_logic_vector(to_unsigned(byte_counter, ADDR_WIDTH_RAM));
                        byte_counter <= byte_counter + 1;
                    else
                        byte_counter <= 0;
                        done <= '1';
                        state <= 3;
                    end if;
                when 3 =>
                    done <= '1';
                    state <= 0;
                when others =>
                    state <= 0;
            end case;
        end if;
    end process;
end Behavioral;