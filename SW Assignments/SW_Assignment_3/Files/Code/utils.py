# ===================================== Import of Libraries ======================================== #

from collections import defaultdict as def_dict
from random import randint as rint
from math import sqrt, ceil, floor
from time import time
from itertools import count
from secrets import randbits
import numpy as np
from matplotlib import pyplot as plt

# =====================================-= Project Constants ======================================== #

# ------------------------------------------ File Paths -------------------------------------------- #

FP_IN = r"SW Assignments\SW_Assignment_3\Files\Code\input.txt"
FP_OUT = r"SW Assignments\SW_Assignment_3\Files\Code\output.txt"
FP_REPORT = r"SW Assignments\SW_Assignment_3\Files\Code\report.txt"

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
            print(f'Function {func.__name__!r} executed in {(t_end-t_start):.4f}s and produced output : {result} \n') 
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

def generate_dimensions(mode = "normal_hi", dim_lo = GATE_DIM_LO, dim_hi = GATE_DIM_HI+1):
    
    assert mode in ["uniform","normal_lo","normal_hi"], Exception("Invalid Mode for Dimension Generation")
    
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

# ====================================== Misc. Helper Functions ====================================== #

def binary_len(n):
    blen = 0
    if(n==0):      # 0 is a Edge case
        return 1
    while n>0:
        n = n >> 1
        blen+=1
    return blen

# ====================================== __main__ for testing  ====================================== #

if(__name__ == "__main__"):
    with open(FP_IN,"w") as file:
        file.write("g1 10 10 1\n")        