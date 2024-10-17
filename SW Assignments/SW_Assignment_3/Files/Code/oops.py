from typing import Any
from utils import *
# print(choice([1,2,3,4,5,6,7,8,9,10]))

# ========================================== OOP's Helper Functions ========================================== #

class dp_state:
    def __init__(self):
        self.minx,self.miny,self.maxx,self.maxy = None,None,None,None
        self.prev_gate, self.max_sp = None, None
        self.total_gate_delay = None
        
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

class Critical_Path:

    def __init__(self,gate_data_ref):
        assert isinstance(gate_data_ref,Gate_Data), Exception("Invalid Type : Gate Data Reference must be of Gate_Data type")
        self.gd_ref = gate_data_ref 
        self.primary_input,self.primary_output = None,None
        self.path = def_dict()
        self.gate_delay = None
        self.wire_delay = None
        self.delay = None
    
    def set_primary_io(self,pip,pop):
        self.primary_input,self.primary_output = pip,pop
            
class Gate_Data:
    
    def __init__(self):
        
        self.gates = def_dict()
        self.wire_dag, self.wire_groups, self.gate_dag = def_dict(dict), def_dict(), def_dict(dict)  
        self.primary_inputs, self.primary_outputs = def_dict(), def_dict()
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
        self.gate_dag[g_i][g_j] = True
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
            pin_ref = self.gates[gate_index].pins[pin_index]
            pin_ref_pin_obj = []                
            for g_ind_to in pin_ref.connected_pins_to:
                for pin_obj in pin_ref.connected_pins_to[g_ind_to]:
                    if(len(pin_obj.connected_pins_to) == 1):
                        self.primary_outputs[(g_ind_to,pin_obj.index)] = True
                    # pin_ref_pin_obj.append(pin_obj) 
                pin_ref_pin_obj.extend(pin_ref.connected_pins_to[g_ind_to])                            
            self.wire_groups[(gate_index,pin_index)] = Wire_Group(gate_index,pin_index,pin_ref_pin_obj)
            self.wire_groups[(gate_index,pin_index)].set_bbox_wg()
            self.gate_wire_groups_keys[gate_index].append(pin_index)
        
        for gate_index in self.gates:
            self.gate_wire_groups[gate_index] = Heap(comparator_func_wg,"max",[self.wire_groups[(gate_index,pin_index)] for pin_index in self.gate_wire_groups_keys[gate_index]])

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
    
