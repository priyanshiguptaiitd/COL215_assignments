library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

----------------------------------------------------------------------------------------------------

entity AES_Round is
    Port ( clk : in std_logic;
           rst : in std_logic;
           start : in std_logic;
           data : in std_logic_vector(127 downto 0);
           key : in std_logic_vector(127 downto 0); 
           result : out std_logic_vector(127 downto 0);
           done : out std_logic
        );
end AES_Round;

----------------------------------------------------------------------------------------------------

architecture arch_AES of AES_Round is

----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_AddRoundKey

    component AES_AddRoundKey
        Port ( en : in std_logic;
               input1 : in std_logic_vector(7 downto 0);
               input2 : in std_logic_vector(7 downto 0);
               output : out std_logic_vector(7 downto 0)
            );
    end component;

    signal input_ARK1 : std_logic_vector(7 downto 0);
    signal input_ARK2 : std_logic_vector(7 downto 0);
    signal output_ARK : std_logic_vector(7 downto 0);
    signal ark_ready : std_logic;   
    signal en_ARK : std_logic;

    signal ready_for_output_ARK : std_logic := '0';    -- Signal to indicate when output data is ready to be written to temp_RAM
    signal counter_ARK_ARK : integer := 0;                 -- Counter_ARK to keep track of processing steps in S1
    signal data_ready_ARK : std_logic := '0';          -- Signal indicating when data_out_RAM is valid after read

----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_ShiftRows

    component AES_ShiftRows
        
        generic (
            S : integer := 4
        );

        Port ( en : in std_logic;
               input_data : in std_logic_vector(31 downto 0);
               shift_bytes : in integer;
               output_data : out std_logic_vector(31 downto 0)
            );
    end component;

    signal input_SR : std_logic_vector(31 downto 0);
    signal output_SR : std_logic_vector(31 downto 0);
    signal en_SR : std_logic;
    signal shift_bytes_SR : integer;


----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_MixColumns

    component AES_MixColumns
        
        generic (
            S : integer := 4
        );

        Port ( en : in std_logic;
               input_data_a : in std_logic_vector(31 downto 0);
               input_data_b : in std_logic_vector(31 downto 0);
               output_data : out std_logic_vector(7 downto 0)
            );

    end component;

    signal input_data_a_MC : std_logic_vector(31 downto 0);
    signal input_data_b_MC : std_logic_vector(31 downto 0);
    signal output_data_MC : std_logic_vector(31 downto 0);
    signal en_MC : std_logic;

----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_SubBytes

    component AES_SubBytes
        
        generic (
            S : integer := 4
        );

        Port ( en : in std_logic;
               input_data : in std_logic_vector(31 downto 0);
               output_data : out std_logic_vector(31 downto 0)
            );

    end component;

    signal input_SB : std_logic_vector(31 downto 0);
    signal output_SB : std_logic_vector(31 downto 0);
    signal en_SB : std_logic;


----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_Key
   
    component AES_Key is
        Port ( clk : in std_logic;
               reset : in std_logic;
               round_num : in std_logic_vector(3 downto 0);
               round_key : out std_logic_vector(127 downto 0)
            );
    end component;

    signal clk_key : std_logic;
    signal reset_key : std_logic;
    signal round_num_key :  std_logic_vector(4 downto 0);
    signal round_key : std_logic_vector(127 downto 0);
    

----------------------------------------------------------------------------------------------------
-- Component Declaration for RAM

    component RAM is
        generic (
            DATA_WIDTH : integer := 8;  -- Width of data bus
            ADDR_WIDTH : integer := 4    -- Width of address bus
        );
        port (
            clk     : in std_logic;                                     -- Clock input
            we      : in std_logic;                                     -- Write enable
            addr    : in std_logic_vector(ADDR_WIDTH-1 downto 0);       -- Address input
            data_in : in std_logic_vector(DATA_WIDTH-1 downto 0);       -- Data input
            data_out: out std_logic_vector(DATA_WIDTH-1 downto 0)       -- Data output
        );
    end component;

    signal data_in_RAM : std_logic_vector(7 downto 0);
    signal data_out_RAM : std_logic_vector(7 downto 0);
    signal addr_RAM : std_logic_vector(3 downto 0);
    signal we_RAM : std_logic;
    signal clk_RAM : std_logic;
    
    signal data_in_RAM_temp : std_logic_vector(7 downto 0);
    signal data_out_RAM_temp : std_logic_vector(7 downto 0);
    signal addr_RAM_temp : std_logic_vector(3 downto 0);
    signal we_RAM_temp : std_logic;
    signal clk_RAM_temp : std_logic;

----------------------------------------------------------------------------------------------------
-- FSM Declaration
    type state_type is (S0, INIT, AddRoundKey, ADDRoundKey_rd,ADDRoundKey_pr,S8 , S9, S10, S11, S12, S13, S14, S15, S16);
    signal state, next_state : state_type;
    signal init_counter_ARK : integer range 0 to 15 := 0 ;
    signal start_copy : std_logic := '0' ;
    
    
begin

----------------------------------------------------------------------------------------------------
-- UUT and Port Mapping for AES_AddRoundKey
    uut_ARK : AES_AddRoundKey
        
        port map (en => en_ARK,
                  input1 => input_ARK1,
                  input2 => input_ARK2,
                  output => output_ARK
                 );

