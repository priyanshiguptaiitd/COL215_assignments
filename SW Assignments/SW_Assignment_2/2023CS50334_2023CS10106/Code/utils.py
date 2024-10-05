from time import time
from itertools import count
from math import floor
from secrets import randbits
import numpy as np
from matplotlib import pyplot as plt
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

CUST_FP_PATH = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Test_Cases\Analysis"

ALLOWED_GATE_FREQ = [10,25,50,100,250,500,1000]
MEAN_GATE_DIM = 50
VAR_GATE_DIM_LO = 10
VAR_GATE_DIM_HI  = 25 
MEAN_PIN_POS = 0.5
VAR_PIN_POS_LO = 0.1
VAR_PIN_POS_HI = 0.25

TIME_BOUND_TOTAL_SEC = 20
TIME_BOUND_BUFFER_SEC = 2
IDEAL_PERT_ITER_HI = 6
IDEAL_PERT_ITER_MED = 4
IDEAL_PERT_ITER_LO = 2
CALL_BOUND_TOTAL = 20
BREAK_FLAG_COUNT = 20

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

def generate_wires(gate_freq,gate_pins,left_edge_data,br_prob = 10**(-2),ensure_wire_freq_bool=False,
          ensure_wire_freq = 50_000):
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
                wires_generated += 1
                if(not atleast_one[g1]):
                    atleast_one[g1] = True
                    count_atleast_one += 1
                if(not atleast_one[g2]):
                    atleast_one[g2] = True
                    count_atleast_one += 1
                if(count_atleast_one == gate_freq):
                    if(ensure_wire_freq_bool):
                        if(len(wire_data) >= ensure_wire_freq):
                            break
                    else:
                        if(rng_break.random() < br_prob):
                            break
    print(f"Total Gates Generated : {gate_freq}")                
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
        wire_data = generate_wires(gate_freq,gate_pins,left_edge,kw["br_prob"],kw["ensure_wire_freq_bool"],kw["ensure_wire_freq"])
        
        for wire in wire_data:
            file.write(wire + "\n")
            
        print(f"Total Pins Generated : {pins_gen}")

    return [gate_freq,pins_gen,len(wire_data)]
    
@ time_it_no_out
def write_multi_case(kw,kw_multi):
    """
    Writes multiple test cases to a file using generate_dimensions, generate_pin_positions,
    and generate_wires methods on input parameters.

    Args:
        gate_freq (int): The frequency of the gate.
        tc_count (int): The number of test cases to generate.
        fpath (str): The file path to write the test cases.
        kw (dict): A dictionary containing the parameters for test case generation.

    Returns:
        None
    """
    if(kw_multi["force_different_wires"]):
        with open(FP_MULTI_IN+f"\\Special_Report_{kw["gate_freq"]}_{kw_multi["tc_count"]}.txt","w") as file:
            file.write(f"Test Cases for {kw["gate_freq"]} frequency of Gates || Varying Wires\n")
            tc_count = 0
            for b in [-2,-3,-4,-5,-6]:
                for a in [9,8,7,6,5,4,3,2,1]:
                    kw["br_prob"] = a*(10**b)
                    tc_count += 1
                    tc_data,dummy_runtime = write_single_case(kw["gate_freq"],FP_MULTI_CASES_IN(kw["gate_freq"],tc_count),kw,supress_time_out = True)
                    file.write(f"Test Case {tc_count} | No of Gates = {tc_data[0]} | No. of Pins = {tc_data[1]} | No. of Wires = {tc_data[2]}\n")
    elif(kw_multi["vary_pins"]):
        with open(FP_MULTI_IN+f"\\Special_Report_{kw["gate_freq"]}_{kw_multi["tc_count"]}.txt","w") as file:
            file.write(f"Test Cases for {kw["gate_freq"]} frequency of Gates || Varying Pins || Fixing Wires\n")
            tc_count = 0
            for a in range(1,21):
                kw["ensure_wire_freq"] = 10_000*a
                tc_count += 1
                tc_data,dummy_runtime = write_single_case(kw["gate_freq"],FP_MULTI_CASES_IN(kw["gate_freq"],tc_count),kw,supress_time_out = True)
                file.write(f"Test Case {tc_count} | No of Gates = {tc_data[0]} | No. of Pins = {tc_data[1]} | No. of Wires = {tc_data[2]}\n")

    else:   
        with open(FP_MULTI_IN+f"\\Report_{kw["gate_freq"]}_{kw_multi["tc_count"]}.txt","w") as file:
            file.write(f"Generating {kw_multi["tc_count"]} Test Cases for {kw["gate_freq"]} frequency of Gates\n")
            for i in range(1,kw_multi["tc_count"]+1):
                tc_data,dummy_runtime = write_single_case(kw["gate_freq"],FP_MULTI_CASES_IN(kw["gate_freq"],i),kw,supress_time_out = True)
                file.write(f"Test Case {i} | No of Gates = {tc_data[0]} | No. of Pins = {tc_data[1]} | No. of Wires = {tc_data[2]}\n")
                
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
    wire_length = gate_data.wire_length
    gate_packing_data = [gate_data.gates[i].get_gate_tup() for i in range(1,len(gate_data.gates)+1)]
    
    return bbox_width,bbox_height,wire_length,gate_packing_data

