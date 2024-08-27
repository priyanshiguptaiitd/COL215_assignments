import numpy as np
from random import randint
from math import floor
from itertools import count
from project_constants import *

from code_timer import *
from os import remove as del_file_at


@ time_it_no_out
def write_single_case(gatefreq,fpath,mode="normal_hi"):
    
    # assert gatefreq%25 == 0 or gatefreq == 10, "Please give a valid test case size"
    assert mode in ["uniform","normal_lo","normal_hi"], "Please give a valid testcase generator type"
    
    with open(fpath,"w") as file:
        if(mode == "uniform"):
            for i in range(1,gatefreq+1):
                rw,rh = floor(np.random.uniform(1,101)),floor(np.random.uniform(1,101))
                file.write(f"g{i} {rw} {rh}\n")
        if(mode == "normal_lo"):
            for i in range(1,gatefreq+1):
                for _infit in count(0,1):
                    rw,rh = floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_LO)),floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_LO))
                    if(1 <= rw <= 100 and 1<= rh <= 100):
                        file.write(f"g{i} {rw} {rh}\n")
                        break
        if(mode == "normal_hi"):
            for i in range(1,gatefreq+1):
                for _infit in count(0,1):
                    rw,rh = floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_HI)),floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_HI))
                    if(1 <= rw <= 100 and 1<= rh <= 100):
                        file.write(f"g{i} {rw} {rh}\n")
                        break
                    
                            
@ time_it_no_out    
def write_multi_cases(gatefreq,tc_freq,mode="normal_hi"):
    assert gatefreq in [10,25,50,100,250,500,1000], "Please give a valid test case size"
    assert mode in ["uniform","normal_lo","normal_hi"], "Please give a valid testcase generator type"
    for i in range(1,tc_freq+1):
        with open(FP_MULTI_CASES_IN(i,gatefreq), "w") as file:
            if(mode == "uniform"):
                for i in range(1,gatefreq+1):
                    rw,rh = floor(np.random.uniform(1,101)),floor(np.random.uniform(1,101))
                    file.write(f"g{i} {rw} {rh}\n")
            if(mode == "normal_lo"):
                for i in range(1,gatefreq+1):
                    for _infit in count(0,1):
                        rw,rh = floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_LO)),floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_LO))
                        if(1 <= rw <= 100 and 1<= rh <= 100):
                            file.write(f"g{i} {rw} {rh}\n")
                            break
            if(mode == "normal_hi"):
                for i in range(1,gatefreq+1):
                    for _infit in count(0,1):
                        rw,rh = floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_HI)),floor(np.random.normal(MEAN_GATE_DIM,VAR_GATE_DIM_HI))
                        if(1 <= rw <= 100 and 1<= rh <= 100):
                            file.write(f"g{i} {rw} {rh}\n")
                            break

@ time_it_no_out
def remove_multi_cases(gatefreq,tc_freq):
    assert gatefreq in ALLOWED_GATE_FREQ, "Please give a valid test case size"
    for i in range(1,tc_freq+1):
        try: 
            del_file_at(FP_MULTI_CASES_IN(i,gatefreq))
            del_file_at(FP_MULTI_CASES_OUT(i,gatefreq)) 
        except OSError as error:  
            print("File path invalid or Can't be removed, Terminating File Deletion operation")
            return