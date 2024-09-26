from oops import *
from time import time
from itertools import count
from math import *
from secrets import randbits
import numpy as np

'''

READ ME - utils.py

This is the utility module, it clubs the funcitonality of multiple of our older implementations of Python Projects
Note that the additional imports mode are only used for test case generation and verification purposes

No additional module was imported to implement any part of the Assignment's process

'''

# ===================================== Project Constants =================================== #

FP_SINGLE_IN = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Code\input.txt"
FP_SINGLE_OUT = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Code\output.txt"
FP_MULTI_IN = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Test_Cases\Auto\Multi_Cases\Input_Test_Cases_Multi"
FP_MULTI_OUT = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Test_Cases\Auto\Multi_Cases\Output_Test_Cases_Multi"
ALLOWED_GATE_FREQ = [10,25,50,100,250,500,1000]
MEAN_GATE_DIM = 50
VAR_GATE_DIM_LO = 10
VAR_GATE_DIM_HI  = 25 
MEAN_PIN_POS = 0.5
VAR_PIN_POS_LO = 0.1
VAR_PIN_POS_HI = 0.25
MAX_PINS = 40_000
KW_MANUAL = {
            "gate_freq":6,
            "mode": "uniform",
            "br_prob":0.50,
            "dim_lo":1,
            "dim_hi":11,
            "pin_density":0.90,
            "max_pin_freq":4,
            "override_specs":True
            }

# PACK_EFF_BOUND = 0.95
# DIM_INC_FAILTC = 1.5
# DIM_DELTA_PEFF = 0.05
# ALPHA_MARGIN_DIM = 1.1
# TC_RUNTIME_BOUND = 2
# MAX_IT_BOUND = 20

# ======================= Helper Functions for Implementation Testing =========================== #

# -------------------------------- Function Timing Utility -------------------------------------- #
def time_it(func): 
    """ time_it - Wrapper for timing function exectution

    Args:
        func (_type_): The function we want to pass to our timing wrapper
    """
    def wrap_func_timeit(*args, **kwargs): 
        t_start = time() 
        result = func(*args) 
        t_end = time()
        if(not kwargs["supress_time_out"]): 
            print(f'Function {func.__name__!r} executed in {(t_end-t_start):.4f}s and produced output : {result}') 
        return result,(t_end-t_start) 
    return wrap_func_timeit

def time_it_no_out(func): 
    """ time_it_no_out - Wrapper for timing function exectution (No Output Shown)

    Args:
        func (_type_): The function we want to pass to our timing wrapper
    """
    def wrap_func_timeit_no_out(*args, **kwargs): 
        t_start = time() 
        result = func(*args) 
        t_end = time() 
        if(not kwargs["supress_time_out"]): 
            print(f'Function {func.__name__!r} executed in {(t_end-t_start):.4f}s ') 
        return result,(t_end-t_start)
    return wrap_func_timeit_no_out

# -------------------------------- Filepath for TestCases IO ------------------------------------ #
def FP_MULTI_CASES_IN(gate_freq,i=None):
    assert gate_freq in ALLOWED_GATE_FREQ, "Invalid Gate Frequency for Multiple Test Cases"
    return FP_MULTI_IN + f"\\{gate_freq} Gates\\tc{i}_{gate_freq}.txt"
    
def FP_MULTI_CASES_OUT(gate_freq,i=None):
    assert gate_freq in ALLOWED_GATE_FREQ, "Invalid Gate Frequency for Multiple Test Cases"
    if (i is not None):
        return FP_MULTI_OUT + f"\\{gate_freq} Gates\\tc{i}_{gate_freq}.txt"
    else:
        return FP_MULTI_OUT + f"\\Report_{gate_freq}_Multi.txt" 

# --------------------------------- Test Case Generation ---------------------------------------- #

