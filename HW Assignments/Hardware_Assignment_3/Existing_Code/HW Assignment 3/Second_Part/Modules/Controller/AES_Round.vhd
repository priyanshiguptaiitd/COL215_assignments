library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity AES_Logic is
    Port(
        start : in STD_LOGIC;
        state_in : in STD_LOGIC_VECTOR(127 downto 0);
        key_in : in STD_LOGIC_VECTOR(127 downto 0);
        state_out : out STD_LOGIC_VECTOR(127 downto 0);
        done : out STD_LOGIC
    );

end AES_Logic;

architecture Behavioral of AES_Round is

    component RAM is
        
        generic(
        DATA_WIDTH_RAM : integer := 8;
        ADDR_WIDTH_RAM : integer := 4
        );

        Port(
            clk : in STD_LOGIC;
            we : in STD_LOGIC;
            addr : in STD_LOGIC_VECTOR(ADDR_WIDTH_RAM-1 downto 0);
            din : in STD_LOGIC_VECTOR(DATA_WIDTH_RAM-1 downto 0);
            dout : out STD_LOGIC_VECTOR(DATA_WIDTH_RAM-1 downto 0)
        );

    end component;

    component AES_AddRoundKey
        Port(
            state_in : in STD_LOGIC_VECTOR(127 downto 0);
            key_in : in STD_LOGIC_VECTOR(127 downto 0);
            state_out : out STD_LOGIC_VECTOR(127 downto 0);
            en : in STD_LOGIC
        );
    end component;

    component AES_SubBytes
        Port(
            state_in : in STD_LOGIC_VECTOR(127 downto 0);
            state_out : out STD_LOGIC_VECTOR(127 downto 0);
            en : in STD_LOGIC
        );
    end component;

    component AES_ShiftRows
        Port(
            state_in : in STD_LOGIC_VECTOR(127 downto 0);
            state_out : out STD_LOGIC_VECTOR(127 downto 0);
            en : in STD_LOGIC
        );
    end component;

    component AES_MixColumns
        Port(
            state_in : in STD_LOGIC_VECTOR(127 downto 0);
            state_out : out STD_LOGIC_VECTOR(127 downto 0);
            en : in STD_LOGIC
        );
    end component;

    component register_n_bit is
        generic (
            N : integer := 8
        );
        port (
            clk     : in  std_logic;
            reset   : in  std_logic;
            enable  : in  std_logic;
            d_in    : in  std_logic_vector(N-1 downto 0);
            q_out   : out std_logic_vector(N-1 downto 0)
        );
    end component;

    

    type state_type is (IDLE,INIT , ADDROUNDKEY, SUBBYTES, SHIFTROWS, MIXCOLUMNS); 
    
    signal state , next_state : state_type;
    signal addr_counter : integer range 0 to 15 := 0;
    signal 

begin



end Behavioral;