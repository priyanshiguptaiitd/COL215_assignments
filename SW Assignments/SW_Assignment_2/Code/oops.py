
# ========================== Implement the Class Structures used to Store Data ========================== #


class Gate_Data():
    def __init__(self):
        self.gates = dict() # Gate_Index : Instance of Gate_Env Object
        self.pins = dict()  # (Gate_Index,Pin_Index) : Instance of Pin Object
        
        self.bbox = None

        self.max_width,self.max_height = 0,0
        self.width_sum,self.height_sum = 0,0
        self.total_gate_area = 0


    def add_gate(self,gate_index,width,height):
        self.gates[gate_index] = Gate_Env(gate_index,width,height)
        self.max_height = self.max_height if(self.max_height > height) else height
        self.max_height = self.max_height if(self.max_height > height) else height
    
    
    def get_gate(self,gate_index,width,height):
        return self.gates.get(gate_index)
    
    def add_pin(self,gate_index,pin_index,pin_x,pin_y):
        self.pins[pin_index]

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
    
    def __str__(self):
        base_s = f"Gate No = {self.gate_index} || Gate_x = {self.x} || Gate_y = {self.y}"
        return base_s

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
        base_s = f"Pin No = {self.gate_index} || Parent Gate = g{self.parent_gate_index}"
        return base_s

    