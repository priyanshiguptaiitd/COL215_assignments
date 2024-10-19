# ===================================== Import of Libraries ======================================== #

from collections import defaultdict as def_dict
from random import randint, choice, seed, random
from math import sqrt, ceil, floor
from time import time
from itertools import count
from secrets import randbits
import numpy as np
from matplotlib import pyplot as plt

# =====================================-= Project Constants ======================================== #


# ------------------------------------------ File Paths -------------------------------------------- #

FP_IN = r"SW Assignments\SW_Assignment_3\Files\Branch_Code_2\input.txt"
FP_OUT = r"SW Assignments\SW_Assignment_3\Files\Branch_Code_2\output.txt"
FP_REPORT = r"SW Assignments\SW_Assignment_3\Files\Branch_Code_2\report.txt"

FP_IN_MULTI = r"SW Assignments\SW_Assignment_3\Files\Test_Cases\TC_Multi\Input"
FP_OUT_MULTI = r"SW Assignments\SW_Assignment_3\Files\Test_Cases\TC_Multi\Output"
FP_REPORT_MULTI = r"SW Assignments\SW_Assignment_3\Files\Test_Case_Reports\TC_Multi"

FP_IN_MOODLE = r"SW Assignments\SW_Assignment_3\Files\Test_Cases\TC_Moodle\Input"
FP_OUT_MOODLE = r"SW Assignments\SW_Assignment_3\Files\Test_Cases\TC_Moodle\Output"
FP_OUT_MOODLE = r"SW Assignments\SW_Assignment_3\Files\Test_Case_Reports\TC_Moodle"

FP_IN_ATTACHED = r"SW Assignments\SW_Assignment_3\Files\Test_Cases\TC_Attached\Input"
FP_OUT_ATTACHED = r"SW Assignments\SW_Assignment_3\Files\Test_Cases\TC_Attached\Output"
FP_REPORT_ATTACHED = r"SW Assignments\SW_Assignment_3\Files\Test_Case_Reports\TC_Attached"

# --------------------------------------- Test Case Bounds ----------------------------------------- #

ALLOWED_GATE_FREQ = [10,25,50,100,250,500,1000]

GATE_DIM_LO = 1
GATE_DIM_HI = 100
MEAN_GATE_DIM = 50
VAR_GATE_DIM_LO = 10
VAR_GATE_DIM_HI  = 25 

MEAN_PIN_POS = 0.5
VAR_PIN_POS_LO = 0.1
VAR_PIN_POS_HI = 0.25

# ------------------------------------- Implementation Bounds -------------------------------------- #

TIME_BOUND_TOTAL_SEC = 20
TIME_BOUND_BUFFER_SEC = 2
IDEAL_PERT_ITER_HI = 6
IDEAL_PERT_ITER_MED = 4
IDEAL_PERT_ITER_LO = 2
CALL_BOUND_TOTAL = 20
BREAK_FLAG_COUNT = 20

MAX_PINS = 40_000

# ==================================== Function Timing Utility ===================================== #

def time_it(func): 

    def wrap_func_timeit(*args, **kwargs): 
        t_start = time() 
        result = func(*args) 
        t_end = time()
        if(not kwargs["supress_time_out"]): 
            print(f'Function {func.__name__!r} executed in {(t_end-t_start):.4f}s and produced output : {result}') 
        return (result,(t_end-t_start))
     
    return wrap_func_timeit

# =================================== Filepath for TestCases IO ==================================== #

def FP_MULTI_CASES_IN(gate_freq, i = None):
    assert gate_freq in ALLOWED_GATE_FREQ, "Invalid Gate Frequency for Multiple Test Cases"
    return FP_IN_MULTI + f"\\{gate_freq} Gates\\tc{i}_{gate_freq}.txt"
    
