class Dimension():
    def __init__(self,size,index) -> None:
        self.size = size
        self.index  = index

class DynamicGrid():
    
    def Data_loc(row_index,col_index):
        return self.gridsize
    
    def __init__(self,width,height):
        self.rows = [Dimension(width,0)]
        self.columns = [Dimension(height,0)]
        self.data = [[0]*self.gridsize for i in range(self.gridsize)]
        
        
    def get_value(self,x,y):
        row_index = self.rows[y].index
        col_index = self.columns[x].index 
        return self.data[self.gridsize*row_index + col_index]
    
    def set_value(self,x,y,value):
        row_index = self.rows[y].index
        col_index = self.columns[x].index 
        self.data[self.gridsize*row_index + col_index] = value
        
    
        
        
             
        