library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity AES_Sequential is
    Port ( 
        clk         : in  STD_LOGIC;
        reset       : in  STD_LOGIC;
        start       : in  STD_LOGIC;
        data_in     : in  STD_LOGIC_VECTOR(127 downto 0);
        round_key   : in  STD_LOGIC_VECTOR(127 downto 0);
        done        : out STD_LOGIC;
        data_out    : out STD_LOGIC_VECTOR(127 downto 0)
    );
end AES_Sequential;

architecture Behavioral of AES_Sequential is
    -- State machine type definition
    type state_type is (IDLE, XOR_KEY, INV_MIX_COLS, INV_SHIFT_ROWS, INV_SUB_BYTES, FINAL_XOR, COMPLETE);
    signal current_state, next_state : state_type;
    
    -- Counter for XOR operations
    signal xor_count : integer range 0 to 8;
    
    -- Internal data registers
    signal data_reg : STD_LOGIC_VECTOR(127 downto 0);
    
begin
    -- Sequential process for state register and counter
    process(clk, reset)
    begin
        if reset = '1' then
            current_state <= IDLE;
            xor_count <= 0;
            data_reg <= (others => '0');
        elsif rising_edge(clk) then
            current_state <= next_state;
            
            case current_state is
                when IDLE =>
                    if start = '1' then
                        data_reg <= data_in;
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