def FP_MULTI_CASES_OUT(gate_freq, i = None):
    assert gate_freq in ALLOWED_GATE_FREQ, "Invalid Gate Frequency for Multiple Test Cases"
    return FP_OUT_MULTI + f"\\{gate_freq} Gates\\tc{i}_{gate_freq}.txt"

# ====================================== Test Case Generation ====================================== #

def generate_dimensions(mode="normal_hi",dim_lo=1,dim_hi =101,dim_delay = 5):
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
        return floor(np.random.uniform(dim_lo,dim_hi)),floor(np.random.uniform(dim_lo,dim_hi)),floor(np.random.uniform(1,dim_delay+1))
    elif(mode == "normal_lo"):
        for _infit in count(0,1):
            gw,gh = floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_LO)),floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_LO))
            if(dim_lo <= gw <= dim_hi and dim_lo <= gh <= dim_hi):
                return gw,gh,floor(np.random(1,dim_delay+1))
    elif(mode == "normal_hi"):
        for _infit in count(0,1):
            gw,gh = floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_HI)),floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_HI))
            if(dim_lo <= gw <= dim_hi and dim_lo <= gh <= dim_hi):
                return gw,gh,floor(np.random.uniform(1,dim_delay+1))

def generate_pin_positions(gh,gate_freq,pin_density = 0.75,max_pin_freq = 6,override_specs = False, ensure_pins = False, ensure_pins_freq = 10):
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
    
    elif(ensure_pins):
        pin_freq_left = ensure_pins_freq//2
        pin_freq_right = ensure_pins_freq - ensure_pins_freq//2
    
    else:
        pin_freq_left =  min(max_pin_freq_2//2,pin_freq_left)
        pin_freq_right = min(max_pin_freq_2-max_pin_freq_2//2,pin_freq_right)    
        
    arr_left = rng_l.choice(arr,int(pin_freq_left),replace=False,shuffle=False)
    arr_right = rng_r.choice(arr,int(pin_freq_right),replace=False,shuffle=False)
    
    return arr_left, arr_right

def generate_wires(gate_freq,is_done_left,left_edge_data,right_edge_data,br_prob = 10**(-2),ensure_wire_freq_bool=False,
          ensure_wire_freq = 50_000, only_pip_freq = 5):
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
    atleast_one,wire_data,count_atleast_one,wires_generated = {i:False for i in range(1,gate_freq+1)},{},0,0
    comb_loops =def_dict(dict)
    
    rng = np.random.default_rng(randbits(128))
    rng_break = np.random.default_rng(randbits(128))     
    
    only_pips = rng.choice([i for i in range(1,gate_freq+1)],only_pip_freq,replace=False)
    
    while(True):
        g1 = rng.integers(1,gate_freq+1)
        g2 = rng.integers(1,gate_freq+1)
        
        if(g1 == g2 or g2 in only_pips):
            if(ensure_wire_freq_bool):
                if(len(wire_data) >= ensure_wire_freq):
                    break
            else:
                if(count_atleast_one >= gate_freq):
                    if(rng_break.random() < br_prob):
                        break
            continue
        
        elif(False not in is_done_left[g2].values()):
            if(ensure_wire_freq_bool):
                if(len(wire_data) >= ensure_wire_freq):
                    break
            else:
                if(count_atleast_one >= gate_freq):
                    if(rng_break.random() < br_prob):
                        break
            continue
        
        elif(g2 in comb_loops[g1] or g1 in comb_loops[g2]):
            # print(f"Comb Loop Detected {g1} {g2}")
            if(ensure_wire_freq_bool):
                if(len(wire_data) >= ensure_wire_freq):
                    break
            else:
                if(count_atleast_one < gate_freq):
                    continue
                if(rng_break.random() < br_prob):
                    break
        else:
            p1 = rng.choice(right_edge_data[g1])
            p2 = rng.choice(left_edge_data[g2])
            
            while(is_done_left[g2][p2]):
                p2 = rng.choice(left_edge_data[g2])
                            
            wire_data[f"wire g{g1}.p{p1} g{g2}.p{p2}"] = True
            
            comb_loops[g2][g1] = True
            comb_loops[g2].update(comb_loops[g1])
            
            for g in comb_loops:
                if(g2 in comb_loops[g]):
                    comb_loops[g].update(comb_loops[g2])
            
            wires_generated += 1
            
            if(not atleast_one[g1]):
                atleast_one[g1] = True
                count_atleast_one += 1
            if(not atleast_one[g2]):
                atleast_one[g2] = True
                count_atleast_one += 1
            
            is_done_left[g2][p2] = True
                
            
            if(ensure_wire_freq_bool):
                if(len(wire_data) >= ensure_wire_freq):
                    break
            else:
                if(count_atleast_one >= gate_freq):
                    if(rng_break.random() < br_prob):
                        break
    # print(comb_loops)
    # print(f"Total Gates Generated : {gate_freq}")                
    # print(f"Total Wires Generated : {len(wire_data)}")
    return wire_data.keys()

def generate_wires_2(gate_freq,is_done_left, left_edge_data, right_edge_data, br_prob = 10**(-2), ensure_wire_freq_bool=False,
          ensure_wire_freq = 50_000, only_pip_freq = 5):
    
    atleast_one,count_atleast_one,wires_generated = {i:False for i in range(1,gate_freq+1)},0,0
    wire_data, comb_loops = {}, def_dict(dict)

    rng = np.random.default_rng(randbits(128))
    rng_break = np.random.default_rng(randbits(128))
    only_pips = rng.choice([i for i in range(1,gate_freq+1)],only_pip_freq,replace=False)
    
    # print(is_done_left,left_edge_data,right_edge_data)
    bcount = 0

    while bcount < 20:
        
        g_out,g_in = rng.integers(1,gate_freq+1),rng.integers(1,gate_freq+1)
        
        while(g_out == g_in):
            g_in = rng.integers(1,gate_freq+1)
        
        print(f"Choosing g_out : {g_out} , g_in : {g_in}")
        
        if(g_in in only_pips):
            print(f"Only PIP Gate Detected : {g_in}")
            continue
        
        if(False not in is_done_left[g_in].values()):
            print(f"Gate {g_in} input's are full")
            continue
        
        if(g_in in comb_loops[g_out]):
            print(f"Comb Loop Detected {g_out} {g_in}")
            continue
        
        p_out, p_in = rng.choice(right_edge_data[g_out]), rng.choice(left_edge_data[g_in])
        
        while(is_done_left[g_in][p_in]):
            p_in = rng.choice(left_edge_data[g_in])
        
        wire_data[f"wire g{g_out}.p{p_out} g{g_in}.p{p_in}"] = True
        
        comb_loops[g_in][g_out] = True
        comb_loops[g_in].update(comb_loops[g_out])
        
        # print(comb_loops)
        
        if(not atleast_one[g_out]):
                atleast_one[g_out] = True
                count_atleast_one += 1
        if(not atleast_one[g_in]):
            atleast_one[g_in] = True
            count_atleast_one += 1
            
        is_done_left[g_in][p_in] = True
        wires_generated += 1
        bcount += 1
        
    return wire_data.keys()  


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
    do_break = False
    
    while(not do_break):
        assert kw["mode"] in ["uniform","normal_lo","normal_hi"], "Please give a valid testcase generator type"
        
        with open(fpath,"w") as file:
            
            
            left_edge, right_edge, is_done_left = def_dict(list),def_dict(list), def_dict(dict) 
            
            pins_gen = 0
            
            for i in range(1,gate_freq+1):
                
                gw, gh, gd = generate_dimensions(kw["mode"],kw["dim_lo"],kw["dim_hi"])
                file.write(f"g{i} {gw} {gh} {gd}\n")
                file.write(f"pins g{i} ")
                pin_left, pin_right = generate_pin_positions(gh,gate_freq,kw["pin_density"],kw["max_pin_freq"],kw["override_specs"],kw["ensure_pins"],kw["ensure_pins_freq"])
                
                pl,pr = len(pin_left),len(pin_right)
                pins_gen += pl + pr
                
                for j in range(pl+pr):
                    if(0<= j <pl):
                        file.write(f"{0} {pin_left[j]} ")
                        left_edge[i].append(j+1) 
                        is_done_left[i][j+1] = False
                    elif(pl<= j <pl+pr):
                        file.write(f"{gw} {pin_right[j-pl]} ")
                        right_edge[i].append(j+1)
                    
                file.write("\n")
            # print(gate_pins)
            print(f"Total Gates Generated : {gate_freq}")
            print(f"Total Pins Generated : {pins_gen}")
            # print(f"Calling wire generation")
            wire_data = generate_wires(gate_freq,is_done_left,left_edge,right_edge,kw["br_prob"],kw["ensure_wire_freq_bool"],kw["ensure_wire_freq"],kw["only_pip_freq"])
            print(f"Total Wires Generated : {len(wire_data)}")
            file.write(f"wire_delay {kw['wire_delay']}\n")
            
            for wire in wire_data:
                file.write(wire + "\n")
                
            # print(f"Total Pins Generated : {pins_gen}")

        return [gate_freq,pins_gen,len(wire_data)]

# ======================== Helper Functions for Simulated Annealing ============================= #        

IT_BOUND = 10**6

def random_seed_128():
    return randbits(128)

def cooling_rate(T):
    return 0.99

def H_global_coord_pin(gate_ref,pin_index,old_coord):
    pin_ref = gate_ref.pins[pin_index]
    pin_rel_x,pin_rel_y = pin_ref.pin_x,pin_ref.pin_y
    return old_coord[0] + pin_rel_x, old_coord[1] + pin_rel_y

def select_perturb_freq(t):
    if(t < 0.5): 
        return IDEAL_PERT_ITER_HI
    elif(t < 2):
        return IDEAL_PERT_ITER_MED
    elif(t <= 5):
        return IDEAL_PERT_ITER_LO
    else:
        if(t<10):
            return 2
        else:
            return 1
@ time_it
def pseudo_copy_gate_data(gate_data):
    bbox_width,bbox_height = gate_data.get_bbox()
    max_wire_delay = gate_data.max_delay
    gate_packing_data = [gate_data.gates[i].get_gate_tup("parse") for i in range(1,len(gate_data.gates)+1)]
    
    return bbox_width,bbox_height,max_wire_delay,gate_packing_data


 
# ====================================== Misc. Helper Functions ====================================== #

def binary_len(n):
    blen = 0
    if(n==0):      # 0 is a Edge case
        return 1
    while n>0:
        n = n >> 1
        blen+=1
    return blen

def left_cyclic_shift(n,shift):
    return (n << shift) | (n >> (len(bin(n))-2-shift))

def right_cyclic_shift(n,shift):
    return (n >> shift) | (n << (len(bin(n))-2-shift))
# ====================================== __main__ for testing  ====================================== #

if(__name__ == "__main__"):
    kw = {
          "gate_freq": 1000,
          "mode": "uniform",
          "br_prob": 10**(-4),
          "dim_lo":1,
          "dim_hi":101,
          "wire_delay": 1,
          "pin_density": 1.6,
          "max_pin_freq":6,
          "override_specs": False,
          "ensure_pins":False, ### May cause 40_000 pins overflow for largser gate frequencies
          "ensure_pins_freq": 10,
          "ensure_wire_freq_bool": False,
          "ensure_wire_freq": 2_000,
          "only_pip_freq": 1
          }
    
    kw_multi =  {
                    "tc_count" : 10,
                    "force_different_wires" : False,
                    "vary_pins" : True                
                }

    
    write_single_case(kw["gate_freq"],FP_IN,kw)      
    
    # print(bin(35))  
    # print(right_cyclic_shift(35,2))
    # print(bin(568))