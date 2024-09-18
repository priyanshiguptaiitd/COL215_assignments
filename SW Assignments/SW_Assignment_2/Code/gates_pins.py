from typing import Any

class Graph():
    def __init__(self):
        self.graph = dict()
    def __str__(self):
        return str(self.graph)

class Gate_Data():
    def __init__(self):
        self.gates = dict()
        self.wires = dict()
    
        self.max_width = 0
        self.max_height = 0
        self.width_sum = 0
        self.height_sum = 0
        self.gate_total_area = 0
        self.bounding_box = (None,None)
        
    def set_gate(self, index, width, height):
        self.gates[index] = Gate(index, width, height)
        self.max_height = self.max_height if self.max_height > height else height   
        self.max_width = self.max_width if self.max_width > width else width
        self.width_sum += width
        self.height_sum += height
        self.gate_total_area += width*height

    def get_gate(self,index):
        return self.gates.get(index,None)

    def set_wire(self, index, g1,p1,g2,p2):
        self.wires[index] = Wire(index,g1,p1,g2,p2)
    
    def get_wire(self,index):
        return self.wires.get(index,None)
    
    def set_bbox(self, width, height):
        self.bounding_box = (width, height)
    
    def get_bbox(self):
        return self.bounding_box[0], self.bounding_box[1]
    
    def get_dim_data(self):
        return self.max_width, self.max_height, self.width_sum, self.height_sum, self.gate_total_area
    
    def get_gate_data(self):
        return [self.gates[i].get_gate_tup() for i in range(1,len(self.gates)+1)]
    
    def __str__(self):
        s1 = "Gates : [Width, Height, X_Gate, Y_Gate, Packing Status] \n"
        for i in range(1,len(self.gates)+1):
            s1 += str(self.gates[i]) + "\n"
        s2 = "Wires : [From (gate_index,gatepin_index), To (gate_index,gatepin_index), Wiring Status]\n"  
        for i in range(1,len(self.wires)+1):
            s2 += str(self.wires[i]) + "\n"
        s3 = f"Bounding Box : " + str(self.bounding_box)+"\n"
        return s1+s2+s3

class Wire():
    def __init__(self,index, g1, p1, g2, p2):
        self.index = index 
        self.g1 = g1
        self.g2 = g2
        self.p1 = p1
        self.p2 = p2
        self.wired = False
        
    def set_wired(self):
        self.wired = True
        
    def __str__(self):
        return f"Wire {self.index} : ({self.g1}, {self.p1}) ---> ({self.g2}, {self.p2}) | {self.wired}"
        
class Gate():
    def __init__(self, index, width, height):
        self.index = index
        self.width = width
        self.height = height
        
        self.pins = dict()
        self.is_packed = False
        self.x,self.y = None,None

    def set_pin(self, index, x, y):
        self.pins[index] = (x, y)
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def packed(self):
        self.is_packed = True

    def get_gate_tup(self):
        return (self.index, self.x, self.y)
    
    def __str__(self):
        return f"Gate {self.index} : {self.width}, {self.height}, {self.x}, {self.y}, {self.is_packed}"




