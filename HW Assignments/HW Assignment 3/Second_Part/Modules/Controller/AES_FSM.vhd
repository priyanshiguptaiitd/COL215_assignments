library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity AES_Sequential is
    
    Port ( 
        clk         : in  STD_LOGIC;
        reset       : in  STD_LOGIC;
        start       : in  STD_LOGIC;
        data_in     : in  STD_LOGIC_VECTOR(127 downto 0);
        data_out    : out STD_LOGIC_VECTOR(127 downto 0);
        done        : out STD_LOGIC
    );

end AES_Sequential;

architecture Behavioral of AES_Sequential is

--------------------------------------------------------------------------------------------------------------------- -- Component for bitwise_xor
    
    component bitwise_xor is
        generic (
                DW : integer := 1;  -- Data_Width (1 Byte / 8 bits by default)
                N : integer := 8  -- Number of Elements (16 Bytes by default)
            );
        port (
            input_a : in std_logic_vector(DW*N-1 downto 0);
            input_b : in std_logic_vector(DW*N-1 downto 0);
            res: out std_logic_vector(DW*N-1 downto 0)
        );
    end component;

    signal input_a_bwx : std_logic_vector(8*1-1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
    signal input_b_bwx : std_logic_vector(8*1-1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
    signal res_bwx : std_logic_vector(8*1-1 downto 0);  -- Output result array (16 bytes)   
    
---------------------------------------------------------------------------------------------------------------------  -- Component for Inverse_Mix_Columns   
        port (
          clk        : in std_logic;
          reset      : in std_logic;
          start_calc : in std_logic;  -- Trigger new calculation
          input_a    : in std_logic_vector(31 downto 0);  -- Example: 4 bytes
          input_b    : in std_logic_vector(31 downto 0);  -- Example: 4 bytes
          result_out : out std_logic_vector(7 downto 0);  -- One byte result
          calc_done  : out std_logic
        );
    end component;

    signal clk_gf : std_logic := '0';
    signal reset_gf : std_logic := '0';
    signal start_calc_gf : std_logic := '0';
    signal input_a_gf : std_logic_vector(31 downto 0);
    signal input_b_gf : std_logic_vector(31 downto 0);
    signal result_out_gf : std_logic_vector(7 downto 0);
    signal calc_done_gf : std_logic;

---------------------------------------------------------------------------------------------------------------------  -- -- Component for Inv_Sub_Bytes 
    
    component Inv_Sub_Bytes_8 is             
        Generic ( 
                  S : integer := 1;  -- Data width (bits per entry)
                  N : integer := 8   -- Number of elements to be processed
                );
        
        Port(   
                -- clk : in std_logic;
                data_input : in std_logic_vector(S * N - 1 downto 0);
                ctrl_isb : in std_logic;
                data_output : out std_logic_vector(S * N - 1 downto 0)
        );
    
    end component;

    signal data_input_isb : std_logic_vector(8 * 1 - 1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
    signal ctrl_isb : std_logic; -- Control signal
    signal data_output_isb : std_logic_vector(8 * 1 - 1 downto 0); -- Output result array (16 bytes)

--------------------------------------------------------------------------------------------------------------------- -- -- Component for Inv_Row_Shift
    
    component inv_row_shift is                 
        generic (
          S : integer := 4; -- Number of Bytes in a row
        ); 
      
        port (
          input_data : in std_logic_vector(8 * S - 1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
          shift_bytes : in integer; -- Number of bytes to shift
          output_data : out std_logic_vector(8 * S - 1 downto 0) -- Output result array (16 bytes)
        );
    end component; 

    signal input_data_irs : std_logic_vector(8 * 4 - 1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
    signal shift_bytes_irs : integer; -- Number of bytes to shift
    signal output_data_irs : std_logic_vector(8 * 4 - 1 downto 0); -- Output result array (16 bytes)


--------------------------------------------------------------------------------------------------------------------- -- Component for RAM
    
    component RAM
        Generic ( DATA_WIDTH_RAM : integer := 8;
                  ADDR_WIDTH_RAM : integer := 8);
        Port ( clk : in  STD_LOGIC;
               we  : in  STD_LOGIC;
               addr: in  STD_LOGIC_VECTOR (ADDR_WIDTH_RAM-1 downto 0);
               din  : in  STD_LOGIC_VECTOR (DATA_WIDTH_RAM-1 downto 0);
               dout : out STD_LOGIC_VECTOR (DATA_WIDTH_RAM-1 downto 0));
    end component;


    signal clk_ram_main : STD_LOGIC := '0';
    signal we_ram_main  : STD_LOGIC := '0';
    signal addr_ram_main: STD_LOGIC_VECTOR (7 downto 0) := (others => '0');
    signal din_ram_main  : STD_LOGIC_VECTOR (7 downto 0) := (others => '0');
    signal dout_ram_main : STD_LOGIC_VECTOR (7 downto 0) := (others => '0');
    
    signal clk_ram_temp : STD_LOGIC := '0';
    signal we_ram_temp  : STD_LOGIC := '0';
    signal addr_ram_temp: STD_LOGIC_VECTOR (7 downto 0) := (others => '0');
    signal din_ram_temp  : STD_LOGIC_VECTOR (7 downto 0) := (others => '0');
    signal dout_ram_temp : STD_LOGIC_VECTOR (7 downto 0) := (others => '0');

    constant clk_period : time := 10 ns;

--------------------------------------------------------------------------------------------------------------------- -- State machine type definition
    -- State machine type definition

    type state_type is (IDLE, XOR_KEY, INV_MIX_COLS, INV_SHIFT_ROWS, INV_SUB_BYTES, FINAL_XOR, COMPLETE);
    signal current_state, next_state : state_type;

    -- Counter for XOR operations
    signal xor_count : integer range 0 to 8;
    signal reg_32_in : std_logic_vector(31 downto 0);
    signal reg_32_out : std_logic_vector(31 downto 0);
    signal reg_8_in : std_logic_vector(7 downto 0);
    signal reg_8_out : std_logic_vector(7 downto 0);
    -- Internal data registers

---------------------------------------------------------------------------------------------------------------------
    
begin
    -- Sequential process for state register and counter

    uut_RAM_main: RAM Generic map ( DATA_WIDTH_RAM => 8, ADDR_WIDTH_RAM => 8)
            Port map (
            clk => clk_ram_main,
            we => we_ram_main,
            addr => addr_ram_main,
            din => din_ram_main,
            dout => dout_ram_main
        );

    uut_RAM_temp: RAM Generic map ( DATA_WIDTH_RAM => 8, ADDR_WIDTH_RAM => 8)
            Port map (
            clk => clk_ram_temp,
            we => we_ram_temp,
            addr => addr_ram_temp,
            din => din_ram_temp,
            dout => dout_ram_temp
        );
    
    uut_bitwise_xor: bitwise_xor Generic map ( DW => 8, N => 1)
            Port map (
            input_a => input_a_bwx,
            input_b => input_b_bwx,
            res => res_bwx
        );
    
    uut_gf256_controller: gf256_controller
            port map (
            clk => clk_gf,
            reset => reset_gf,
            start_calc => start_calc_gf,
            input_a => input_a_gf,
            input_b => input_b_gf,
            result_out => result_out_gf,
            calc_done => calc_done_gf
        );
    
    uut_Inv_Sub_Bytes_8: Inv_Sub_Bytes_8 Generic map( S => 8, N => 1)
            Port map (
            data_input => data_input_isb,
            ctrl_isb => ctrl_isb,
            data_output => data_output_isb
        );

    uut_inv_row_shift: inv_row_shift Generic map( S => 4)
            Port map (
            input_data => input_data_irs,
            shift_bytes => shift_bytes_irs,
            output_data => output_data_irs
        );
    
    
    process(clk, reset)
    begin
        if reset = '1' then
            
            current_state <= IDLE;
            xor_count <= 0;
            reg_32_in <= (others => '0');
            reg_32_out <= (others => '0');
            reg_8_in <= (others => '0');
            reg_8_out <= (others => '0');

        elsif rising_edge(clk) then

            current_state <= next_state;
            
            case current_state is
                when IDLE =>
                    
                    if start = '1' then
                        addr_ram_main <= data_in(127 downto 120);
                        din_ram_main <= data_in(119 downto 112);
                        we_ram_main <= '1';
                    else
                        we_ram_main <= '0';
                    end if;
                
                when XOR_KEY =>
                    
                    data_reg <= data_reg xor round_key;
                    if xor_count < 8 then
                        xor_count <= xor_count + 1;
                    end if;
                
                when INV_MIX_COLS =>
                    -- Add your InvMixColumns implementation here
                    -- data_reg <= InvMixColumns(data_reg);
                    
                when INV_SHIFT_ROWS =>
                    -- Add your InvShiftRows implementation here
                    -- data_reg <= InvShiftRows(data_reg);
                    
                when INV_SUB_BYTES =>
                    -- Add your InvSubBytes implementation here
                    -- data_reg <= InvSubBytes(data_reg);
                    
                when FINAL_XOR =>
                    data_reg <= data_reg xor round_key;
                    
                when others =>
                    null;
            end case;
        end if;
    end process;

    -- Combinational process for next state logic
    process(current_state, start, xor_count)
    begin
        next_state <= current_state;  -- Default: stay in current state
        done <= '0';  -- Default output
        
        case current_state is

            when IDLE =>
                if start = '1' then
                    next_state <= XOR_KEY;
                end if;
                
            when XOR_KEY =>
                if xor_count = 8 then
                    next_state <= INV_MIX_COLS;
                end if;
                
            when INV_MIX_COLS =>
                next_state <= INV_SHIFT_ROWS;
                
            when INV_SHIFT_ROWS =>
                next_state <= INV_SUB_BYTES;
                
            when INV_SUB_BYTES =>
                next_state <= FINAL_XOR;
                
            when FINAL_XOR =>
                next_state <= COMPLETE;
                
            when COMPLETE =>
                done <= '1';
                if start = '0' then
                    next_state <= IDLE;
                end if;
            
        end case;
    end process;

    -- Output assignment
    data_out <= data_reg;
    
end Behavioral;