class Simulated_Annealing():
    ''' Basic Description -
    
        Class to perform simulated annealing for optimizing gate placement to minimize wire length
        At the heart, involves generating an deterministic initial packing of gates, perturbing the packing, and accepting or rejecting the perturbation 
        based on the cost difference and temperature and an acceptance function.
        
        Since the probabilistic arguments are used, the packing and perturbing process is not entirely deterministic
        but improves with the number of iterations, intial temperature, perturbations per annealing iteration
        as well as cooling rate.
        
        Probablistic arguments require extensive testing on Test - Cases,
        as well as tweaking of the parameters to get the best results.
    '''
    ''' Attributes:
    
            gate_data (Gate_Data): An instance of the Gate_Data class containing gate and wire information.
            temp (float): The current temperature in the simulated annealing process.
            initial_temp (float): The initial temperature for the simulated annealing process.
            min_temp (float): The minimum temperature to stop the annealing process.
            wire_cost (float): The current wire cost.
            initial_wire_cost (float): The initial wire cost, generated after the initial packing.
    '''
    ''' Methods:
    
            acceptance_probability(old_cost, new_cost):
                Calculates the acceptance probability of a new perturbef solution 
                based on the cost difference and current temperature.
                
                If the new cost is less than the old cost, the new solution is always accepted.
                Otherwise, the acceptance probability is calculated based on the cost difference and temperature.
                
                Returns a boolean indicating whether the new solution is accepted or not
            
            update_wire_cost(l):
                Updates the current wire cost in the Annealing class instance as well as 
                the gate_data attribute and returns it.
            
            wire_cost_function():
                Calculates the total wire length for the current gate placement
                Is expensive with respect to number of wires 
                and should be called only when necessary.
            
            cost_delta_function(g1, g2, old_coord):
                Calculates the change in wire length caused by swapping two gates.
                Heart of the perturbation_v2 function, since we don't need to recalculate 
                the wire length for all the wires.
            
            gen_init_packing():
                Generates an deterministic initial packing (based on order of gates) of gates as 
                well as the bounding box. Sets the initial wire cost and is called 
                whenver a new annealing process is started.
                
            perturb_packing_swap():
                Performs a perturbation by swapping two randomly selected gates and calculates the new wire cost
                by the wire_cost_function method.
                
                Accepts or rejects the perturbation based on the acceptance_probability method.
                If rejected then the gates environments are reset to the old values. 
            
            perturb_packing_swap_v2():
                Performs a perturbation by swapping two randomly selected gates and 
                calculates the delta wire cost using cost_delta_function.

                Accepts or rejects the perturbation based on the acceptance_probability method.
                If rejected then the gates environments are reset to the old values.
                
                ---- Significantly faster than perturb_packing_swap ----
                
            perturb_packing_move():
                Performs a perturbation by moving a randomly selected gate to a new position.
                Not Yet Implemented.
                
            anneal_to_pack(perturb_freq_per_iter=5):
                Performs the simulated annealing process to optimize gate placement.
                Implements the core logic mentioned in the description.
            
            anneal_routine():
                A routine to perform the annealing process.
                Determines how to call the annealing function based on one call to the anneal_to_pack
                method using perturb_freq_per_iter, estimating the runtime and deciding the number of iterations
                depending on the time available for packing optimization.
                
    '''
    
    def __init__(self, gate_data , initial_temp, min_temp):
        self.gate_data = gate_data
        self.final_packed_data = gate_data
        self.temp = initial_temp
        self.initial_temp = initial_temp
        self.min_temp = min_temp
           
    # =============================== Acceptance and Reset Temp Functionality ======    ============================ #
    
    def reset_temp(self):
        self.temp = self.initial_temp
    
    def acceptance_probability(self, old_cost, new_cost):
        if new_cost < old_cost:
            return True
        else:
            cost_pr = pow(10,(old_cost - new_cost) / (self.temp))
            return random() < cost_pr
    
    # ============================ Methods for updating/Calculating wire Costs ================================= #
    
    def update_wire_cost(self,l):
        pass
    
    @ time_it
    def wire_cost_function(self):
        pass

    
    @ time_it
    def cost_delta_function(self,g1,g2):
        pass    
    
    # ================================= Methods for Perturbing the Packing ===================================== #   
        
    @ time_it
    def perturb_packing_swap(self):
        # Randomly select a gate and swap / Move within the bounding box it to a new position
        # Calculate the new wire length (Recalculate only for the moved part) and decide whether to accept the move
        # If the move is accepted, update the wire length and repeat
        # If the move is rejected, repeat the process
        random.seed(random_seed_128())
        g1,g2 = random.randint(1,len(self.gate_data.gates)),random.randint(1,len(self.gate_data.gates))
        
        while(g1==g2):
            g1,g2 = random.randint(1,len(self.gate_data.gates)),random.randint(1,len(self.gate_data.gates))
        
        g1_ref,g2_ref = self.gate_data.gates[g1],self.gate_data.gates[g2]
        
        g1_old_env_x,g1_old_env_y,g1_old_x,g1_old_y =  g1_ref.envelope_x, g1_ref.envelope_y , g1_ref.x, g1_ref.y
        g2_old_env_x,g2_old_env_y,g2_old_x,g2_old_y =  g2_ref.envelope_x, g2_ref.envelope_y , g2_ref.x, g2_ref.y
        # print(f"Old Config : g1 = {g1} , g2 = {g2} , g1_old_x = {g1_old_x} , g1_old_y = {g1_old_y} , g2_old_x = {g2_old_x} , g2_old_y = {g2_old_y}") 
        # old_coord = (g1_old_x,g1_old_y,g2_old_x,g2_old_y)
        
        g1_ref.set_coord_env(g2_old_env_x,g2_old_env_y)
        g1_ref.set_coord_rel_env(g1_old_x-g1_old_env_x,g1_old_y-g1_old_env_y) 
        g2_ref.set_coord_env(g1_old_env_x,g1_old_env_y)
        g2_ref.set_coord_rel_env(g2_old_x-g2_old_env_x,g2_old_y-g2_old_env_y)
        
        # print(f"New Config : g1 = {g1} , g2 = {g2} , g1_new_x = {g1_ref.x} , g1_new_y = {g1_ref.y} , g2_new_x = {g2_ref.x} , g2_new_y = {g2_ref.y}")
        pass
    
    @ time_it
    def perturb_packing_move(self):
        
        random.seed(random_seed_128())
        g = random.randint(1,len(self.gate_data.gates))
        random.seed(random_seed_128())  
        
        gate_ref = self.gate_data.gates[g]
        gate_old_x,gate_old_y,gate_old_delta_x,gate_old_delta_y =  gate_ref.x, gate_ref.y, gate_ref.x-gate_ref.envelope_x,  gate_ref.y-gate_ref.envelope_y
        gdx_max = gate_ref.envelope_width - gate_ref.width
        gdy_max = gate_ref.envelope_height - gate_ref.height
        
        possible_pos = [(0,0),(gdx_max//2,0),(gdx_max,0),
                        (0,gdy_max//2),(gdx_max,gdy_max//2),
                        (0,gdy_max),(gdx_max//2,gdy_max),(gdx_max,gdy_max)
                        ]
                        
        choice_delta = random.choice(possible_pos)
        
        gate_ref.set_coord_rel_env(random.randint(0,gdx_max),random.randint(0,gdy_max)) 
        # gate_ref.set_coord_rel_env(choice_delta[0],choice_delta[1])
        
        old_coord = (gate_old_x,gate_old_y)
        
        pass
    
        
    # ================================= Methods for Annealing the Packing ====================================== #
    
    @ time_it
    def anneal_to_pack(self,perturb_freq_per_iter = 1,call_init_pack = True, return_data = False, do_move = True):   
        if(return_data):
            iter_data = []
        
        if(call_init_pack):
            self.gen_init_packing(supress_time_out=True)
            # print(f"Total Initial Wire Cost: {self.wire_cost}")
            if(return_data):
                iter_data.append((0,self.wire_cost))
        
        it_er = 0
        while self. temp > self.min_temp and it_er < IT_BOUND:
            for _ in range(perturb_freq_per_iter):
                self.perturb_packing_swap_v2(supress_time_out=True)
                if(do_move):
                    self.perturb_packing_move_v2(supress_time_out=True)
                    pass
            self.temp *= cooling_rate(self.temp)
            it_er += 1
            if(return_data):
                iter_data.append((it_er,self.wire_cost))
            
            if(self.wire_cost == 0):                # If the wire cost is 0, then we have definitely reached the optimal solution
                break
        # wc,rt = self.wire_cost_function(supress_time_out=True)
        # self.update_wire_cost(wc)
        
        if(return_data):
            return iter_data
        # print(f"New_Cost = {self.wire_cost}")
        # self.update_wire_cost(self.wire_cost_function())
        # print(f"New_Cost_2 = {self.wire_cost}")
      
    @ time_it
    def anneal_routine(self,supress_out):
        '''
        Determines the entire flow of how to perform the Annealing Function for the best results
        '''
        
        gate_freq,pin_freq,wire_freq = len(self.gate_data.gates),self.gate_data.total_pins_added,self.gate_data.total_wires_added
        print(f"\nGate Frequency : {gate_freq} || Pin Frequency : {pin_freq} || Wire Frequency : {wire_freq} || Pin Components : {len(self.gate_data.connected_components)}")
        est_runtime = 0
        res_timeit_no_out,t_func_call = self.gen_init_packing(supress_time_out=True)
        est_runtime += t_func_call
        print(f"Wire Length of Initial Packing (Our Heuristic): {self.initial_wire_cost}")
        ac_wc,rut = self.wire_cost_function_piazza(supress_time_out=True)
        est_runtime += rut
        print(f"Wire Length of Initial Packing (Piazza Heuristic): {ac_wc}")
        print(f"Calling one Annealing Iteration with perturb_freq_per_iter = {1}")
        do_we_move = True if(pin_freq < 20_000) else False
        res_timeit_no_out,time_of_one_call = self.anneal_to_pack(1,False,do_we_move,supress_time_out = True)
        
        # wc,tr = self.wire_cost_function_piazza(supress_time_out=False)
        # self.update_wire_cost(wc)
        est_runtime += time_of_one_call
        self.final_packed_data,var_useless = pseudo_copy_gate_data(self.gate_data,supress_time_out=True)
        self.reset_temp()
        
        print(f"Wire Length after First Trial Packing: {self.wire_cost}")
        print(f"Time of One Call : {time_of_one_call :.6f} seconds, Determining optimal parameters for future calls")
        old_wire_cost = self.final_packed_data[2]
        
        perturb_freq = select_perturb_freq(time_of_one_call)
        call_count,max_no_change = 1,0
        print(f"Calling Annealing with perturb_freq_per_iter = {perturb_freq}")
        while(est_runtime <= TIME_BOUND_TOTAL_SEC-TIME_BOUND_BUFFER_SEC):
            res_timeit_no_out,time_of_one_call = self.anneal_to_pack(perturb_freq,False,do_we_move,supress_time_out = True)
            call_count += 1
            print(f"Best Wire length (Our Heuristic): {old_wire_cost} || Wire Length after Current Iteration (Our Heuristic): {self.wire_cost}")
            self.reset_temp()
            est_runtime += time_of_one_call
            if(old_wire_cost > self.wire_cost):
                # print("Old Wire Cost is more than current wire cost, updating wire costs !!")
                # wc,tr = self.wire_cost_function_piazza(supress_time_out=False)
                # self.update_wire_cost(wc)
                self.final_packed_data,var_t = pseudo_copy_gate_data(self.gate_data,supress_time_out=True)
                old_wire_cost = self.final_packed_data[2]
                est_runtime += time_of_one_call + var_t
                max_no_change = 0
            else:
                if(max_no_change > BREAK_FLAG_COUNT):
                    break
                else:
                    max_no_change += 1
                    
        # Updating Global Data to reflect the best packing
        self.gate_data.set_bbox(self.final_packed_data[0],self.final_packed_data[1])
        for gate_data_up in self.final_packed_data[3]:
            self.gate_data.gates[gate_data_up[0]].set_coord_env(gate_data_up[1],gate_data_up[2])
            self.gate_data.gates[gate_data_up[0]].set_coord_rel_env(gate_data_up[3],gate_data_up[4]) 
        
        v,rt = self.wire_cost_function_piazza(supress_time_out = True)
        self.update_wire_cost(v)
        # Calculating Wire Cost in their manner
        print(f"Exiting Routine, Total Calls made to Annealing = {call_count}")
        
        # return self.final_packed_data
    
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