----------------------------------------------------------------------------------------------------
-- UUT and Port Mapping for AES_ShiftRows

    uut_ASR : AES_ShiftRows
        generic map (S => 4)

        port map (en => en_SR,
                  input_data => input_SR,
                  shift_bytes => shift_bytes_SR,
                  output_data => output_SR
                 );

----------------------------------------------------------------------------------------------------
-- UUT and Port Mapping for AES_MixColumns

    uut_AMC : AES_MixColumns
        generic map (S => 4)

        port map (en => en_MC,
                  input_data_a => input_data_a_MC,
                  input_data_b => input_data_b_MC,
                  output_data => output_data_MC
                 );

----------------------------------------------------------------------------------------------------
-- UUT and Port Mapping for AES_SubBytes

    uut_ASB : AES_SubBytes
        generic map (S => 1)

        port map (en => en_SB,
                  input_data => input_SB,
                  output_data => output_SB
                 );

----------------------------------------------------------------------------------------------------
-- UUT and Port Mapping for AES_Key

    uut_key : AES_Key
        
        port map (
                  clk => clk_key,
                  reset => reset_key,
                  round_num => round_num_key,
                  round_key => round_key
                 );

----------------------------------------------------------------------------------------------------
-- UUT and Port Mapping for RAM

    uut_RAM : RAM
        generic map (
            DATA_WIDTH => 8,
            ADDR_WIDTH => 4
        )
        port map (
            clk => clk_RAM,
            we => we_RAM,
            addr => addr_RAM,
            data_in => data_in_RAM,
            data_out => data_out_RAM
        );
    
    uut_RAM_temp : RAM
        generic map (
            DATA_WIDTH => 8,
            ADDR_WIDTH => 4
        )
        port map (
            clk => clk_RAM_temp,
            we => we_RAM_temp,
            addr => addr_RAM_temp,
            data_in => data_in_RAM_temp,
            data_out => data_out_RAM_temp
        );
    
----------------------------------------------------------------------------------------------------

clk_key <= clk;
clk_RAM <= clk;
clk_RAM_temp <= clk;


-- Starting FSM Process for processing a given Round

    process(clk, rst)
    begin
        if(rst = '1') then
            state <= S0;
            done <= '0';
            start_copy <= '0';
            init_counter <= 0;
        
        elsif (rising_edge(clk)) then
            
            case state is
                
                when S0 => 
                    if(start = '1') then
                        state <= INIT;
                        start_copy <= '1';  
                    end if;
                
                when INIT =>
                    if(start_copy = '1') then
                        we_RAM <= '1';
                        addr_RAM <= "0000";
                        data_in_RAM <= data(127 -(init_counter * 8) downto 120 - (init_counter * 8));
                        init_counter <= init_counter + 1;

                        if(init_counter = 15) then
                            start_copy <= '0';
                            we_RAM <= '0';
                            init_counter <= 0;
                            state <= S1;
                        end if;

                    end if;
                
                when ADDRoundKey =>
                    state <= s0;
                    if counter_ARK < 16 then  -- Process 16 bytes (8-bit data * 16)
                        -- Step 1: Enable reading from RAM
                        read_en <= '1'; 
                        addr_RAM <= std_logic_vector(to_unsigned(counter_ARK, 4)); -- Set address in RAM
                        state <= ADDRoundKey_rd;  -- Transition to a delay state to wait for valid data

                    else
                        -- All bytes processed, move to next state
                        counter_ARK <= 0;
                        state <= S2;  -- Proceed to the next state after S1
                    end if;
                
                when ADDRoundKey_rd =>
                    -- Wait for data_out_RAM to be valid, then proceed with processing
                    data_ready_ARK <= '1';  -- Signal that data is ready for processing in the next cycle
                    state <= ADDRoundKey_pr;  -- Move to processing state
                
                when ADDRoundKey_pr =>
                    if(data_ready_ARK = '1') then
                        -- Step 2: Feed RAM data to AES_AddRoundKey component
                        input_ARK1 <= data_out_RAM;     -- Read data from RAM (now valid)
                        input_ARK2 <= round_key((127 - (counter * 8)) downto (120 - (counter * 8))); -- Select 8 bits of round key
                        en_ARK <= '1';                  -- Enable AES_AddRoundKey operation
                        ready_for_output_ARK <= '0';        -- Reset ready signal until operation completes
                        data_ready <= '0';              -- Reset data_ready for the next byte

                    -- Step 3: Wait for AES_AddRoundKey to complete, then prepare to store result
                    if en_ARK = '1' then
                        -- After one clock cycle, AES_AddRoundKey operation completes
                        ready_for_output_ARK <= '1';     -- Indicate that data is ready for writing to temp_RAM
                        en_ARK <= '0';               -- Disable further AES_AddRoundKey until next cycle
                    
                    end if;

                    -- Step 4: Write processed data to temp_RAM if ready
                    if ready_for_output_ARK = '1' then
                        
                        we_temp <= '1';        -- Enable writing to temp_RAM
                        addr_RAM_temp <= std_logic_vector(to_unsigned(counter_ARK, 4)); -- Target address in temp_RAM
                        data_in_RAM_temp <= output_ARK;  -- Write output from AES_AddRoundKey to temp_RAM
                        ready_for_output_ARK <= '0';     -- Reset ready signal for next cycle
                        counter_ARK <= counter_ARK + 1;      -- Move to next byte
                        state <= S1;                 -- Return to S1 for the next byte
                        
                    end if;

                end if;
                
                when others =>
                    state <= S0;
            end case;
        end if;
    end process;
                        
end arch_AES;