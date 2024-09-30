from time import time
from itertools import count
from math import floor
from secrets import randbits
import numpy as np

''' READ ME - utils.py

This is the utility module, it clubs the funcitonality of multiple of our older implementations of Python Projects
Note that the additional imports mode are only used for test case generation and verification purposes

No additional module was imported to implement any part of the assignment's process

'''

# ===================================== Project Constants =================================== #
'''
Storing Constants for projects that are going to be used throughout the project
This includes File Paths, Allowed Gate Frequencies, Mean and Variance for Gate Dimensions and Pin Positions
Also stores preferable standard arguments test case generation
'''

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

TIME_BOUND_TOTAL_SEC = 18
TIME_BOUND_BUFFER_SEC = 2
IDEAL_PERT_ITER_HI = 8
IDEAL_PERT_ITER_MED = 6
IDEAL_PERT_ITER_LO = 4
CALL_BOUND_TOTAL = 20
BREAK_FLAG_COUNT = 30

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
            print(f'Function {func.__name__!r} executed in {(t_end-t_start):.4f}s and produced output : {result} \n') 
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
            print(f'Function {func.__name__!r} executed in {(t_end-t_start):.4f}s \n') 
        return result,(t_end-t_start)
    return wrap_func_timeit_no_out

# -------------------------------- Filepath for TestCases IO ------------------------------------ #
'''
Function to generate File Paths for Single and Multiple Test Cases
Relevant to the local Host's File System, Change the File Paths Accordingly
'''

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
    """
    Generates dimensions for gates based on the specified mode.

    Args:
        mode (str): The mode of dimension generation. Can be "uniform", "normal_lo", or "normal_hi".
        dim_lo (int): The lower bound for the dimensions.
        dim_hi (int): The upper bound for the dimensions.

    Returns:
        tuple: A tuple containing the width and height of the gate.
    """
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