# ======================== Helper Functions for Test Case Analysis ============================== #

def visualize_test_case(fpath):
    
    # Initialize lists to store data
    data = []

    # Read the file and extract data
    with open(fpath, "r") as file:
        lines = file.readlines()
        # print(lines)
        for i in range(0,len(lines),5):
            g_freq= int((lines[i+1].strip()).split()[-1])
            w_freq  = int((lines[i+3].strip()).split()[-1])
            r_time = float((lines[i+4].strip()).split()[-2])
            data.append((w_freq,r_time))
    data.sort(key=lambda x: x[0])
    
    num_wires = [x[0] for x in data][30:41]
    runtimes = [x[1] for x in data][30:41]
    
    # Plot the data
    print(data)
    plt.figure(figsize=(10, 6))
    plt.plot(num_wires, runtimes, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Wires in Netlist')
    plt.ylabel('Runtime of one anneal_pack call (seconds)')
    plt.title('Runtime vs Number of Wires - For 100 Gates')
    plt.grid(True)
    plt.show()

def visualize_test_case_2(fpath):
    data = []
    with open(fpath,"r") as file:
        lines = file.readlines()    
        for i in range(0,len(lines)):
            line_data = (lines[i].strip()).split()
            data.append((int(line_data[-2]),int(line_data[-1])))
    print(data)
    
    num_ITERATIONS = [x[0] for x in data]
    System_Cost = [x[1] for x in data]
    
    # Plot the data
    # print(data)
    plt.figure(figsize=(10, 6))
    plt.plot(num_ITERATIONS, System_Cost, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Iterations ran inside a single anneal_pack call')
    plt.ylabel('Wire Cost of the Packing')
    plt.title('Evolution of Wire Cost by anneal_pack')
    plt.grid(True)
    plt.show()

def visualize_test_case_3():
    fpaths = [r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Report\Graphs\TC_Anneal_Pack\output.txt",
              r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Report\Graphs\TC_Anneal_Pack\output1.txt",
              r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Report\Graphs\TC_Anneal_Pack\output2.txt",
              r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Report\Graphs\TC_Anneal_Pack\output3.txt",
              r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Report\Graphs\TC_Anneal_Pack\output4.txt"]
    data = [list() for _ in range(5)]
    
    for j in [0,1,2,3,4]:
        with open(fpaths[j],"r") as file:
            lines = file.readlines()    
            for i in range(0,len(lines)):
                line_data = (lines[i].strip()).split()
                data[j].append((int(line_data[-2]),int(line_data[-1])))

    
    n0, c0 = [x[0] for x in data[0]], [x[1] for x in data[0]]
    n1, c1 = [x[0] for x in data[1]], [x[1] for x in data[1]]
    n2, c2 = [x[0] for x in data[2]], [x[1] for x in data[3]]
    n3, c3 = [x[0] for x in data[3]], [x[1] for x in data[3]]
    n4, c4 = [x[0] for x in data[4]], [x[1] for x in data[4]]    
    # Plot the data
    print(data)
    plt.figure(figsize=(10, 6))
    
    plt.plot(n0,c0, marker='o', linestyle='-', color='b',label="p = 1")
    plt.plot(n1,c1, marker='o', linestyle='-', color='g',label="p = 2")    
    plt.plot(n2,c2, marker='o', linestyle='-', color='r',label="p = 3")
    # plt.plot(n3,c3, marker='o', linestyle='-', color='c',label="p = 4")
    plt.plot(n4,c4, marker='o', linestyle='-', color='m',label="p = 5")
    
    plt.xlabel('Number of Iterations ran inside a single anneal_pack call')
    plt.ylabel('Wire Cost of the Packing')
    plt.title('Evolution of Wire Cost by anneal_pack for different values of perturb_freq')
    plt.legend(loc="lower left")
    plt.grid(True)
    plt.show()

def visualize_test_case_4():
    fpath = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Code\output5.txt"
    data = []
    with open(fpath,"r") as file:
        lines = file.readlines()    
        for i in range(0,len(lines)):
            line_data = (lines[i].strip()).split()
            data.append((int(line_data[-2]),float(line_data[-1])))
    # print(data)
    
    xdata = [x[0] for x in data]
    ydata = [x[1] for x in data]
    
    # Plot the data
    # print(data)
    plt.figure(figsize=(10, 6))
    plt.plot(xdata, ydata, marker='o', linestyle='-', color='r')
    plt.xlabel('Value of perturb_freq parameter for anneal_pack') 
    plt.ylabel('Runtime of one anneal_pack call (seconds)')
    plt.title('Evolution of Wire Cost by anneal_pack')
    plt.grid(True)
    plt.show()

def visualize_test_case_5():
    fpath = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Test_Cases\Analysis\Special_Report_Inverse.txt"
    data = []
    
    with open(fpath,"r") as file:
        lines = file.readlines()    
        for i in range(0,len(lines)):
            line_data = (lines[i].strip()).split()
            data.append((int(line_data[-2]),float(line_data[-1])))
    
    print(data)
    
    xdata = [x[0] for x in data]
    ydata = [x[1] for x in data]
    
    # Plot the data
    # print(data)
    plt.figure(figsize=(10, 6))
    plt.plot(xdata, ydata, marker='o', linestyle='-', color='b')
    plt.xlabel('Frequency of Gates') 
    plt.ylabel('Runtime of one anneal_pack call (seconds)')
    plt.title('Variation of Runtime of one anneal_pack call - Fixed Number of Wires (1_00_000)')
    plt.grid(True)
    plt.show()

def visualize_test_case_6():
    fpath = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Test_Cases\Analysis\Special_Report_Vary_Wires_Fix_Pins.txt"
    data = []
    
    with open(fpath,"r") as file:
        lines = file.readlines()    
        for i in range(0,len(lines),6):
            data.append((int(lines[i+3].strip().split()[-1]),float(lines[i+5].strip().split()[-2])))
    
    xdata = [x[0] for x in data][5::]
    ydata = [x[1] for x in data][5::]
          
    plt.figure(figsize=(10, 6))
    plt.ylim(0,20)
    plt.plot(xdata, ydata, marker='o', linestyle='-', color='r')
    plt.xlabel('Number of Wires in Netlist') 
    plt.ylabel('Runtime of one anneal_pack call (seconds)')
    plt.title('Variation of Runtime of one anneal_pack call - 500 Gates and Number of Pins ~ 12_000')
    plt.grid(True)
    plt.show()
    
if(__name__ == "__main__"):
    kw = {
          "gate_freq": 900,
          "mode": "uniform",
          "br_prob": 10**(-5),
          "dim_lo":1,
          "dim_hi":101,
          "pin_density": 1.7,
          "max_pin_freq":4,
          "override_specs":False,
          "ensure_max_pins":False, ### May cause 40_000 pins overflow for largser gate frequencies
          "ensure_wire_freq_bool": True,
          "ensure_wire_freq": 3_21_127
          }
    kw_multi =  {
                   "tc_count" : 10,
                   "force_different_wires" : False,
                   "vary_pins" : True                
                }
    
    write_single_case(kw["gate_freq"],FP_SINGLE_IN,kw,supress_time_out=False)
    # write_multi_case(kw,kw_multi,supress_time_out=False)
    # for gfreq in range(50,1001,50):
    #     kw["gate_freq"] = gfreq
    #     write_single_case(kw["gate_freq"],CUST_FP_PATH+f"\\tc_{gfreq}.txt",kw,supress_time_out=False)
    # write_single_case(kw["gate_freq"],FP_SINGLE_IN,kw,supress_time_out=False)
    # visualize_test_case_6()
    print("Done")
    
    