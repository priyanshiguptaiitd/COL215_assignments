from oops import *
from utils import *
import sys

# ============================ Helper Functions for I/O Parsing ================================= #
sys.setrecursionlimit(5*10**6)

''' READ ME Regarding Coordinate System Used -
    
    We have assumed the global coordinate system to have (0,0) at the top left corner of the bounding box
    Relevant Calculations are done accordingly to calculate the relative as well as global coordinates of the gate envelopes,
    gates and pin coordinates.    

'''

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
            elif(line_data[0].lower() == "pins"):
                gate_index = int(line_data[1][1:])
                for i in range(2,len(line_data),2):
                    pin_index,pin_x,pin_y = i//2,int(line_data[i]),int(line_data[i+1])
                    gate_data.add_pin(gate_index,pin_index,pin_x,pin_y)
            elif(line_data[0].lower() == "wire"):
                gp_i,gp_j = line_data[1].split('.'),line_data[2].split('.') 
                g_i,p_i = int(gp_i[0][1:]),int(gp_i[1][1:])
                g_j,p_j = int(gp_j[0][1:]),int(gp_j[1][1:])
                # print(g_i,p_i,g_j,p_j)
                gate_data.add_wire(g_i,p_i,g_j,p_j)
    gate_data.set_gate_env()            
    gate_data.find_connected_components()
    gate_data.find_pin_comps()
    return gate_data

def Parse_Output(gate_data ,fpath, is_pseudo_copy = False):
    if(not is_pseudo_copy):
        bounding_box_x,bounding_box_y = gate_data.get_bbox()
        with open(fpath,'w') as file:
            file.write(f"bounding_box {bounding_box_x} {bounding_box_y} \n")
            for i in range(1,len(gate_data.gates)+1):
                gate_index,gate_x,gate_y = gate_data.gates[i].get_gate_tup_og()
                file.write(f"g{gate_index} {gate_x} {gate_y} \n")
            file.write(f"wire_length {gate_data.wire_length}")
    else:
        bbox_width,bbox_height,wire_length,gate_packing_data = gate_data
        with open(fpath,'w') as file:
            file.write(f"bounding_box {bbox_width} {bbox_height} \n")
            for i in range(len(gate_packing_data)):
                file.write(f"g{gate_packing_data[i][0]} {gate_packing_data[i][1]} {gate_packing_data[i][2]} \n")
            file.write(f"wire_length {wire_length}")

# ============================ Functions for Automated Test Case ================================= #

@time_it_no_out
def test_testcases(gate_freq,tc_freq):
    '''
    Function to test single call to anneal_to_pack for various test cases
    '''
    with open(FP_MULTI_OUT+f"\\Special_Report_{gate_freq}.txt",'w') as file:
        for i in range(1,tc_freq+1):
            gd = Parse_Input(FP_MULTI_CASES_IN(gate_freq,i))
            sma = Simulated_Annealing(gd,10**(8),0.1)
            psd_gd,anneal_pack_time = sma.anneal_to_pack(1,True,supress_time_out = True)
            file.write(f"Test Case {i} :\n") 
            file.write(f"No. of Gates : {len(gd.gates)}\n")
            file.write(f"No. of Pins : {gd.total_pins_added}\n")
            file.write(f"No. of Wires : {gd.total_wires_added}\n")
            file.write(f"Runtime : {anneal_pack_time:.6f} seconds\n")
            print(f"Done with test case {i}")    
    print("Done with all test cases")    

@time_it_no_out
def test_testcase_single(perturb_freq):
    '''
    Function to test single call to anneal_routine for single test case
    '''
    fpath = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Code"
    fpath = fpath + "\\output2.txt"
    
    with open(fpath,"w") as file:
        gd = Parse_Input(FP_SINGLE_IN)
        sma = Simulated_Annealing(gd,10**(5),0.1)
        anneal_data,vd = sma.anneal_to_pack(perturb_freq,True,True,True,supress_time_out = False)
        # for t in anneal_data:
        #     file.write(f"Iteration & Cost : {t[0]} {t[1]}\n")
    print("Done with test case")

@ time_it_no_out
def test_testcase_multi():
    with open(CUST_FP_PATH+f"\\Special_Report_Vary_Pins_Not_Wires.txt",'w') as file:
        for i in range(1,18):
            gd = Parse_Input(FP_MULTI_CASES_IN(1000,i))
            sma = Simulated_Annealing(gd,10**(5),0.1)
            psd_gd,anneal_routine_time = sma.anneal_to_pack(1,True,False,True,supress_time_out = True)
            print(f"Done with test case {i}")
            file.write(f"Done with test case {i}\n")
            file.write(f"No of Gates : {len(gd.gates)}\n")
            file.write(f"No of Pins : {gd.total_pins_added}\n")
            file.write(f"No of Wires : {gd.total_wires_added}\n")
            file.write(f"Total wire cost after annealing: {sma.wire_cost}\n")
            file.write(f"Total anneal routine Time: {anneal_routine_time:.6f} seconds\n")
            Parse_Output(sma.gate_data,FP_MULTI_CASES_OUT(1000,i),is_pseudo_copy = False)
            
@ time_it_no_out
def test_testcase_multi_2():
    with open(CUST_FP_PATH+f"\\Special_Report_Vary_Wires_Fix_Pins.txt", "w") as file:
        for i in range(1,21):
            gd = Parse_Input(FP_MULTI_CASES_IN(500,i))
            sma = Simulated_Annealing(gd,10**(5),0.1)
            psd_gd,anneal_routine_time = sma.anneal_to_pack(1,True,False,True,supress_time_out = True)
            print(f"Done with test case {i}")
            file.write(f"Done with test case {i}\n")
            file.write(f"No of Gates : {len(gd.gates)}\n")
            file.write(f"No of Pins : {gd.total_pins_added}\n")
            file.write(f"No of Wires : {gd.total_wires_added}\n")
            file.write(f"Total wire cost after annealing: {sma.wire_cost}\n")
            file.write(f"Total anneal routine Time: {anneal_routine_time:.6f} seconds\n")
            Parse_Output(sma.gate_data,FP_MULTI_CASES_OUT(500,i),is_pseudo_copy = False)
        
# ====================================== Main Function ========================================== #

if(__name__ == "__main__"):
    gd = Parse_Input(FP_SINGLE_IN)
    sma = Simulated_Annealing(gd,10**(5),0.1)
    psd_gd,anneal_routine_time = sma.anneal_routine(False,supress_time_out = True)
    print(f"Total wire cost after annealing (Piazza Heuristic): {sma.wire_cost}\n")
    print(f"Total anneal routine Time: {anneal_routine_time:.6f} seconds\n")
    Parse_Output(sma.gate_data,FP_SINGLE_OUT,is_pseudo_copy = False)