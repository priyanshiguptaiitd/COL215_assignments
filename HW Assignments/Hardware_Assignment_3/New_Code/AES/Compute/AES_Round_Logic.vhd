library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

----------------------------------------------------------------------------------------------------

entity AES_Round is
    Port ( clk : in std_logic;
           rst : in std_logic;  
           start : in std_logic;
           data : in std_logic_vector(127 downto 0);
           round_key : in std_logic_vector(127 downto 0); 
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
    signal ark_ready : std_logic := '0';   
    signal en_ARK : std_logic;

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
    signal sr_ready : std_logic := '0';
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
    signal output_data_MC : std_logic_vector(7 downto 0);
    signal i_mc : integer range 0 to 3 := 0;
    signal j_mc : integer range 0 to 3:= 0;
    signal mc_ready : std_logic := '0';
    signal en_MC : std_logic;
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
-- FSM Declaration
    type state_type is (S0, AddRoundKey, InvMixCols ,InvShiftRows , InvSubBytes, SF);
    signal state : state_type;
    signal init_counter : integer range 0 to 15 := 0;
    signal temp : std_logic_vector(127 downto 0);
    signal temp1 : std_logic_vector(127 downto 0);
    signal we_done : std_logic := '0';

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
                  data_input => input_SB,
                  data_output => output_SB
                 );

----------------------------------------------------------------------------------------------------

process(clk, rst) 
begin
    if rst = '1' then
        state <= S0;
        init_counter <= 0;
        done <= '0';
        temp <= (others => '0');
        i_mc <= 0;
        j_mc <= 0;
    elsif rising_edge(clk) then
        case state is
            when S0 =>
                if (start = '1' and we_done = '0') then
                    state <= AddRoundKey;
                end if;

            when AddRoundKey =>
                if init_counter < 16 then
                    if(ark_ready = '0') then
                        input_ARK1 <= data(127-(init_counter*8) downto 120-(init_counter*8));
                        input_ARK2 <= round_key(127-(init_counter*8) downto 120-(init_counter*8));
                        en_ARK <= '1';
                        ark_ready <= '1';
                    else
                        en_ARK <= '0';
                        ark_ready <= '0';
                        temp(127-(init_counter*8) downto 120-(init_counter*8)) <= output_ARK;
                        init_counter <= init_counter + 1;
                    end if;
                else
                    result <= temp;
                    temp1 <= temp;
                    init_counter <= 0;
                    state <= InvMixCols;
                end if;

            when InvMixCols =>
                if(init_counter < 16) then
                    if(mc_ready = '0') then
                        case i_mc is
                            when 0 =>
                                input_data_a_MC <= temp1(127 downto 96);
                            when 1 =>
                                input_data_a_MC <= temp1(95 downto 64);
                            when 2 =>
                                input_data_a_MC <= temp1(63 downto 32);
                            when 3 =>
                                input_data_a_MC <= temp1(31 downto 0);
                        end case;

                        case j_mc is
                            when 0 =>
                                input_data_b_MC <= temp1(127 downto 96);
                            when 1 =>
                                input_data_b_MC <= temp1(95 downto 64);
                            when 2 =>
                                input_data_b_MC <= temp1(63 downto 32);
                            when 3 =>
                                input_data_b_MC <= temp1(31 downto 0);
                        end case;

                        en_MC <= '1';
                        mc_ready <= '1';
                    else
                        en_MC <= '0';
                        mc_ready <= '0';
                        temp(127-(init_counter*8) downto 120-(init_counter*8)) <= output_data_MC;
                        init_counter <= init_counter + 1;
                        if(j_mc = 3) then
                            j_mc <= 0;
                            i_mc <= i_mc + 1;
                        else
                            j_mc <= j_mc + 1;
                        end if;
                    end if;
                else
                    result <= temp;
                    init_counter <= 0;
                    state <= InvShiftRows;
                end if;

            when InvShiftRows =>
                if(init_counter < 4) then
                    if(sr_ready = '0') then
                        input_SR <= temp(127-32*(init_counter) downto 96-32*(init_counter));
                        shift_bytes_SR <= init_counter;
                        en_SR <= '1';
                        sr_ready <= '1';
                    else
                        en_SR <= '0';
                        sr_ready <= '0';
                        init_counter <= init_counter + 1;
                        temp(127-32*(init_counter) downto 96-32*(init_counter)) <= output_SR;
                    end if;
                else
                    result <= temp;
                    init_counter <= 0;
                    state <= InvSubBytes;
                end if;

            when InvSubBytes =>
                if(init_counter < 16) then
                    if(sb_ready = '0') then
                        input_SB <= temp(127-(init_counter*8) downto 120-(init_counter*8));
                        en_SB <= '1';
                        sb_ready <= '1';
                    else
                        en_SB <= '0';
                        sb_ready <= '0';
                        temp(127-(init_counter*8) downto 120-(init_counter*8)) <= output_SB;
                        init_counter <= init_counter + 1;
                    end if;
                else
                    result <= temp;
                    init_counter <= 0;
                    state <= SF;
                end if;

            when SF =>
                done <= '1';
                we_done <= '1';
                state <= S0;

            when others =>
                state <= S0;
        end case;
    end if;
end process;
end arch_AES;