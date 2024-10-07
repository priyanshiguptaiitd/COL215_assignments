from oops import *
from utils import *
import sys

# ============================ Helper Functions for I/O Parsing ================================= #
sys.setrecursionlimit(5*10**6)

# TODO - FIX these  for newproblem statements

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
                for i in range(2,len(line_data),2):
                    pin_index,pin_x,pin_y = i//2,int(line_data[i]),int(line_data[i+1])
                    gate_data.add_pin(gate_index,pin_index,pin_x,pin_y)
            elif(line_data[0].lower() == "wire_delay"):
                gate_data.set_wire_delay(int(line_data[1]))
            elif(line_data[0].lower() == "wire"):
                gp_i,gp_j = line_data[1].split('.'),line_data[2].split('.') 
                g_i,p_i = int(gp_i[0][1:]),int(gp_i[1][1:])
                g_j,p_j = int(gp_j[0][1:]),int(gp_j[1][1:])
                # print(g_i,p_i,g_j,p_j)
                gate_data.add_wire(g_i,p_i,g_j,p_j)
               
    gate_data.init_packing()
    gate_data.init_wire_groups()
    
    return gate_data

# ============================ Functions for Automated Test Case ================================= #

# ============================= __main__ for Testing Purposes ==================================== #

if(__name__ == "__main__"):
    gd = Parse_Input(FP_IN)
    print(gd)
    print("Exited Input Parsing")
    