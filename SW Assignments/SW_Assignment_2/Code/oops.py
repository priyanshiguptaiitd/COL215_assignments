from utils import *
from math import ceil,sqrt,pow
import random
# ========================== Implement the Class Structures used to Store Data ========================== #

class Gate_Data():
    ''' Basic Description -
    
        Class to store the data of the gates and wires for a given input netlist.
        One of the important backbones our entire implementation, derives the obejcts stored from Gate_Env and Pin classes.
    '''
    ''' Attributes:
    
            gates (dict): A dictionary where the key is the gate index and the value is an instance of the Gate_Env object.
            wires (dict): A dictionary where the key is a tuple (Gate_Index, Pin_Index) and the value is a list of tuples (Gate_Index, Pin_Index) representing connected pins.
                          Note that connections are stored twice because of implementation reasons and the actual answer of wire lenght
                          is half of the calculated wire length (Updated by correction_wire_length() method).
            
            bbox (tuple): A tuple representing the bounding box dimensions (width, height).
            
            max_width (int): The maximum width of any gate, used for generating enevelopes of gates
            max_height (int): The maximum height of any gate, used for generating enevelopes of gates
            
            wire_length (int): The total wire length of the current packing, updated by Simulate_Anneal class whenever packing is changed
    '''
    ''' Methods:
            add_gate(gate_index, width, height):
                Adds a gate to the gates dictionary and updates the maximum width and height.

            get_gate(gate_index):
                Returns the Gate_Env object for the given gate index.
            
            add_pin(gate_index, pin_index, pin_x, pin_y):
                Adds a pin to the specified gate.
            
            get_pin(gate_index, pin_index):
                Returns the Pin object for the given gate and pin index.
            
            add_wire(g_i, p_i, g_j, p_j):
                Adds a wire connection between two pins, updating the connected pins for both pins 
                and the wires dictionary ( Connections are considered both way !!).
            
            set_bbox(x, y):
                Sets the bounding box dimensions.
            
            get_bbox():
                Returns the bounding box dimensions.
            
            set_gate_env():
                Sets the envelope dimensions for all gates.
            
            correction_wire_length():
                Corrects the wire length by dividing it by 2.
            
            __str__ :
            
                Calls __str__ on the gate instances stored and handles appropriate formatting.
    '''    
    
    def __init__(self):
        self.gates = dict() # Gate_Index : Instance of Gate_Env Object
        self.wires = dict()  # (Gate_Index,Pin_Index) : Instance of Pin Object
        
        self.bbox = (None,None)
        self.max_width,self.max_height = 0,0
        self.wire_length = None

    def add_gate(self,gate_index,width,height):
        self.gates[gate_index] = Gate_Env(gate_index,width,height)
        self.max_width = self.max_width if(self.max_width > width) else width
        self.max_height = self.max_height if(self.max_height > height) else height
        
    def get_gate(self,gate_index):
        return self.gates[gate_index]
    
    def add_pin(self,gate_index,pin_index,pin_x,pin_y):
        self.gates[gate_index].add_pin(pin_index,pin_x,pin_y)
        
    def get_pin(self,gate_index,pin_index):
        return self.gates[gate_index].pins[pin_index]
    
    def add_wire(self,g_i,p_i,g_j,p_j):
        p_i_ref,p_j_ref = self.gates[g_i].pins[p_i],self.gates[g_j].pins[p_j]
        p_i_ref.connected_to(g_j,p_j)
        p_j_ref.connected_to(g_i,p_i)
        if((g_i,p_i) not in self.wires):
            self.wires[(g_i,p_i)] = [(g_j,p_j)]
        else:
            self.wires[(g_i,p_i)].append((g_j,p_j))
        
        if((g_j,p_j) not in self.wires):
            self.wires[(g_j,p_j)] = [(g_i,p_i)]
        else:
            self.wires[(g_j,p_j)].append((g_i,p_i))
        # print(self.wires)
        
    def set_bbox(self,x,y):
        self.bbox = (x,y)
    
    def get_bbox(self):
        return self.bbox[0],self.bbox[1]
    
    def set_gate_env(self):
        for i in self.gates:
            self.gates[i].set_env(self.max_width,self.max_height)
    
    def correction_wire_length(self):
        self.wire_length = self.wire_length//2
    
    def __str__(self):
        base_s = f"Gate Data || No of Gates = {len(self.gates)} || Bounding Box = ({self.bbox[0]},{self.bbox[1]})\n"
        gates_s = []
        for i in self.gates:
            gates_s.append(str(self.gates[i]))
        return base_s + "\n".join(gates_s)
        
