library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.numeric_std.all;

entity AES_Controller is
    
    Port ( clk : in STD_LOGIC;
           reset : in STD_LOGIC;
           start : in STD_LOGIC;
           result : out STD_LOGIC_VECTOR(127 downto 0);
--           temp_res : out std_logic_vector(127 downto 0);
--           temp_key : out std_logic_vector(127 downto 0);
           done : out STD_LOGIC);

end AES_Controller;

architecture Behavioral of AES_Controller is

----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_ShiftRows

    component AES_ShiftRows is
        
        generic (
            S : integer := 4 -- Number of Bytes in a row
        );
        
        port (
            en : in std_logic;
            input_data : in std_logic_vector(8 * S - 1 downto 0);  -- Input array (N x 8-bit elements, 16 bytes)
            shift_bytes : in integer; -- Number of bytes to shift (Must lie from 0 to S-1)
            output_data : out std_logic_vector(8 * S - 1 downto 0) -- Output result array (16 bytes)
        );

    end component;
    
    signal input_SR : std_logic_vector(31 downto 0);
    signal output_SR : std_logic_vector(31 downto 0);
    signal en_SR : std_logic;
    signal sr_ready : std_logic := '0';
    signal shift_bytes_SR : integer;

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
    signal ark_ready : std_logic := '0';   
    signal en_ARK : std_logic;
    signal ark_counter : integer range 0 to 15 := 0;  
    
----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_SubBytes

    component AES_SubBytes
            
        generic (
            S : integer := 1;
            N : integer := 8
        );

        Port ( 
            data_input : in std_logic_vector(7 downto 0);
            en : in std_logic;
            data_output : out std_logic_vector(7 downto 0)
            );

    end component;

    signal input_SB : std_logic_vector(7 downto 0);
    signal output_SB : std_logic_vector(7 downto 0);
    signal sb_ready : std_logic := '0';
    signal en_SB : std_logic;

----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_Round

    component AES_Round is
        
        Port (  clk : in std_logic;
                rst : in std_logic;  
                start : in std_logic;
                data : in std_logic_vector(127 downto 0);
                round_key : in std_logic_vector(127 downto 0); 
        --           tempval : out std_logic_vector(127 downto 0);
        --           temp_inpisb : out std_logic_vector(7 downto 0);
        --           temp_outisb : out std_logic_vector(7 downto 0);
        --           temp_input_data_a_MC : out std_logic_vector(31 downto 0);
        --           temp_input_data_b_MC : out std_logic_vector(31 downto 0);
        --           temp_output_data_MC : out std_logic_vector(7 downto 0);           
                result : out std_logic_vector(127 downto 0);
                done : out std_logic
            );

    end component;

    -- signal clk_round : std_logic;
    signal rst_round : std_logic := '1';
    signal start_round : std_logic := '0';
    signal result_round : std_logic_vector(127 downto 0);
    signal done_round : std_logic;
    signal start_process_round : std_logic_vector(1 downto 0) := "00";

----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_Key

    component AES_Key is
        
        Generic ( 
                S : integer := 1;  -- Data width (bits per entry)
                N : integer := 8  -- Number of elements to be processed
                );
        
        Port(   
                -- clk : in std_logic;
                data_input : in std_logic_vector(S * N - 1 downto 0);
                en : in std_logic;
                data_output : out std_logic_vector(S * N - 1 downto 0)
        );

    end component;

    signal input_key : std_logic_vector(7 downto 0);
    signal output_key : std_logic_vector(7 downto 0);
    signal en_key : std_logic;
    signal key_ready : std_logic := '0';
    
    signal key_counter : integer range 0 to 15 := 0;

----------------------------------------------------------------------------------------------------
-- Component Declaration for AES_Text
    
    component AES_Text is

        Generic ( 
                S : integer := 4;  -- Input Data width (bits per entry)
                N : integer := 8  -- Output Data width (bits per entry)
                );
        
        Port(   
                -- clk : in std_logic;
                data_input : in std_logic_vector(S - 1 downto 0);
                en : in std_logic;
                data_output : out std_logic_vector(N - 1 downto 0)
        );
        
    end component;
    
        signal input_text : std_logic_vector(3 downto 0);
        signal output_text : std_logic_vector(7 downto 0);
        signal en_text : std_logic;

        signal text_ready : std_logic := '0';
        signal text_counter : integer range 0 to 15 := 0;