def generate_dimensions(mode="normal_hi",dim_lo=1,dim_hi =101):
    if(mode == "uniform"):
        return floor(np.random.uniform(dim_lo,dim_hi)),floor(np.random.uniform(dim_lo,dim_hi))
    elif(mode == "normal_lo"):
        for _infit in count(0,1):
            gw,gh = floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_LO)),floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_LO))
            if(dim_lo <= gw <= dim_hi and dim_lo <= gh <= dim_hi):
                return gw,gh
    elif(mode == "normal_hi"):
        for _infit in count(0,1):
            gw,gh = floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_HI)),floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_HI))
            if(dim_lo <= gw <= dim_hi and dim_lo <= gh <= dim_hi):
                return gw,gh

def generate_pin_positions(gh,gate_freq,pin_density = 0.75,max_pin_freq = 6,override_specs = False):
    max_pin_freq_2 = (pin_density*MAX_PINS)//gate_freq
    rng_l = np.random.default_rng(randbits(128))
    rng_r = np.random.default_rng(randbits(128))
    arr = np.arange(1,gh+1)
    pin_freq_left =  max(rng_l.integers(0,gh+1),1)
    pin_freq_right = max(1,rng_r.integers(0,gh+1))
    
    if(override_specs):
        pin_freq_left =  min(max_pin_freq//2,pin_freq_left)
        pin_freq_right = min(max_pin_freq//2,pin_freq_right)
    else:
        pin_freq_left =  min(max_pin_freq_2//2,pin_freq_left)
        pin_freq_right = min(max_pin_freq_2//2,pin_freq_right)    
    
    arr_left = rng_l.choice(arr,int(pin_freq_left),replace=False,shuffle=False)
    arr_right = rng_r.choice(arr,int(pin_freq_right),replace=False,shuffle=False)
    return arr_left, arr_right

def generate_wires(gate_freq,gate_pins,left_edge_data,br_prob = 10**(-2)):
    atleast_one,wire_data,count_atleast_one = {i:False for i in range(1,gate_freq+1)},{},0
    rng = np.random.default_rng(randbits(128))
    rng_break = np.random.default_rng(randbits(128))
    while True:
        g1 = rng.integers(1,gate_freq+1)
        g2 = rng.integers(1,gate_freq+1)
        if(g1 == g2):
            continue
        else:
            p1 = rng.integers(0,len(gate_pins[g1]))
            p2 = rng.integers(0,len(gate_pins[g2]))
            if(gate_pins[g1][p1][0] != 0 and gate_pins[g2][p2][0] != 0):
                wire_data[f"wire g{g1}.p{p1+1} g{g2}.p{p2+1}"] = True
                if(not atleast_one[g1]):
                    atleast_one[g1] = True
                    count_atleast_one += 1
                if(not atleast_one[g2]):
                    atleast_one[g2] = True
                    count_atleast_one += 1
                if(count_atleast_one == gate_freq):
                    if(rng_break.random() < br_prob):
                        break                    
            elif(gate_pins[g1][p1][0] == 0 and gate_pins[g2][p2][0] != 0):
                if(not left_edge_data[(g1,0,gate_pins[g1][p1][1])]):
                    left_edge_data[(g1,0,gate_pins[g1][p1][1])] = True
                    wire_data[f"wire g{g1}.p{p1+1} g{g2}.p{p2+1}"] = True
                    if(not atleast_one[g1]):
                        atleast_one[g1] = True
                        count_atleast_one += 1
                    if(not atleast_one[g2]):
                        atleast_one[g2] = True
                        count_atleast_one += 1
                    if(count_atleast_one == gate_freq):
                        if(rng_break.random() < br_prob):
                            break                   
            elif(gate_pins[g1][p1][0] != 0 and gate_pins[g2][p2][0] == 0):
                if(not left_edge_data[(g2,0,gate_pins[g2][p2][1])]):
                    left_edge_data[(g2,0,gate_pins[g2][p2][1])] = True
                    wire_data[f"wire g{g1}.p{p1+1} g{g2}.p{p2+1}"] = True
                    if(not atleast_one[g1]):
                        atleast_one[g1] = True
                        count_atleast_one += 1
                    if(not atleast_one[g2]):
                        atleast_one[g2] = True
                        count_atleast_one += 1
                    if(count_atleast_one == gate_freq):
                        if(rng_break.random() < br_prob):
                            break
            else:
                if(not (left_edge_data[(g1,0,gate_pins[g1][p1][1])] or left_edge_data[(g2,0,gate_pins[g2][p2][1])])):
                    left_edge_data[(g1,0,gate_pins[g1][p1][1])] = True
                    left_edge_data[(g2,0,gate_pins[g2][p2][1])] = True
                    wire_data[f"wire g{g1}.p{p1+1} g{g2}.p{p2+1}"] = True
                    if(not atleast_one[g1]):
                        atleast_one[g1] = True
                        count_atleast_one += 1
                    if(not atleast_one[g2]):
                        atleast_one[g2] = True
                        count_atleast_one += 1
                    if(count_atleast_one == gate_freq):
                        if(rng_break.random() < br_prob):
                            break
    print(f"Total Wires Generated : {len(wire_data)}")
    return wire_data.keys()

def write_single_case(gate_freq,fpath,kw):
    # assert gatefreq%25 == 0 or gatefreq == 10, "Please give a valid test case size"
    assert kw["mode"] in ["uniform","normal_lo","normal_hi"], "Please give a valid testcase generator type"
    
    with open(fpath,"w") as file:
        gate_pins = {i:[] for i in range(1,gate_freq+1)}
        left_edge = {} 
        pins_gen = 0
        for i in range(1,gate_freq+1):
            gw,gh = generate_dimensions(kw["mode"],kw["dim_lo"],kw["dim_hi"])
            file.write(f"g{i} {gw} {gh} \n")
            file.write(f"pins g{i} ")
            pin_left,pin_right = generate_pin_positions(gh,gate_freq,kw["pin_density"],kw["max_pin_freq"],kw["override_specs"])
            pins_gen += len(pin_left) + len(pin_right)
            for j in range(len(pin_left)):
                file.write(f"{0} {pin_left[j]} ")
                gate_pins[i].append((0,pin_left[j]))
                left_edge[(i,0,pin_left[j])] = False
            for j in range(len(pin_right)):
                file.write(f"{gw} {pin_right[j]} ")
                gate_pins[i].append((gw,pin_right[j]))
            file.write("\n")
        # print(gate_pins)
        wire_data = generate_wires(gate_freq,gate_pins,left_edge,kw["br_prob"])
        
        for wire in wire_data:
            file.write(wire + "\n")
            
        print(f"Total Pins Generated : {pins_gen}")

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
                gate_data.add_wire(g_i,p_i,g_j,p_j)
                
    return gate_data

def Parse_Output(gate_data ,fpath):
    bounding_box_x,bounding_box_y = gate_data.get_bbox() 
    with open(fpath,'w') as file:
        file.write(f"bounding_box {bounding_box_x} {bounding_box_y} \n")
        for i in range(1,len(gate_data.gates)+1):
            gate_index,gate_x,gate_y = gate_data.gates[i].get_gate_tup()
            file.write(f"g{gate_index} {gate_x} {gate_y} \n")
        file.write(f"wire_length {gate_data.wire_length}")
      
# ======================== Helper Functions for Simulated Annealing ============================= #        

if(__name__ == "__main__"):
    kw = {
          "gate_freq":1000,
          "mode": "normal_hi",
          "br_prob":5*10**(-4),
          "dim_lo":1,
          "dim_hi":101,
          "pin_density":1.0,
          "max_pin_freq":4,
          "override_specs":False
          }
    write_single_case(kw["gate_freq"],FP_SINGLE_IN,kw)
    print("Done")