class Gate_Env():
    ''' Basic Description - 
        
        Class to represent the environment of a gate, including the dimensions of it's envelope, 
        relative positioning of gate, pins, and the pin objects themselves. Also stores relevant information
        about the gate's dimensions and index.
        
    '''
    ''' Attributes:
    
            width (int): The width of the gate.
            height (int): The height of the gate.
            gate_index (int): The index of the gate.
            pins (dict): A dictionary where the key is the pin index and the value is an instance of the Pin object
            envelope_width (int): The width of the envelope containing the gate.
            envelope_height (int): The height of the envelope containing the gate.
            envelope_x (int): The x-coordinate of the envelope.
            envelope_y (int): The y-coordinate of the envelope.
            x_relative_env (int): The x-coordinate of the gate relative to the envelope.
            y_relative_env (int): The y-coordinate of the gate relative to the envelope.
            x (int): The global x-coordinate of the gate.
            y (int): The global y-coordinate of the gate.
    
    '''
    ''' Methods:
            set_env(env_w, env_h):
                Sets the envelope dimensions for the gate.
            
            set_coord_env(env_x, env_y):
                Sets the global coordinates of the envelope.
            
            set_coord_rel_env(Delta_x, Delta_y):
                Sets the coordinates of the gate relative to the envelope and the global coordinates of the gate after calculations.
                The default choice implemented throughout is to place the gate in the middle of the envelope as much as possible
            
            add_pin(pin_index, pin_x, pin_y):
                Adds a pin to the gate, storing the pin object in the pins dictionary with the pin index as the key.
            
            get_global_coord():
                Returns the global coordinates of the gate
            
            get_global_coord_pin(pin_index):
                Returns the global coordinates of the specified pin
                
            __str__:
                Calls handles appropriate formatting for the gate and pin objects stored and returns a string object containing the information.
    '''
    
    def __init__(self,gate_index,width,height) -> None:
        self.width = width
        self.height = height
        self.gate_index = gate_index
        self.pins = dict()
        
        self.envelope_width = None
        self.envelope_height = None
        self.envelope_x = None
        self.envelope_y = None
        
        self.x_relative_env = None
        self.y_relative_env = None        
        self.x = None
        self.y = None
        
    def set_env(self,env_w,env_h):
        self.envelope_width,self.envelope_height = env_w,env_h
            
    def set_coord_env(self,env_x,env_y):
        self.envelope_x,self.envelope_y = env_x,env_y 
        
    def set_coord_rel_env(self,Delta_x,Delta_y):
        assert 0 <= Delta_x <= self.envelope_width-self.width, f"Gate goes out of Envelope (X Direction) : {Delta_x} , {self.envelope_width} , {self.width}"
        assert 0 <= Delta_y <= self.envelope_height-self.height, f"Gate goes out of Envelope (Y Direction) : : {Delta_y} , {self.envelope_height} , {self.height}"

        self.x_relative_env,self.y_relative_env = Delta_x,Delta_y
        self.x = self.envelope_x + Delta_x
        self.y = self.envelope_y + Delta_y
        
    def add_pin(self,pin_index,pin_x,pin_y):
        self.pins[pin_index] = Pin(self.gate_index,pin_index,pin_x,pin_y)
        pass
    
    def get_global_coord(self):
        return self.x,self.y
    
    def get_global_coord_pin(self,pin_index):
        pin_ref = self.pins[pin_index]
        pin_rel_x,pin_rel_y = pin_ref.pin_x,pin_ref.pin_y
        return self.x + pin_rel_x, self.y + self.height-pin_rel_y
    
    def get_gate_tup(self):
        return self.gate_index,self.x,self.y
    
    def __str__(self):
        base_s = f"Gate No = {self.gate_index} || Gate_x = {self.x} || Gate_y = {self.y}"
        pins_s = []
        for i in range(1,len(self.pins)+1):
            p_xg,p_yg = self.get_global_coord_pin(i)
            pins_s.append(f"Pin {i} || Parent Gate = {self.gate_index} || Pin_X_Global = {p_xg} || Pin_Y_Global = {p_yg}")
        
        if(len(pins_s)==0):
            return base_s+'\n'+"No Pins on this gate"
        
        return base_s+"\n"+"\n".join(pins_s)

