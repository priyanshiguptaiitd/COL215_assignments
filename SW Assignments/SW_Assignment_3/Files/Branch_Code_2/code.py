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
        file.write(f"bounding_box {bbox[0]} {bbox[1]}\n")
        file.write(f"{cpath}\n")
        file.write(f"{cpath_delay}\n")
        for gate in gate_data.gates:
            gate_index, gate_width, gate_height = gate_data.gates[gate].get_gate_tup("parse")
            file.write(f"g{gate_index} {gate_width} {gate_height}\n")

def re_write_vis():
    with open(FP+r'\\output_vis.txt','w') as file:
        with open(FP_OUT,'r') as file_out:
            for line in file_out.readlines():
                if(line.startswith("critical_path")):
                    continue
                if(line.startswith("critical_path_delay")):
                    continue
                file.write(line)
    
    print("Output Written to output_vis.txt")
      
    with open(FP+r'\\input_vis.txt','w') as file:
        with open(FP_IN,'r') as file_in:
            for line in file_in.readlines():
                
                line_data = (line.strip()).split()
                
                if(len(line_data)==0):              # If any unexpected blank line is encountered
                    continue
                
                if(line_data[0].startswith('g')):
                    gate_index,gate_width,gate_height,gate_delay = int(line_data[0][1:]),int(line_data[1]),int(line_data[2]), int(line_data[3])
                    file.write(f"g{gate_index} {gate_width} {gate_height}\n")
                elif(line_data[0].lower() == "pins"):
                    file.write(line)
                elif(line_data[0].lower() == "wire_delay"):     
                    continue
                elif(line_data[0].lower() == "wire"):
                    file.write(line)
    
    print("Input Written to input_vis.txt")

def Loop_Pin_Check(fpath):
    gd = Parse_Input(fpath)
    # print(gd.gate_dag_from_to)
    comb_loops = def_dict(dict)
    
    for g_out in gd.gate_dag_from_to:
        for g_in in gd.gate_dag_from_to[g_out]:
            if(g_in in comb_loops[g_out]):
                print (f"Loop Detected : {g_out}, {g_in} and between")
                return False
            else:
                comb_loops[g_in][g_out] = True
                comb_loops[g_in].update(comb_loops[g_out])
                
                for g in comb_loops:
                    if(g_in in comb_loops[g]):
                        comb_loops[g].update(comb_loops[g_in])
                # print(comb_loops)
    # print(comb_loops)
    print("No Loop Detected")
    
    for k in gd.wire_dag_to_from:
        if(len(gd.wire_dag_to_from[k]) > 1):
            print(f"Multiple Inputs detected at pin : g{k[0]}.p{k[1]}")
            return False
        
    print("No Multiple Input Detected")
    return True
                   
@time_it
def solve_testcase():
    
    gd = Parse_Input(FP_IN)
    gd.better_pack_order = [None] + list(np.random.permutation([i for i in range(1,len(gd.gates)+1)]))
    # print(len(gd.only_primary_input_gates))
    
    gd.find_max_delay_routine()
    md , run_t = gd.find_max_delay(supress_time_out = True)
    max_delay, max_gate = md[0],md[1]    
    gd.max_delay = max_delay
    gd.set_critical_path(max_gate)
    # print(f"Critical Path Delay: {gd.max_delay}")
    
    return gd

# ============================ Functions for Automated Test Case ================================= #

# ============================= __main__ for Testing Purposes ==================================== #    
    
if(__name__ == "__main__"):
    Loop_Pin_Check(FP_IN)
    # iters_ran = 0
    # gd_0, run_time = solve_testcase(supress_time_out = True)
    # Parse_Output(gd_0,FP_OUT)
    # gd_0.write_netlist_data(FP_REPORT, supress_time_out = True)
    # print(f"Initial Critical Path Delay: {gd_0.max_delay}")
    # prev_delay = gd_0.max_delay
    # iters_ran += 1
    # tot_run_time = run_time
    # while (TIME_BOUND_TOTAL_SEC-TIME_BOUND_BUFFER_SEC) > tot_run_time:
    #     iters_ran += 1
    #     gd, rt = solve_testcase(supress_time_out = True)
    #     tot_run_time += rt
    #     run_time = rt if (rt > run_time) else run_time
    #     if(gd.max_delay < prev_delay):
    #         gd.write_netlist_data(FP_REPORT, supress_time_out = True)
    #         print(f"New Critical Path Delay: {gd.max_delay}")
    #         prev_delay = gd.max_delay
    #         Parse_Output(gd,FP_OUT)
    # print(f"Final Critical Path Delay: {prev_delay}")
    # print(f"Total Run Time, Single Run_time, Iterations Ran: {tot_run_time : .8f}, {run_time : .8f}, {iters_ran}")
    
    # re_write_vis()