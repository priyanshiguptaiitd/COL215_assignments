
# ========================== Implement the Class Structures used to Store Data ========================== #

class Gate_Data():
    def __init__(self):
        self.gates = dict() # Gate_Index : Instance of Gate_Env Object
        self.wires = dict()  # (Gate_Index,Pin_Index) : Instance of Pin Object
        
        self.bbox = (None,None)

        self.max_width,self.max_height = 0,0
        self.width_sum,self.height_sum = 0,0
        self.total_gate_area = 0
        
        self.wire_length = None

    def add_gate(self,gate_index,width,height):
        self.gates[gate_index] = Gate_Env(gate_index,width,height)
        self.max_height = self.max_height if(self.max_height > height) else height
        self.max_height = self.max_height if(self.max_height > height) else height
        
    def get_gate(self,gate_index):
        return self.gates[gate_index]
    
    def add_pin(self,gate_index,pin_index,pin_x,pin_y):
        self.gates[gate_index].add_pin(pin_index,pin_x,pin_y)
        
    def get_pin(self,gate_index,pin_index):
        return self.gates[gate_index].pins[pin_index]
    
    def add_wire(self,g_i,p_i,g_j,p_j):
        p_i_ref,p_j_ref = self.gates[g_i].pins[p_i],self.gates[g_i].pins[p_i]
        p_i_ref.connected_to(g_j,p_j)
        p_j_ref.connected_to(g_i,p_i)

        self.wires[(g_i,p_i)] = (g_j,p_j)
        
    def set_bbox(self,x,y):
        self.bbox = (x,y)
    
    def get_bbox(self):
        return self.bbox[0],self.bbox[1]
    
    def __str__(self):
        base_s = f"No of Gates = {len(self.gates)} || Bounding Box Dimensions : ({self.bbox[0]},{self.bbox[1]}) \n"
        gate_s = []
        for i in range(1,len(self.gates)+1):
            gate_s.append(str(self.gates[i]))
            
        wire_s = []
        
        for i in self.wires:
            g_i,p_i = i
            g_j,p_j = i[0], i[1]
            wire_s.append(f"Wire || g{g_i},p{p_i} ===== > g{g_j},p{p_j}")            
                    
        if(len(gate_s)>0):
            return base_s + "\n".join(gate_s) + '\n' + "\n".join(wire_s)
        else:
            return base_s + "No gate added Yet !!!"
        
class Gate_Env():
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
        
        self.is_packed = False
        
    def set_env(self,env_w,env_h):
        self.envelope_width,self.envelope_height = env_w,env_h
            
    def set_coord_env(self,env_x,env_y):
        self.envelope_x,self.envelope_y = env_x,env_y 
        
    def set_coord_rel_env(self,Delta_x,Delta_y):
        assert 0 <= Delta_x <= self.envelope_width-self.width, "Gate goes out of Envelope (X Direction)"
        assert 0 <= Delta_y <= self.envelope_height-self.height, "Gate goes out of Envelope (X Direction)"

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
            pins_s.append(str(self.pins[i]))
        
        if(len(pins_s)==0):
            return base_s+'\n'+"No Pins on this gate"
        
        return base_s+"\n"+"\n".join(pins_s)

class Pin():
    def __init__(self,gate_index,pin_index,pin_x,pin_y):
        self.parent_gate_index = gate_index
        self.pin_index = pin_index
        self.pin_x, self.pin_y = pin_x, pin_y
        self.connected_pins = dict()
    
    def connected_to(self,gate_index,pin_index):
        if gate_index not in self.connected_pins:
            self.connected_pins[gate_index] = [pin_index]
        else:
            self.connected_pins[gate_index].append(pin_index)
    
    def __str__(self):
        base_s = f"Pin No = {self.pin_index} || Parent Gate = g{self.parent_gate_index} || Pin_x = {self.pin_x} || Pin_y = {self.pin_y}"
        
        return base_s

    