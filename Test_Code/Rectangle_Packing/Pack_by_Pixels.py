from Rect import *
from time import time

def time_it(func): 
    # This function shows the execution time of  
    # the function object passed 
    def wrap_func(*args, **kwargs): 
        t_start = time() 
        result = func(*args, **kwargs) 
        t_end = time() 
        print(f'Function {func.__name__!r} executed in {(t_end-t_start):.4f}s') 
        return result 
    return wrap_func 

def All_Rec_Packed(rec_data):
    for rec in rec_data:
        if(not rec.is_packed):
            return False
    return True

@time_it
def Pack_by_Pixel(rec_data,Im_Width,Im_Height):
    """
    Naive algorithm that scans every possible pixel and checks wether
    a given rectangle can fit in the grid
    
    TODO - Determine how to change dimensions effciently to check if possible or not
    
    Can be improve if step size of gridscanning is taken as per rectangle dimensions

    Args:
        rec_data (List of Rec objects): The Gates as Rec Objects in a list 
        Im_Width (_type_): _
        Im_Height (_type_): _description_
    """
    cells_packed = 0
    Im_Data = [[0]*Im_Width for r in range(Im_Height)]
    print(Im_Data)
    
    for i in range(len(rec_data)):
        print(rec_data[i].index,rec_data[i].width,rec_data[i].height)
        rec_done = False
        for y in range(Im_Height):
            if(y+rec_data[i].height > Im_Height or rec_done):
                break
            else:
                for x in range(Im_Width):
                    if(x+rec_data[i].width > Im_Width):
                        break
                    if(Im_Data[y][x] == 0 and Im_Data[y+rec_data[i].height-1][x+rec_data[i].width-1] == 0):
                        print("Might be possible at x,y",y,x)
                        isvalid = True
                        for r in range(y,y+rec_data[i].height):
                            for c in range(x,x+rec_data[i].width):
                                if(Im_Data[r][c] == 1):
                                    isvalid = False
                                    break
                        if(isvalid):
                            for r in range(y,y+rec_data[i].height):
                                for c in range(x,x+rec_data[i].width):
                                    cells_packed += 1
                                    Im_Data[r][c] = 1
                            rec_data[i].packed()
                            rec_data[i].set_pos(x,y)
                            rec_done = True
                            break
                        
        for r in Im_Data:
            print(r)
        print()
    
    if(All_Rec_Packed(rec_data)):    
        return rec_data,cells_packed,True
    else:
        return -1,None,None