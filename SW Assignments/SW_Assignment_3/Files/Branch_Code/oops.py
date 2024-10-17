from typing import Any
from utils import *
# print(choice([1,2,3,4,5,6,7,8,9,10]))

# ========================================== OOP's Helper Functions ========================================== #

class dp_state:
    def __init__(self):
        self.minx,self.miny,self.maxx,self.maxy = None,None,None,None
        self.prev_gate, self.max_sp = None, None
        self.total_gate_delay = None
        self.current_path_length = None
        
class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    # ------------- Constructor for Heap Helper Functions ------------- #
    def __init__(self, comparison_function,mode, init_array):
        self.heap = list()
        self.mode = mode
        self.comparison_function = comparison_function
        self.hash_table_values = def_dict(int)           # To store the index of the value in the heap for O(log(n)) removal in gen    
        
        if(len(init_array)>0):
            self.heap = init_array
            parent = self.parent_index(len(self.heap)-1)
            for i in range(parent,-1,-1):
                self.down_heap(i)
                # print(self.heap)
        
        for i in range(len(self.heap)):
            self.hash_table_values[heap_key_hash(self.heap[i])] = i
    # ------------- Indexing and General Helper Functions ------------- #
    def __len__(self):
        return len(self.heap)
    
    def __str__(self):
        return str(self.heap)
    
    def __repr__(self):
        return str(self.heap)
    
    def index_in_range(self,i):
        return True if(0<=i<len(self.heap)) else False
    
    def is_heap_empty(self):
        return True if(len(self.heap)==0) else False
    
    def is_heap_full(self):
        l = len(self.heap)
        if(l==0):
            return False,None
        bin_max_size_curr_heap = binary_len(l)
        if(l == 2**(bin_max_size_curr_heap) - 1):
            return True,l
        else:
            return False,2**(bin_max_size_curr_heap) - 1
    
    def parent_index(self,i):
        return (i-1)//2 if(i%2==1) else (i-2)//2 
    
    def children_indices(self,i):
        return 2*i+1,2*i+2
    
    # ----------------- Up Heap / Down Heap Functions ----------------- #
    
    def swap_data(self,i,j):
        if(self.index_in_range(i) and self.index_in_range(j)):
            self.heap[i],self.heap[j] = self.heap[j],self.heap[i]
            self.hash_table_values[heap_key_hash(self.heap[i])] = i
            self.hash_table_values[heap_key_hash(self.heap[j])] = j
        else:
            raise IndexError("Index out of range for Heap")
    
    def down_heap(self,i):
        if(self.index_in_range(i)):
            left_child,right_child = self.children_indices(i)
            # print(left_child,right_child)
            smaller_child = i
            if(self.index_in_range(left_child) and self.comparison_function(self.heap[left_child],self.heap[smaller_child],self.mode)):
                smaller_child = left_child
            if(self.index_in_range(right_child) and self.comparison_function(self.heap[right_child],self.heap[smaller_child],self.mode)):
                smaller_child = right_child
            if(smaller_child!=i):
                self.swap_data(i,smaller_child)
                self.down_heap(smaller_child)
        else:
            pass
        
    def up_heap(self,i):
        if(self.index_in_range(i)):
            parent = self.parent_index(i)
            if(self.index_in_range(parent) and self.comparison_function(self.heap[i],self.heap[parent],self.mode)):
                self.swap_data(parent,i)
                self.up_heap(parent)
        else:
            raise IndexError("Index out of range for Heap")
    
    # ---------------- Insertion and Deletion Functions --------------- #    
    def insert(self, obj):
        self.heap.append(obj)
        self.up_heap(len(self.heap)-1)
        pass
    
    def extract(self):
        
        if(len(self.heap)>0):
            self.swap_data(0,len(self.heap)-1)
            extracted_val = self.heap.pop()
            self.down_heap(0)
            return extracted_val

    def remove(self,obj):
        if(len(self.heap)>0):
            assert heap_key_hash(obj) in self.hash_table_values, Exception("Hashing Error : Object not present in Heap")
            assert self.index_in_range(self.hash_table_values[heap_key_hash(obj)]), Exception("Hashing Error : Object not present in Heap - Out of Bounds Index")
            key_index = self.hash_table_values[heap_key_hash(obj)]
            self.swap_data(key_index,len(self.heap)-1)
            extracted_val = self.heap.pop()
            self.down_heap(key_index)
            return extracted_val
        else:
            raise IndexError("Heap is Empty")        
    
    def top(self):

        if(len(self.heap)>0):
            return self.heap[0]
        else:
            return None
    