class Pin():
    ''' Basic Description -
        
        Class to represent a pin on a gate, including its relative position to the gate and 
        connections to other pins on different gates.

    '''
    ''' Attributes:
            parent_gate_index (int): The index of the gate to which this pin belongs.
            pin_index (int): The index of the pin.
            pin_x (int): The x-coordinate of the pin relative to the gate.
            pin_y (int): The y-coordinate of the pin relative to the gate.
            connected_pins (dict): A dictionary where the key is the gate index and the value is a list of pin indices that this pin is connected to (of the givven gate ).
    '''
    ''' Methods:
            connected_to(gate_ind, pin_ind):
                Adds a connection from this pin to another pin on a specified gate.
            
            __str__():
                Returns a string representation of the pin, including its relative position and connections.
    '''
    
    def __init__(self,gate_index,pin_index,pin_x,pin_y):
        self.parent_gate_index = gate_index
        self.pin_index = pin_index
        self.pin_x, self.pin_y = pin_x, pin_y
        self.connected_pins = dict()
    
    def connected_to(self,gate_ind,pin_ind):
        '''
        Adds a connection from this pin to another pin on a specified gate.

        Parameters:
            gate_ind (int): The index of the gate to which the other pin belongs.
            pin_ind (int): The index of the other pin.
        '''
        # print(f"Connecting to : g{self.parent_gate_index} , p{self.pin_index} :: g{gate_ind} , p{pin_ind}")
        if gate_ind not in self.connected_pins:
            self.connected_pins[gate_ind] = [pin_ind]
        else:
            self.connected_pins[gate_ind].append(pin_ind)
    
    def __str__(self):
        '''
        Returns a string representation of the pin, including its position and connections.

        Returns:
            str: A string representation of the pin.
        '''
        base_s = f"Pin No = {self.pin_index} || Parent Gate = g{self.parent_gate_index} || Pin_x = {self.pin_x} || Pin_y = {self.pin_y}"
        further_s = []
        for i in self.connected_pins:
            for j in self.connected_pins[i]:
                further_s.append(f"Connected to : g{i} , p{j}")
        return base_s + "\n" + "\n".join(further_s)

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
        self.temp = initial_temp
        self.initial_temp = initial_temp
        self.min_temp = min_temp
        self.wire_cost = None
        self.initial_wire_cost = None
    
    def reset_temp(self,temp):
        self.temp = temp
    
    def acceptance_probability(self, old_cost, new_cost):
        if new_cost < old_cost:
            return True
        else:
            cost_pr = pow(10,(old_cost - new_cost) / self.temp)
            return random.random() < cost_pr
    
    def update_wire_cost(self,l):
        self.wire_cost = l
        self.gate_data.wire_length = l
        return l
    
    def wire_cost_function(self):
        total_wire_length = 0
        for (g_i, p_i),gp in self.gate_data.wires.items():
            for g_j,p_j in gp:
                x_i, y_i = self.gate_data.get_gate(g_i).get_global_coord_pin(p_i)
                x_j, y_j = self.gate_data.get_gate(g_j).get_global_coord_pin(p_j)
                total_wire_length += abs(x_i - x_j) + abs(y_i - y_j)
        return total_wire_length
    
    def cost_delta_function(self, g1, g2, old_coord):
        if(g2 is not None):
            gate_1, gate_2, cost_delta = self.gate_data.gates[g1], self.gate_data.gates[g2], 0
            g1_old_x, g1_old_y, g2_old_x, g2_old_y = old_coord
            pin_data_gate1, pin_data_gate2 = gate_1.pins, gate_2.pins
            
            for i in range(1, len(pin_data_gate1) + 1):
                pin_i_gate_1 = pin_data_gate1[i]
                x_i, y_i = gate_1.get_global_coord_pin(i)
                x_i_old, y_i_old = H_global_coord_pin(gate_1, i, (g1_old_x, g1_old_y), gate_1.height)
                pins_connected_to_i_gate_1 = pin_i_gate_1.connected_pins
                for g_i, pins_g_i in pins_connected_to_i_gate_1.items():
                    for p_j in pins_g_i:
                        # print(f"Called  by : g{g1} , p{i} || Connecttion : g{g_i} , p{p_j}")
                        x_j, y_j = self.gate_data.gates[g_i].get_global_coord_pin(p_j)
                        if g_i == g2:
                            x_j_o, y_j_o = H_global_coord_pin(gate_2, p_j, (g2_old_x, g2_old_y), gate_2.height)
                            # print(f"Old Value of connection : {abs(x_i_old - x_j_o) + abs(y_i_old - y_j_o)}")
                            # print(f"{x_i} {x_j} {y_i} {y_j}")
                            # print(f"New Value of connection : {abs(x_i - x_j) + abs(y_i - y_j)}")
                            cost_delta += abs(x_i - x_j) + abs(y_i - y_j)
                            cost_delta -= abs(x_i_old - x_j_o) + abs(y_i_old - y_j_o)
                            # print(f"Cost Delta : {cost_delta}")
                        else:
                            # print(f"Old Value of connection : {abs(x_i_old - x_j) + abs(y_i_old - y_j)}")
                            # print(f"New Value of connection : {abs(x_i - x_j) + abs(y_i - y_j)}")
                            cost_delta += 2 * (abs(x_i - x_j) + abs(y_i - y_j))
                            cost_delta -= 2 * (abs(x_i_old - x_j) + abs(y_i_old - y_j))
                            # print(f"Cost Delta : {cost_delta}")
            
            for i in range(1, len(pin_data_gate2) + 1):
                pin_i_gate_2 = pin_data_gate2[i]
                x_i, y_i = gate_2.get_global_coord_pin(i)
                x_i_old, y_i_old = H_global_coord_pin(gate_2, i, (g2_old_x, g2_old_y), gate_2.height)
                pins_connected_to_i_gate_2 = pin_i_gate_2.connected_pins
                for g_i, pins_g_i in pins_connected_to_i_gate_2.items():
                    for p_j in pins_g_i:
                        # print(f"Called  by : g{g2} , p{i} || Connecttion : g{g_i} , p{p_j}")
                        x_j, y_j = self.gate_data.gates[g_i].get_global_coord_pin(p_j)
                        if g_i == g1:
                            x_j_o, y_j_o = H_global_coord_pin(gate_1, p_j, (g1_old_x, g1_old_y), gate_1.height)
                            # print(f"Old Value of connection : {abs(x_i_old - x_j_o) + abs(y_i_old - y_j_o)}")
                            # print(f"New Value of connection : {abs(x_i - x_j) + abs(y_i - y_j)}")
                            cost_delta += abs(x_i - x_j) + abs(y_i - y_j)
                            cost_delta -= abs(x_i_old - x_j_o) + abs(y_i_old - y_j_o)
                            # print(f"Cost Delta : {cost_delta}")
                        else:
                            # print(f"Old Value of connection : {abs(x_i_old - x_j) + abs(y_i_old - y_j)}")
                            # print(f"New Value of connection : {abs(x_i - x_j) + abs(y_i - y_j)}")
                            cost_delta += 2 * (abs(x_i - x_j) + abs(y_i - y_j))
                            cost_delta -= 2 * (abs(x_i_old - x_j) + abs(y_i_old - y_j))
                            # print(f"Cost Delta : {cost_delta}")

            return cost_delta
        else:
            gate_1, cost_delta = self.gate_data.gates[g1], 0
            g1_old_x, g1_old_y = old_coord
            pin_data_gate1 = gate_1.pins
            
            for i in range(1, len(pin_data_gate1) + 1):
                pin_i_gate_1 = pin_data_gate1[i]
                x_i, y_i = gate_1.get_global_coord_pin(i)
                x_i_old, y_i_old = H_global_coord_pin(gate_1, i, (g1_old_x, g1_old_y), gate_1.height)
                pins_connected_to_i_gate_1 = pin_i_gate_1.connected_pins
                for g_i, pins_g_i in pins_connected_to_i_gate_1.items():
                    for p_j in pins_g_i:
                        x_j, y_j = self.gate_data.gates[g_i].get_global_coord_pin(p_j)
                        # print(f"Old Value of connection : {abs(x_i_old - x_j) + abs(y_i_old - y_j)}")
                        # print(f"New Value of connection : {abs(x_i - x_j) + abs(y_i - y_j)}")
                        cost_delta += 2 * (abs(x_i - x_j) + abs(y_i - y_j))
                        cost_delta -= 2 * (abs(x_i_old - x_j) + abs(y_i_old - y_j))
                        # print(f"Cost Delta : {cost_delta}")
            
            return cost_delta
        
    @ time_it_no_out
    def gen_init_packing(self):
        # Calculate the number of rows and columns in the grid
        gate_freq = len(self.gate_data.gates)
        bb_grid_dim,bb_grid_width,bb_grid_height = ceil(sqrt(gate_freq)), self.gate_data.max_width, self.gate_data.max_height
        # Shuffle the grid positions to ensure a random initial placement
        # Place each gate in a unique grid cell
        
        for i in range(1,len(self.gate_data.gates)+1):
            if(i%bb_grid_dim==0):
                self.gate_data.gates[i].set_coord_env(((i-1)%bb_grid_dim)*bb_grid_width,(i//bb_grid_dim-1)*bb_grid_height)
                self.gate_data.gates[i].set_coord_rel_env((bb_grid_width-self.gate_data.gates[i].width)//2,(bb_grid_height-self.gate_data.gates[i].height)//2)
            else:
                self.gate_data.gates[i].set_coord_env(((i-1)%bb_grid_dim)*bb_grid_width,(i//bb_grid_dim)*bb_grid_height)
                self.gate_data.gates[i].set_coord_rel_env((bb_grid_width-self.gate_data.gates[i].width)//2,(bb_grid_height-self.gate_data.gates[i].height)//2)

        total_wire_length = self.wire_cost_function()
        self.gate_data.bbox = (bb_grid_dim*bb_grid_width,(ceil(len(self.gate_data.gates)/bb_grid_dim))*bb_grid_height)
        self.update_wire_cost(total_wire_length)
        self.initial_wire_cost = total_wire_length    
    
    @ time_it_no_out
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
        old_wire_cost = self.wire_cost
        
        ## Redundant Calculation of Wire Cost
        ## TODO - Improve this part
        new_wire_cost = self.wire_cost_function()

        
        if(self.acceptance_probability(old_wire_cost,new_wire_cost)):
            self.update_wire_cost(new_wire_cost)
            # print(f"Accepting Config : Old Cost {old_wire_cost} ---> New Cost {new_wire_cost}")
            return
        else:
            self.update_wire_cost(old_wire_cost)
            g1_ref.set_coord_env(g1_old_env_x,g1_old_env_y)
            g1_ref.set_coord_rel_env(g1_old_x-g1_old_env_x,g1_old_y-g1_old_env_y) 
            g2_ref.set_coord_env(g2_old_env_x,g2_old_env_y)
            g2_ref.set_coord_rel_env(g2_old_x-g2_old_env_x,g2_old_y-g2_old_env_y)
            return
            # print(f"Rejecting Config")

    @ time_it_no_out
    def perturb_packing_swap_v2(self):
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
        old_coord = (g1_old_x,g1_old_y,g2_old_x,g2_old_y)
        
        g1_ref.set_coord_env(g2_old_env_x,g2_old_env_y)
        g1_ref.set_coord_rel_env(g1_old_x-g1_old_env_x,g1_old_y-g1_old_env_y) 
        g2_ref.set_coord_env(g1_old_env_x,g1_old_env_y)
        g2_ref.set_coord_rel_env(g2_old_x-g2_old_env_x,g2_old_y-g2_old_env_y)
        
        # print(f"New Config : g1 = {g1} , g2 = {g2} , g1_new_x = {g1_ref.x} , g1_new_y = {g1_ref.y} , g2_new_x = {g2_ref.x} , g2_new_y = {g2_ref.y}")
        # print(g1_ref)
        # print(g2_ref)
        old_wire_cost = self.wire_cost
        
        cost_delta = self.cost_delta_function(g1,g2,old_coord)
        new_wire_cost = old_wire_cost + cost_delta
        
        if(self.acceptance_probability(old_wire_cost,new_wire_cost)):
            self.update_wire_cost(new_wire_cost)
            # print(f"Accepting Config : Old Cost {old_wire_cost} ---> New Cost {new_wire_cost}")
            return
        else:
            self.update_wire_cost(old_wire_cost)
            g1_ref.set_coord_env(g1_old_env_x,g1_old_env_y)
            g1_ref.set_coord_rel_env(g1_old_x-g1_old_env_x,g1_old_y-g1_old_env_y) 
            g2_ref.set_coord_env(g2_old_env_x,g2_old_env_y)
            g2_ref.set_coord_rel_env(g2_old_x-g2_old_env_x,g2_old_y-g2_old_env_y)
            return
            # print(f"Rejecting Config")        
    
    @ time_it_no_out
    def perturb_packing_move(self):
        # Randomly select a gate and move it within the bounding box to a new position
        # Calculate the new wire length (Recalculate only for the moved part) and decide whether to accept the move
        # If the move is accepted, update the wire length and repeat
        # If the move is rejected, repeat the processg
        random.seed(random_seed_128())
        
        g = random.randint(1,len(self.gate_data.gates))
        
        random.seed(random_seed_128())  
        
        gate_ref = self.gate_data.gates[g]
        gate_old_x,gate_old_y,gate_old_delta_x,gate_old_delta_y =  gate_ref.x, gate_ref.y, gate_ref.x-gate_ref.envelope_x,  gate_ref.y-gate_ref.envelope_y
        
        gate_ref.set_coord_rel_env(random.randint(0,gate_ref.envelope_width-gate_ref.width),random.randint(0,gate_ref.envelope_height-gate_ref.height)) 
        
        old_coord = (gate_old_x,gate_old_y)
        
        old_wire_cost = self.wire_cost
        
        cost_delta = self.cost_delta_function(g,None,old_coord)
        
        new_wire_cost = old_wire_cost + cost_delta
        
        if(self.acceptance_probability(old_wire_cost,new_wire_cost)):
            self.update_wire_cost(new_wire_cost)
            # print(f"Accepting Config : Old Cost {old_wire_cost} ---> New Cost {new_wire_cost}")
            return
        else:
            self.update_wire_cost(old_wire_cost)
            gate_ref.set_coord_rel_env(gate_old_delta_x,gate_old_delta_y)
            return
            # print(f"Rejecting Config")
        
    @ time_it_no_out
    def anneal_to_pack(self,perturb_freq_per_iter = 1):
        # self.reset_temp(10**perturb_freq_per_iter)
        it_er = 0
        while self.temp > self.min_temp and it_er < IT_BOUND:
            for _ in range(perturb_freq_per_iter):
                self.perturb_packing_swap_v2(supress_time_out=True)
                self.perturb_packing_move(supress_time_out=True)
            self.temp *= cooling_rate(self.temp)
            it_er += 1
            
            if(self.wire_cost == 0):                # If the wire cost is 0, then we have definitely reached the optimal solution
                break
        self.wire_cost_function()
        # print("Exiting Annealing Successfully !!")
    
    def anneal_routine(self):
        pass 