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

def All_Rec_Packed(rec_data):
    for rec in rec_data:
        if(not rec.is_packed):
            return False
    return True

def Rec_Data_Analysis(rec_data):
    aspect_ratio,w_avg,h_avg,freq = 0,0,0,len(rec_data)
    assert (freq>0), "Don't pass empty Set of Rectangles"
    for rec in rec_data:
        aspect_ratio += rec.width/rec.height
        w_avg += rec.width
        h_avg += rec.height
    return aspect_ratio/freq,w_avg/freq,h_avg/freq 