class Gate_Env:
    
    def __init__(self,gate_index,gate_width,gate_height,gate_delay):
        
        self.index = gate_index
        self.width = gate_width
        self.height = gate_height
        self.delay = gate_delay
        self.dp_state = None
        
        self.pins = def_dict()
        self.critical_paths = None
        self.affected_wire_groups_to = set()
        self.affected_wire_groups_from = set()

        
        self.envelope_x, self.envelope_y = None,None
        self.x_rel_env, self.y_rel_env = None,None
        self.x, self.y = None,None
    
    def set_coord_env(self,env_x,env_y):
        
        self.envelope_x, self.envelope_y = env_x,env_y
        
    def set_coord_rel_env(self,envelope_width,envelope_height,Delta_x,Delta_y):
        
        assert 0 <= Delta_x <= envelope_width-self.width, f"Gate goes out of Envelope (X Direction) : {Delta_x} , {self.width} , {envelope_width}"
        assert 0 <= Delta_y <= envelope_height-self.height, f"Gate goes out of Envelope (Y Direction) : : {Delta_y} , {self.height} , {envelope_height}"
        self.x_relative_env,self.y_relative_env = Delta_x,Delta_y
        self.x = self.envelope_x + Delta_x
        self.y = self.envelope_y + Delta_y
    
    def set_affected_wire_groups(self):
        for pin_index in self.pins:
            pin_ref = self.pins[pin_index]
            for g_ind_to in pin_ref.connected_pins_to:
                for p_ind_to in pin_ref.connected_pins_to[g_ind_to]:
                    self.affected_wire_groups_to.add((g_ind_to,p_ind_to))
    
    def add_pin(self,pin_index,pin_x,pin_y):
        
        self.pins[pin_index] = Pin(self,self.index,pin_index,pin_x,pin_y)
        pass
    
    def get_global_coord(self):
        
        return (self.x,self.y)
    
    def get_global_coord_pin(self,pin_index):
        
        pin_ref = self.pins[pin_index]
        pin_rel_x, pin_rel_y = pin_ref.pin_x, pin_ref.pin_y
        return (self.x + pin_rel_x, self.y + pin_rel_y)
    
    def get_gate_tup(self,mode="parse"):
        
        assert mode in ["parse","desc"], Exception("Invalid Mode : Must be 'parse' or 'desc'")
        
        if(mode == "parse"):
            return (self.index, self.x, self.y)
        elif(mode == "desc"):
            return (self.index, self.envelope_x, self.envelope_y,
                    self.x_relative_env, self.y_relative_env)
    
    def __str__(self):
        
        basic_data = f"Gate : {self.index} || Pos_X : {self.x} || Pos_Y {self.y} || Width : {self.width} || Height : {self.height}"
        pin_data = [f"Pin : {pin_index} || Parent_Gate : {self.index} || Pin_X : {self.get_global_coord_pin(pin_index)[0]} || Pin_Y : {self.get_global_coord_pin(pin_index)[1]}" for pin_index in self.pins]
        return "\n" + basic_data + "\n" + "\n".join(pin_data)
    
    def __repr__(self) -> str:
        return f"Gate : {self.index} || Pos_X : {self.x} || Pos_Y {self.y} || Width : {self.width} || Height : {self.height}"
    
class Pin:
    
    def __init__(self,parent_ref, gate_index, pin_index, pin_x,pin_y):
        assert isinstance(parent_ref,Gate_Env), Exception("Invalid Type : Parent Reference of a Pin must be Gate_Env type")   
        self.parent_ref = parent_ref
        self.parent_index = gate_index
        self.index = pin_index
        self.pin_x, self.pin_y = pin_x, pin_y
        self.connected_pins_to = def_dict(list)
        self.connected_pins_from = def_dict(list)
        self.connected_pins_to[gate_index] = [self]
    
    def get_global_coord(self):
        return self.parent_ref.get_global_coord_pin(self.index)
    
    def __str__(self):
        
        basic_data = f"Pin No = {self.index} || Parent Gate = g{self.parent_index} || Pin_x = {self.pin_x} || Pin_y = {self.pin_y}"
        connected_from = [f"Connections of form gx.py --------> g{self.parent_index}.p{self.index}"]
        connected_to = [f"Connections of form g{self.parent_index}.p{self.index} --------> gx.py"]
        
        for g_ind_to in self.connected_pins_to:
            for p_ind_to in self.connected_pins_to[g_ind_to]:
                connected_to.append(f"Wire || g{self.parent_index}.p{self.index} --------> g{g_ind_to}.p{p_ind_to}")
        for g_ind_from in self.connected_pins_from:
            for p_ind_from in self.connected_pins_from[g_ind_from]:
                connected_from.append(f"Wire || g{g_ind_from}.p{p_ind_from} --------> g{self.parent_index}.p{self.index}")        
        
        return basic_data + "\n" + "\n".join(connected_to) + "\n" + "\n".join(connected_from)

    def __repr__(self):
        return f"Pin No = {self.index} || Parent Gate = g{self.parent_index} || Pin_x = {self.pin_x} || Pin_y = {self.pin_y}"    

