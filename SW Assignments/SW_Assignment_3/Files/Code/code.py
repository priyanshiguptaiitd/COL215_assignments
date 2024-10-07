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
    gate_data.set_gate_env()            
    
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