----------------------------------------------------------------------------------------------------
-- AES FSM Signals begin here

    type state_type is (S0, PrepareData, PrepareKey, AddRoundKey, InvShiftRows , InvSubBytes, RoundLogic, FinalAddRoundKey, SF);
    
    signal state : state_type;
    signal round_counter : integer range 0 to 9 := 0;
    signal round_key : std_logic_vector(127 downto 0);
    signal round_data : std_logic_vector(127 downto 0);
    signal we_done : std_logic := '0';




----------------------------------------------------------------------------------------------------
-- Controller Logic Begins Here

begin
--temp_res <= round_data;
--temp_key <= round_key;
----------------------------------------------------------------------------------------------------
-- Instantiate AES_ShiftRows

    uut_SR: AES_ShiftRows
        generic map (
            S => 4
        )
        port map (
            en => en_SR,
            input_data => input_SR,
            shift_bytes => shift_bytes_SR,
            output_data => output_SR
        );

----------------------------------------------------------------------------------------------------
-- Instantiate AES_AddRoundKey
    
    uut_ARK : AES_AddRoundKey
            
    port map (en => en_ARK,
            input1 => input_ARK1,
            input2 => input_ARK2,
            output => output_ARK
            );

----------------------------------------------------------------------------------------------------
-- Instantiate AES_SubBytes

    uut_ASB : AES_SubBytes

    generic map (S => 1)

    port map (
            en => en_SB,
            data_input => input_SB,
            data_output => output_SB
            );

----------------------------------------------------------------------------------------------------
-- Instantiate AES_Round

    uut_round : AES_Round

    port map (
            clk => clk,
            rst => rst_round,
            start => start_round,
            data => round_data,
            round_key => round_key,
            result => result_round,
            done => done_round
            );

----------------------------------------------------------------------------------------------------
-- Instantiate AES_Key

    uut_key : AES_Key

    generic map (S => 1, N => 8)

    port map (
            data_input => input_key,
            en => en_key,
            data_output => output_key
            );
----------------------------------------------------------------------------------------------------
-- Instantiate AES_Text

    uut_text : AES_Text

    generic map (S => 4, N => 8)

    port map (
            data_input => input_text,
            en => en_text,
            data_output => output_text
            );