class Wire_Group:
    
    def __init__(self,gate_index,pin_index,connected_pins_to) -> None:
        self.key = (gate_index,pin_index)
        self.member_count = len(connected_pins_to)
        self.xmin = Heap(comparator_func_pins,"min_x",connected_pins_to[::])
        self.xmax = Heap(comparator_func_pins,"max_x",connected_pins_to[::])
        self.ymin = Heap(comparator_func_pins,"min_y",connected_pins_to[::])
        self.ymax = Heap(comparator_func_pins,"max_y",connected_pins_to[::])
        self.wire_group_length = None
    
    def adjust_wire_group(self,affected_con_pins):
        for pin_ref in affected_con_pins:
            pref_xmin = self.xmin.remove(pin_ref)
            self.xmin.insert(pref_xmin)
            pref_ymin = self.ymin.remove(pin_ref)
            self.ymin.insert(pref_ymin)
            pref_xmax = self.xmax.remove(pin_ref)
            self.xmax.insert(pref_xmax)
            pref_ymax = self.ymax.remove(pin_ref)
            self.ymax.insert(pref_ymax)        
        
    def set_bbox_wg(self):
        self.wire_group_length = self.xmax.top().get_global_coord()[0] - self.xmin.top().get_global_coord()[0]+ self.ymax.top().get_global_coord()[1] - self.ymin.top().get_global_coord()[1]
    
    def __len__(self):
        return self.wire_group_length 
    
    def __str__(self):
        basic_data_wg = f"\nWire_Group : {self.key} || X_min : {self.xmin.top().get_global_coord()[0]} || Y_min : {self.ymin.top().get_global_coord()[1]} || X_max : {self.xmax.top().get_global_coord()[0]} || Y_max : {self.ymax.top().get_global_coord()[1]} || Wire_Legth : {self.wire_group_length} || Members : {self.member_count}"
        pin_data_wg = []
        for pin_ref in self.xmin.heap:
            pin_data_wg.append(f"Member : {len(pin_data_wg)+1} || Parent Gate : {pin_ref.parent_index} || Pin : {pin_ref.index}")
        return basic_data_wg + "\n" + "\n".join(pin_data_wg)

    def __repr__(self):
        return f"Wire_Group : {self.key} || X_min : {self.xmin.top().get_global_coord()[0]} || Y_min : {self.ymin.top().get_global_coord()[1]} || X_max : {self.xmax.top().get_global_coord()[0]} || Y_max : {self.ymax.top().get_global_coord()[1]} || Wire_Legth : {self.wire_group_length} || Members : {self.member_count}"
            
