from oops import *
from utils import *
import time

# ============================ Helper Functions for I/O Parsing ================================= #

def Parse_Input(fpath):
    '''
    Returns a object of Gate_Data type
    '''
    gate_data = Gate_Data()
    with open(fpath,'r') as file:
        for line in file.readlines():
            line_data = (line.strip()).split()
            if(len(line_data)==0):              # If any unexpected blank line is encountered
                continue
            if(line_data[0].startswith('g')):
                gate_index,gate_width,gate_height = int(line_data[0][1:]),int(line_data[1]),int(line_data[2])
                gate_data.add_gate(gate_index,gate_width,gate_height)
            elif(line_data[0] == "pins"):
                gate_index = int(line_data[1][1:])
                for i in range(2,len(line_data),2):
                    pin_index,pin_x,pin_y = i//2,int(line_data[i]),int(line_data[i+1])
                    gate_data.add_pin(gate_index,pin_index,pin_x,pin_y)
            elif(line_data[0] == "wire"):
                gp_i,gp_j = line_data[1].split('.'),line_data[2].split('.') 
                g_i,p_i = int(gp_i[0][1:]),int(gp_i[1][1:])
                g_j,p_j = int(gp_j[0][1:]),int(gp_j[1][1:])
                # print(g_i,p_i,g_j,p_j)
                gate_data.add_wire(g_i,p_i,g_j,p_j)
    gate_data.set_gate_env()            
    return gate_data

def Parse_Output(gate_data ,fpath):
    bounding_box_x,bounding_box_y = gate_data.get_bbox()
    gate_data.correction_wire_length() 
    with open(fpath,'w') as file:
        file.write(f"bounding_box {bounding_box_x} {bounding_box_y} \n")
        for i in range(1,len(gate_data.gates)+1):
            gate_index,gate_x,gate_y = gate_data.gates[i].get_gate_tup()
            file.write(f"g{gate_index} {gate_x} {gate_y} \n")
        file.write(f"wire_length {gate_data.wire_length}")

# ====================================== Main Function ========================================== #

if(__name__ == "__main__"):
    t1 = time.time()
    gd = Parse_Input(FP_SINGLE_IN)
    sma = Simulated_Annealing(gd,10**(8),0.99,0.1)
    sma.gen_init_packing()
    sma.anneal_to_pack(3)
    Parse_Output(sma.gate_data,FP_SINGLE_OUT)
    # sma.perturb_packing_swap_v2()
    # print(f"Current_cost {sma.update_wire_cost(sma.wire_cost_function())}")
    # # for i in range(1,len(sma.gate_data.gates)+1):
    # #     print(sma.gate_data.gates[i])
    t2 = time.time()
    print(f"Done {t2-t1:.4f}s")
    print(f"Older Wire Length: {sma.initial_wire_cost}")
    print(f"Wire Length: {sma.gate_data.wire_length}")