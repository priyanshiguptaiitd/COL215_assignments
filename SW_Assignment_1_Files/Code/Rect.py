from typing import Any


class Rect():
    def __init__(self,index,width,height):
        self.index = index
        self.width = width
        self.height = height
        self.is_packed = False
        self.x,self.y = None,None
    
    def set_pos(self,x,y):
        self.x = x
        self.y = y
        
    def packed(self):
        self.is_packed = True
        