class Gate_Data:
    
    def __init__(self):
        
        self.gates = def_dict()
        self.wire_dag, self.wire_groups, self.gate_dag_from,self.gate_dag_to = def_dict(dict), def_dict(), def_dict(dict), def_dict(dict)  
        self.primary_inputs, self.primary_outputs = def_dict(), def_dict()
        self.primary_input_gates, self.primary_output_gates = def_dict(), def_dict()
        
        self.gate_wire_groups_keys = def_dict(list)
        self.gate_wire_groups = def_dict()
        
        self.critical_path_count = 0
        self.total_wires_added = 0
        self.total_pins_added = 0
        self.bbox = (None,None)
        self.max_width,self.max_height = 0,0
        
        self.wire_delay = None
        self.max_delay = None
    
    def set_bbox(self,x,y):
        self.bbox = (x,y)
    
    def get_bbox(self):
        return self.bbox[0],self.bbox[1]
   
    def set_wire_delay(self,wire_delay):
        
        self.wire_delay = wire_delay    
    
    def add_gate(self,gate_index,gate_width,gate_height,gate_delay):
        self.gates[gate_index] = Gate_Env(gate_index,gate_width,gate_height,gate_delay)
        self.max_width = self.max_width if(self.max_width > gate_width) else gate_width
        self.max_height = self.max_height if(self.max_height > gate_height) else gate_height
        
    def get_gate(self,gate_index):
        return self.gates[gate_index]
    
    def add_pin(self,gate_index,pin_index,pin_x,pin_y):
        self.gates[gate_index].add_pin(pin_index,pin_x,pin_y)
        self.total_pins_added += 1
    
    def get_pin(self,gate_index,pin_index):
        return self.gates[gate_index].pins[pin_index]
    
    def add_wire(self,g_i,p_i,g_j,p_j):
        p_i_ref,p_j_ref = self.gates[g_i].pins[p_i],self.gates[g_j].pins[p_j]
        p_i_ref.connected_pins_to[g_j].append(self.gates[g_j].pins[p_j])
        p_j_ref.connected_pins_from[g_i].append(self.gates[g_i].pins[p_i])
        self.wire_dag[(g_i,p_i)][(g_j,p_j)] = True
        self.gate_dag_from[g_i][g_j] = True
        self.gate_dag_to[g_j][g_i] = True
        self.total_wires_added += 1
    
    def get_crtical_path(self):
        pass
    
    def get_critical_path_delay(self):
        pass
    
    @time_it
    def init_packing(self):
        gate_frequency = len(self.gates)
        bb_dim,bb_cell_w,bb_cell_h = ceil(sqrt(gate_frequency)), self.max_width, self.max_height                
        for i in range(1,len(self.gates)+1):
            if(i%bb_dim==0):
                self.gates[i].set_coord_env(((i-1)%bb_dim)*bb_cell_w,(i//bb_dim-1)*bb_cell_h)
                self.gates[i].set_coord_rel_env(bb_cell_w,bb_cell_h,(bb_cell_w-self.gates[i].width)//2,(bb_cell_h-self.gates[i].height)//2)
            else:
                self.gates[i].set_coord_env(((i-1)%bb_dim)*bb_cell_w,(i//bb_dim)*bb_cell_h)
                self.gates[i].set_coord_rel_env(bb_cell_w,bb_cell_h,(bb_cell_w-self.gates[i].width)//2,(bb_cell_h-self.gates[i].height)//2)

    @time_it  
    def init_wire_groups(self):        
        for gate_index,pin_index in self.wire_dag:
            if(len(self.gates[gate_index].pins[pin_index].connected_pins_from) == 0):
                self.primary_inputs[(gate_index,pin_index)] = True
                # self.primary_input_gates[gate_index] = True
                                
            pin_ref = self.gates[gate_index].pins[pin_index]
            pin_ref_pin_obj = []                
            for g_ind_to in pin_ref.connected_pins_to:
                for pin_obj in pin_ref.connected_pins_to[g_ind_to]:
                    if(len(pin_obj.connected_pins_to) == 1):
                        self.primary_outputs[(g_ind_to,pin_obj.index)] = True
                        self.primary_output_gates[g_ind_to] = True
                    # pin_ref_pin_obj.append(pin_obj) 
                pin_ref_pin_obj.extend(pin_ref.connected_pins_to[g_ind_to])                            
            self.wire_groups[(gate_index,pin_index)] = Wire_Group(gate_index,pin_index,pin_ref_pin_obj)
            self.wire_groups[(gate_index,pin_index)].set_bbox_wg()
            self.gate_wire_groups_keys[gate_index].append(pin_index)
        
        for gate_index in self.gates:
            self.gate_wire_groups[gate_index] = Heap(comparator_func_wg,"max",[self.wire_groups[(gate_index,pin_index)] for pin_index in self.gate_wire_groups_keys[gate_index]])
            if(self.gate_dag_to[gate_index] == {}):
                self.primary_input_gates[gate_index] = True

    @time_it
    def init_critical_paths(self):
        all_paths = []
        for pip in self.primary_inputs:
            # print(pip)
            stack,visited = [pip],dict()
            while stack:
                # print(stack)
                for neighbour in self.wire_dag[stack[-1]]:
                    if(neighbour not in visited):
                        visited[neighbour] = True
                        stack.append(neighbour)
                        break
                else:
                    # print("Hi",stack[-1],self.primary_outputs)
                    if(stack[-1] in self.primary_outputs):
                        all_paths.append(stack[::])
                    stack.pop()


        self.critical_paths = all_paths
    
    def __str__(self):
        basic_data = '\n'+" Netlist Information ".center(120,"=") + '\n'
        basic_data +=  f"\nTotal Gates : {len(self.gates)} || Total Pins : {self.total_pins_added} || Total Wires : {self.total_wires_added}"
        
        gate_data_str = ['\n'+" Gate Information ".center(120,"=")]
        for gate_ref in self.gates:
            gate_data_str.append(str(self.gates[gate_ref])) 
        
        wire_group_data_str = ['\n'+ " Wire Group Information ".center(120,"=")]
        wire_group_data_str.append(f"\nTotal Wire Groups : {len(self.wire_groups)}")
        for wire_group_ref in self.wire_groups:
            wire_group_data_str.append(str(self.wire_groups[wire_group_ref]))

        primary_pin_data = ['\n'+" Primary IO Pins Information ".center(120,"=")]
        primary_pin_data.append(f"\nPrimary Inputs Pins (PIP's) : {len(self.primary_inputs)} || Primary Outputs Pins (POP's) : {len(self.primary_outputs)}\n")
        pip_count,pop_count = 0,0
        for gate_ind,pin_ind in self.primary_inputs:
            pip_count += 1
            primary_pin_data.append(f"PIP : {pip_count} || Parent Gate : {gate_ind} || Pin : {pin_ind}")
        primary_pin_data.append("")
        for gate_ind,pin_ind in self.primary_outputs:
            pop_count += 1
            primary_pin_data.append(f"POP : {pop_count} || Parent Gate : {gate_ind} || Pin : {pin_ind}")           
        
        critical_path_data = ['\n' + " Critical Path Information ".center(120,"=")]
        critical_path_data.append(f"\nTotal Critical Paths : {self.critical_path_count}")
        
        data_end = '\n'+"".center(120,"=")
        return basic_data + "\n" + "\n".join(gate_data_str) + "\n" + "\n".join(wire_group_data_str) + "\n" + "\n".join(primary_pin_data) + "\n" + "\n".join(critical_path_data)+ '\n'+ data_end

    @time_it
    def write_netlist_data(self,fpath):
        with open(fpath,"w") as file:
            s = str(self)
            file.write(s)
        print("Netlist Data Written to File : ",fpath)
    
    
# ========================================== OOP's Helper Functions ========================================== #
    
def heap_key_hash(obj):
    if(isinstance(obj,Gate_Env)):
        return obj.index
    elif(isinstance(obj,Pin)):
        return (obj.parent_index,obj.index)
    elif(isinstance(obj,Wire_Group)):
        return obj.key
    else:
        return obj

def comparator_func_pins(pin_1,pin_2,mode):
    
    assert isinstance(pin_1,Pin) and isinstance(pin_2,Pin), Exception("Invalid Type : Pin object comparator must receive Pin objects")
    assert mode in ["min_x","min_y","max_x","max_y"], Exception("Invalid Mode : Pin object comparator mode must be 'min_x' or 'min_y' or 'max_x' or 'max_y'")
    
    if(mode == "min_x"):
        return pin_1.get_global_coord()[0] < pin_2.get_global_coord()[0]
    elif(mode == "min_y"):
        return pin_1.get_global_coord()[1] < pin_2.get_global_coord()[1]
    elif(mode == "max_x"):
        return pin_1.get_global_coord()[0] > pin_2.get_global_coord()[0]
    elif(mode == "max_y"):
        return pin_1.get_global_coord()[1] > pin_2.get_global_coord()[1]

def comparator_func_wg(wg_1,wg_2,mode):
    assert isinstance(wg_1,Wire_Group) and isinstance(wg_2,Wire_Group), Exception("Invalid Type : Wire Group object comparator must receive Wire Group objects")
    assert mode in ["min","max"], Exception("Invalid Mode : Wire Group object comparator mode must be 'min' or 'max'")
    
    if(mode == "min"):
        return len(wg_1) < len(wg_2)
    elif(mode == "max"):
        return len(wg_1) > len(wg_2)

def comparator_func(x,y,mode):
    
    assert mode in ["min","max"], Exception("Invalid Mode : General Comparator mode must be 'min' or 'max'")

    if(mode == "min"):
        return x < y
    elif(mode == "max"):
        return x > y

# ========================================== __main__ for testing ============================================ #

if(__name__ == "__main__"):
    hp = Heap(comparator_func,"min",[88, 17, 29, 12, 91, 67, 84, 66, 57, 94])
    print(hp)
    print(hp.hash_table_values)
    hp.insert(4)
    hp.insert(1)
    print(hp)
    print(hp.hash_table_values)
