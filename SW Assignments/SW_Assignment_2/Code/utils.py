from oops import *
from time import time
from itertools import count
from math import *
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

def generate_dimensions(mode="normal_hi",dim_lo=1,dim_hi =11):
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

def generate_pin_positions(gw,gh,min_pin_freq=3,max_pin_freq = 5,mode="normal_hi"):
    assert mode in ["uniform","normal_lo","normal_hi"], "Please give a valid testcase generator type"
    pin_freq = np.random.randint(min_pin_freq,max_pin_freq+1)
    pins = []
    for i in range(1,pin_freq+1):
        if(mode == "uniform"):
            eta = np.random.uniform(0,1)
        elif(mode == "normal_lo"):
            eta = np.random.normal(MEAN_PIN_POS,VAR_PIN_POS_LO)
        elif(mode == "normal_hi"):
            eta = np.random.normal(MEAN_PIN_POS,VAR_PIN_POS_HI)
        
        gate_side = np.random.randint(1,5)  # 1: Bottom, 2: Right, 3: Top, 4: Left
        
        if(gate_side == 1):                     # Bottom Side
            pins.append((floor(gw*eta),0))
        elif(gate_side == 2):                   # Right Side
            pins.append((gw,floor(gh*eta)))
        elif(gate_side == 3):                   # Top Side
            pins.append((floor(gw*eta),gh))
        elif(gate_side == 4):                   # Left Side
            pins.append((0,floor(gh*eta)))
    
    return pins

def write_single_case(gate_freq,fpath,mode="normal_hi"):
    
    # assert gatefreq%25 == 0 or gatefreq == 10, "Please give a valid test case size"
    assert mode in ["uniform","normal_lo","normal_hi"], "Please give a valid testcase generator type"
    
    with open(fpath,"w") as file:
        pass  

# ============================ Helper Functions for I/O Parsing ================================= #

def Parse_Input(fpath):
    '''
    Returns a object of Gate_Data type
    '''


if(__name__ == "__main__"):
    for i in range(8):
        gw,gh = generate_dimensions(mode="uniform")
        print(gw,gh)    
        print(generate_pin_positions(gw,gh,mode="uniform"))
        print()