----------------------------------------------------------------------------------------------------

    process(clk, reset)
    begin
        if reset = '1' then

            state <= S0;
            round_counter <= 0;
            round_data <= (others => '0');
            round_key <= (others => '0');
            we_done <= '0';

            
            input_text <= (others => '0');
            text_ready <= '0';
            text_counter <= 0;

            input_key <= (others => '0');
            key_ready <= '0';
            key_counter <= 0;

            input_SB <= (others => '0');
            sb_ready <= '0';

            input_ARK1 <= (others => '0');
            input_ARK2 <= (others => '0');
            ark_ready <= '0';

            input_SR <= (others => '0');
            sr_ready <= '0';
            -- shift_bytes_SR <= 0;

            done <= '0';
             
        
        elsif rising_edge(clk) then

            case state is

                when S0 =>

                    if (start = '1' and we_done = '0') then 
                        state <= PrepareData;
                    end if;
                
                when PrepareData =>

                    if(text_counter < 16) then
                        if(text_ready = '0') then
                            input_text <= std_logic_vector(to_unsigned(text_counter, 4));
                            en_text <= '1';
                            text_ready <= '1';
                        else
                            en_text <= '0';
                            text_ready <= '0';
                            round_data(127 - 8 * text_counter downto 120 - 8 * text_counter) <= output_text;
                            text_counter <= text_counter + 1;
                        end if;
                    else
                        text_counter <= 0;
                        state <= PrepareKey;
                    end if;

                when PrepareKey =>
                    if(key_counter < 16) then
                        if(key_ready = '0') then
                            input_key <= std_logic_vector(to_unsigned(16*(round_counter) + key_counter, 8));
                            en_key <= '1';
                            key_ready <= '1';
                        else
                            en_key <= '0';
                            key_ready <= '0';
                            round_key(127 - 8 * key_counter downto 120 - 8 * key_counter) <= output_key;
                            key_counter <= key_counter + 1;
                        end if;
                    else
                        key_counter <= 0;
                        if(round_counter = 0) then
                            state <= AddRoundKey;
                            round_counter <= round_counter + 1;
                        elsif (round_counter = 9) then
                            state <= FinalAddRoundKey;
                        else
                            state <= RoundLogic;
                            round_counter <= round_counter + 1;
                        end if;    

                    end if;
                
                when RoundLogic =>
                    if(start_process_round = "00") then
                        rst_round <= '1';
                        start_process_round <= "01";
                    elsif(start_process_round = "01") then
                        start_process_round <= "10";
                    elsif(start_process_round = "10") then
                        rst_round <= '0';
                        start_round <= '1';
                        start_process_round <= "11";
                    elsif(start_process_round = "11") then
                        if(done_round = '1') then
                            start_round <= '0';
                            start_process_round <= "00";
                            round_data <= result_round;
                            state <= PrepareKey;
                        end if;
                    end if;

                when AddRoundKey =>
                    if ark_counter < 16 then
                        if(ark_ready = '0') then
                            input_ARK1 <= round_data(127-(ark_counter*8) downto 120-(ark_counter*8));
                            input_ARK2 <= round_key(127-(ark_counter*8) downto 120-(ark_counter*8));
                            en_ARK <= '1';
                            ark_ready <= '1';
                        else
                            en_ARK <= '0';
                            ark_ready <= '0';
                            round_data(127-(ark_counter*8) downto 120-(ark_counter*8)) <= output_ARK;
                            ark_counter <= ark_counter + 1;
                        end if;
                    else
                        result <= round_data;
                        ark_counter <= 0;
                        state <= InvShiftRows;
                    end if;
                
                when InvShiftRows =>
                    if(ark_counter < 4) then
                        if(sr_ready = '0') then
                            input_SR <= round_data(127-32*(ark_counter) downto 96-32*(ark_counter));
                            shift_bytes_SR <= ark_counter;
                            en_SR <= '1';
                            sr_ready <= '1';
                        else
                            en_SR <= '0';
                            sr_ready <= '0';
                            ark_counter <= ark_counter + 1;
                            round_data(127-32*(ark_counter) downto 96-32*(ark_counter)) <= output_SR;
                        end if;
                    else
                        result <= round_data;
                        ark_counter <= 0;
                        state <= InvSubBytes;
                        
                    end if;
                        
                when InvSubBytes =>

                     if(ark_counter < 16) then
                        if(sb_ready = '0') then
                            input_SB <= round_data(127-(ark_counter*8) downto 120-(ark_counter*8));
                            en_SB <= '1';
                            sb_ready <= '1';
                        else
                            en_SB <= '0';
                            sb_ready <= '0';
                            round_data(127-(ark_counter*8) downto 120-(ark_counter*8)) <= output_SB;
                            ark_counter <= ark_counter + 1;
                        end if;
                     else
                        result <= round_data;
                        ark_counter <= 0;
                        state <= PrepareKey;
                     end if;
                
                when FinalAddRoundKey =>
                    if ark_counter < 16 then
                        if(ark_ready = '0') then
                            input_ARK1 <= round_data(127-(ark_counter*8) downto 120-(ark_counter*8));
                            input_ARK2 <= round_key(127-(ark_counter*8) downto 120-(ark_counter*8));
                            en_ARK <= '1';
                            ark_ready <= '1';
                        else
                            en_ARK <= '0';
                            ark_ready <= '0';
                            round_data(127-(ark_counter*8) downto 120-(ark_counter*8)) <= output_ARK;
                            ark_counter <= ark_counter + 1;
                        end if;
                    else
                        result <= round_data;
                        ark_counter <= 0;
                        state <= SF;
                    end if;
                
                when SF =>
                    we_done <= '1';
                    done <= '1';
                    state <= S0;

                when others =>
                    state <= S0;

            end case;
        end if;

    end process;

end Behavioral;