from oops import *
from utils import *
import sys

# ============================ Helper Functions for I/O Parsing ================================= #
sys.setrecursionlimit(10**6)

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
                gate_index,gate_width,gate_height,gate_delay = int(line_data[0][1:]),int(line_data[1]),int(line_data[2]), int(line_data[3])
                gate_data.add_gate(gate_index,gate_width,gate_height,gate_delay)
            elif(line_data[0].lower() == "pins"):
                gate_index = int(line_data[1][1:])
                gw = gate_data.gates[gate_index].width
                for i in range(2,len(line_data),2):
                    pin_index,pin_x,pin_y = i//2,int(line_data[i]),int(line_data[i+1])
                    gate_data.add_pin(gate_index,pin_index,pin_x,pin_y)
                
            elif(line_data[0].lower() == "wire_delay"):
                gate_data.set_wire_delay(int(line_data[1]))
            elif(line_data[0].lower() == "wire"):
                gp_i,gp_j = line_data[1].split('.'),line_data[ 2].split('.') 
                g_i,p_i = int(gp_i[0][1:]),int(gp_i[1][1:])
                g_j,p_j = int(gp_j[0][1:]),int(gp_j[1][1:])
                # print(g_i,p_i,g_j,p_j)
                gate_data.add_wire(g_i,p_i,g_j,p_j)
                
    gate_data.init_better_packing(supress_time_out = True)
    gate_data.init_wire_groups(supress_time_out = True)
    # gate_data.init_critical_paths(supress_time_out = False)
    
    return gate_data

def Parse_Output(gate_data,fpath):
    bbox = gate_data.get_bbox()
    cpath = f"critical_path {gate_data.critical_path}" 
    cpath_delay = f"critical_path_delay {gate_data.max_delay}"
    with open(fpath,'w') as file:
        file.write(f"bounding_box {bbox[0], bbox[1]}\n")
        file.write(f"{cpath}\n")
        file.write(f"{cpath_delay}\n")
        for gate in gate_data.gates:
            gate_index, gate_width, gate_height = gate_data.gates[gate].get_gate_tup("parse")
            file.write(f"g{gate_index} {gate_width} {gate_height}\n")
        
# ============================ Functions for Automated Test Case ================================= #

# ============================= __main__ for Testing Purposes ==================================== #

if(__name__ == "__main__"):
    
    gd = Parse_Input(FP_IN)
    gd.better_pack_order = [None] + list(np.random.permutation([i for i in range(1,len(gd.gates)+1)]))
    gd.write_netlist_data(FP_REPORT,supress_time_out = False)
    
    print(len(gd.only_primary_input_gates))
    
    gd.find_max_delay_routine()
    md , run_t = gd.find_max_delay(supress_time_out = False)
    max_delay, max_gate = md[0],md[1]    
    gd.max_delay = max_delay
    gd.set_critical_path(max_gate)
    print(f"Critical Path Delay: {gd.max_delay}")
    # print(f"Critical Path: {gd.critical_path}")
    
    prev_delay = gd.max_delay
    Parse_Output(gd,FP_OUT)
    print(f"Initial Critical Path Delay: {gd.max_delay}")
    
    for lc in range(100):
        rng = np.random.default_rng()
        gd = Parse_Input(FP_IN)
        #  gd.write_netlist_data(FP_REPORT,supress_time_out = False)
        #  print(len(gd.only_primary_input_gates)) 
        gd.find_max_delay_routine()
        md , run_t = gd.find_max_delay(supress_time_out = True)
        max_delay, max_gate = md[0],md[1]    
        gd.max_delay = max_delay
        gd.set_critical_path(max_gate)
        # print(f"Critical Path Delay: {gd.max_delay}")
        # print(f"Critical Path: {gd.critical_path}")
        
        if(gd.max_delay < prev_delay):
            print(f"New Critical Path Delay: {gd.max_delay}")
            prev_delay = gd.max_delay
            Parse_Output(gd,FP_OUT)
            continue
    
    print(f"Final Critical Path Delay: {prev_delay}")