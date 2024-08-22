"""
Storing Constants / Literals that are being Used across the programmes
    
"""
FP_SINGLE_CASE_IN = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\input.txt"
FP_SINGLE_CASE_OUT =  r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\output.txt"
ALLOWED_GATE_FREQ = [10,25,50,100,250,500,1000]
MEAN_GATE_DIM = 50
VAR_GATE_DIM_LO = 10
VAR_GATE_DIM_HI  = 25 
PACK_EFF_BOUND = 0.95
DIM_INC_FAILTC = 1.5
DIM_DELTA_PEFF = 0.05
ALPHA_MARGIN_DIM = 1.1
TC_RUNTIME_BOUND = 2
MAX_IT_BOUND = 20


def FP_MULTI_CASES_IN(i,gate_freq):
    assert gate_freq in ALLOWED_GATE_FREQ, "Invalid Gate Frequency for Multiple Test Cases"
    return r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\SW_Assignment_1_Files\Multi_Cases\Input_Test_Cases_Multi" + f"\\{gate_freq} Gates\\tc{i}_{gate_freq}.txt"
    
def FP_MULTI_CASES_OUT(i=None,gate_freq=None):
    assert gate_freq in ALLOWED_GATE_FREQ, "Invalid Gate Frequency for Multiple Test Cases"
    if (i is not None):
        return r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\SW_Assignment_1_Files\Multi_Cases\Output_Test_Cases_Multi" + f"\\{gate_freq} Gates\\tc{i}_{gate_freq}.txt"
    else:
        return r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\SW_Assignment_1_Files\Multi_Cases\Output_Test_Cases_Multi" + f"\\Report_{gate_freq}_Multi.txt" 
    
def ALPHA_MARGIN(gate_frequency):
    if(gate_frequency >= 100):
        return 1.1
    elif(gate_frequency >= 50):
        return 1.2
    else:
        return 1.5