def generate_pin_positions(gh,gate_freq,pin_density = 0.75,max_pin_freq = 6,override_specs = False, ensure_max_pins = False):
    """
    Generates pin positions for gates.

    Args:
        gh (int): The height of the gate.
        gate_freq (int): The frequency of the gate, for pin density calculations
        pin_density (float): The density of the pins , based on how many pins we want per gate and MAX_PINS
        max_pin_freq (int): The maximum frequency of the pins, used to override if override_specs is True.
        override_specs (bool): Whether to override the specifications for manual checking of TC

    Returns:
        tuple: Two arrays containing the positions of the left side and right side pins.
    """
    max_pin_freq_2 = (pin_density*MAX_PINS)//gate_freq
    rng_l = np.random.default_rng(randbits(128))
    rng_r = np.random.default_rng(randbits(128))
    arr = np.arange(1,gh+1)
    pin_freq_left =  rng_l.integers(1,gh+1)
    pin_freq_right = rng_r.integers(1,gh+1)
    
    if(override_specs):
        pin_freq_left =  min(max_pin_freq//2,pin_freq_left)
        pin_freq_right = min(max_pin_freq//2,pin_freq_right)
    else:
        pin_freq_left =  min(max_pin_freq_2//2,pin_freq_left)
        pin_freq_right = min(max_pin_freq_2//2,pin_freq_right)    
    
    if(ensure_max_pins):
        pin_freq_left =  ensure_max_pins = gh
        
    arr_left = rng_l.choice(arr,int(pin_freq_left),replace=False,shuffle=False)
    arr_right = rng_r.choice(arr,int(pin_freq_right),replace=False,shuffle=False)
    return arr_left, arr_right

def generate_wires(gate_freq,gate_pins,left_edge_data,br_prob = 10**(-2)):
    """
    Generates wires between gates based on the problem Statement specifications.
    
    Left Edge Data is used to ensure that the left edge of the gate is not used for multiple wires.

    Args:
        gate_freq (int): The frequency of the gate.
        gate_pins (dict): A dictionary containing the pins of the gates.
        left_edge_data (dict): A dictionary containing the left edge data.
        br_prob (float): The probability of breaking out of the wire generation loop.
                         Only activates once all gates have at least one wire.
                         Ensured by atleast_one dict.
    Returns:
        wire_data.keys: The keys of the wire data dictionary.
    """
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
            
            meets_wire_gen_criteria = False
            
            if(gate_pins[g1][p1][0] != 0 and gate_pins[g2][p2][0] != 0):
                meets_wire_gen_criteria = True 
                                   
            elif(gate_pins[g1][p1][0] == 0 and gate_pins[g2][p2][0] != 0):
                if(not left_edge_data[(g1,0,gate_pins[g1][p1][1])]):
                    meets_wire_gen_criteria = True
                    left_edge_data[(g1,0,gate_pins[g1][p1][1])] = True
                                       
            elif(gate_pins[g1][p1][0] != 0 and gate_pins[g2][p2][0] == 0):
                if(not left_edge_data[(g2,0,gate_pins[g2][p2][1])]):
                    meets_wire_gen_criteria = True
                    left_edge_data[(g2,0,gate_pins[g2][p2][1])] = True
            
            else:
                if(not (left_edge_data[(g1,0,gate_pins[g1][p1][1])] or left_edge_data[(g2,0,gate_pins[g2][p2][1])])):
                    meets_wire_gen_criteria = True
                    left_edge_data[(g1,0,gate_pins[g1][p1][1])] = True
                    left_edge_data[(g2,0,gate_pins[g2][p2][1])] = True

            if(meets_wire_gen_criteria):
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

@ time_it_no_out 
def write_single_case(gate_freq,fpath,kw):
    """
    Writes a single test case to a file using generate_dimensions, generate_pin_positions,
    and generate_wires methods on input parameters.

    Args:
        gate_freq (int): The frequency of the gate.
        fpath (str): The file path to write the test case.
        kw (dict): A dictionary containing the parameters for test case generation.

    Returns:
        None
    """
    assert kw["mode"] in ["uniform","normal_lo","normal_hi"], "Please give a valid testcase generator type"
    
    with open(fpath,"w") as file:
        gate_pins = {i:[] for i in range(1,gate_freq+1)}
        left_edge = {} 
        pins_gen = 0
        for i in range(1,gate_freq+1):
            gw,gh = generate_dimensions(kw["mode"],kw["dim_lo"],kw["dim_hi"])
            file.write(f"g{i} {gw} {gh} \n")
            file.write(f"pins g{i} ")
            pin_left,pin_right = generate_pin_positions(gh,gate_freq,kw["pin_density"],kw["max_pin_freq"],kw["override_specs"],kw["ensure_max_pins"])
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
      
# ======================== Helper Functions for Simulated Annealing ============================= #        

IT_BOUND = 10**6

def random_seed_128():
    return randbits(128)

def cooling_rate(T):
    return 0.99

def H_global_coord_pin(gate_ref,pin_index,old_coord, height):
    pin_ref = gate_ref.pins[pin_index]
    pin_rel_x,pin_rel_y = pin_ref.pin_x,pin_ref.pin_y
    return old_coord[0] + pin_rel_x, old_coord[1] + height - pin_rel_y

@ time_it
def pseudo_copy_gate_data(gate_data):
    bbox_width,bbox_height = gate_data.get_bbox()
    wire_length = gate_data.wire_length
    gate_packing_data = [gate_data.gates[i].get_gate_tup() for i in range(1,len(gate_data.gates)+1)]
    
    return bbox_width,bbox_height,wire_length,gate_packing_data


if(__name__ == "__main__"):
    kw = {
          "gate_freq":1000,
          "mode": "uniform",
          "br_prob": 10**(-6),
          "dim_lo":1,
          "dim_hi":101,
          "pin_density":1.5,
          "max_pin_freq":4,
          "override_specs":False,
          "ensure_max_pins":False ### May cause 40_000 pins overflow for larger gate frequencies
          }
    write_single_case(kw["gate_freq"],FP_SINGLE_IN,kw,supress_time_out=False)
    print("Done")