from Rect import *
from code_timer import *
from itertools import count 
from copy import deepcopy


@time_it
def Pack_by_Pixel_v0(rec_data,h_max):
    """
    A very Naive algorithm that just fits the rectangles adjacent to one another

    TODO - Find a bettter algorithm (Done in V1)

    Args:
        rec_data (List of Rec objects): The Gates as Rec Objects in a list 
        h_max (Maximum height of Gates): The height of the diagram we will be using
    """
    x,y = 0,0
    cells_packed, max_rows_used, max_cols_used = 0, h_max, 0
    rdata = deepcopy(rec_data)
    
    for i in range(len(rdata)):
        rdata[i].set_pos(x,y)
        rdata[i].packed()
        x += rdata[i].width
        cells_packed += (rdata[i].width)*(rdata[i].height)
    
    max_cols_used = x
    
    return rdata,[cells_packed,max_rows_used,max_cols_used],True
        
@time_it
def Pack_by_Pixel_v1(rec_data,Im_Width,Im_Height):
    """
    Naive algorithm that scans every possible pixel and checks wether
    a given rectangle can fit in the grid
    
    TODO - Determine how to change dimensions effciently to check if possible or not
           (Can be improve if step size of gridscanning is taken as per rectangle dimensions ?) 
           (Done now in V2)

    Args:
        rec_data (List of Rec objects): The Gates as Rec Objects in a list 
        Im_Width (_type_): Image Width in which we try to fit the gates
        Im_Height (_type_): Image Height in which we try to fit the gates
    """
    
    rdata = deepcopy(rec_data)
    cells_packed, max_rows_used, max_cols_used = 0, 0, 0
    Im_Data = [[0]*Im_Width for r in range(Im_Height)]
    
    for i in range(len(rdata)):
        rec_done = False
        for y in range(Im_Height):
            if(y+rdata[i].height > Im_Height or rec_done):
                break
            else:
                for x in range(Im_Width):
                    if(x+rdata[i].width > Im_Width):
                        break
                    if(Im_Data[y][x] == 0 and Im_Data[y+rdata[i].height-1][x+rdata[i].width-1] == 0):
                        isvalid = True
                        for r in range(y,y+rdata[i].height):
                            if(isvalid):
                                for c in range(x,x+rdata[i].width):
                                    if(Im_Data[r][c] == 1):
                                        isvalid = False
                                        break
                            else:
                                break
                        if(isvalid):
                            for r in range(y,y+rdata[i].height):
                                for c in range(x,x+rdata[i].width):
                                    Im_Data[r][c] = 1
                            cells_packed += (rdata[i].height)*(rdata[i].width) 
                            max_rows_used,max_cols_used = max(max_rows_used,y+rdata[i].height),max(max_cols_used,x+rdata[i].width)
                            rdata[i].packed()
                            rdata[i].set_pos(x,y)
                            rec_done = True
                            break
        if(not rec_done):
            return -1,None,None                    
    
    return rdata,[cells_packed,max_rows_used,max_cols_used],True

    
@time_it
def Pack_by_Pixel_v2(rec_data,Im_Width,Im_Height):
    """ Pack_by_Pixel_v2 
    
    Improved Version of v1 - Better grid scanning for potential possible positions of 
                             placing rectangles by taking into account the cells where a rectangle is already placed
                             
                             Visually skips to the right most edge + 1 of the rectangle encompassing the current region
                             In case the current row becomes insufficient then jumps to the next row. Breaks out of loop
                             if the remaining rows are insufficient 
                             
                             Smartly tackles the case of finding a filled cell while scanning subgrid of a potential postion
                             for placing a rectangle 
                             
    IMP - Using a deepcopy of rec_data - Since these functions were written way before we implemented test_code.py 
          To prevent clash with the Original Rec_Data passed in test_code, we mutate a deepcopy of the Rec_Data
    
    TODO - Figure out a way to capitalise on smaller runtimes buy smartly generating initial guesses 
           and working the way around from there to achieve max efficiency

    Args:
        rec_data (List of Rec objects): The Gates as Rec Objects in a list 
        Im_Width (_type_): Image Width in which we try to fit the gates
        Im_Height (_type_): Image Height in which we try to fit the gates
    """
    rdata = deepcopy(rec_data)
    cells_packed,max_rows_used,max_cols_used = 0,0,0
    Im_Data = [[0]*Im_Width for r in range(Im_Height)]
    Im_Rec_Data = {rdata[i].index : rdata[i] for i in range(len(rdata))}
        
    for i in range(len(rdata)):
        rec_done = False
        x,y = 0,0
        for _inf_it in count(0,1):
            if (y + rdata[i].height > Im_Height or rec_done):
                break
            else:
                if(x + rdata[i].width > Im_Width):
                    x,y = 0,y+1
                    continue
                else:
                    if(Im_Data[y][x] == 0):
                        if(Im_Data[y+rdata[i].height-1][x+rdata[i].width-1] == 0):
                            isvalid = True
                            for r in range(y,y+rdata[i].height):
                                if(isvalid):
                                    for c in range(x,x+rdata[i].width):
                                        if(Im_Data[r][c] != 0):
                                            isvalid = False
                                            row_notvalid,col_notvalid = r,c
                                            break                                            
                                else:
                                    break
                                
                            if(isvalid):
                                cells_packed += (rdata[i].height)*(rdata[i].width) 
                                rdata[i].packed()
                                rdata[i].set_pos(x,y)
                                max_rows_used = max_rows_used if (max_rows_used >= y+rdata[i].height) else y+rdata[i].height
                                max_cols_used = max_cols_used if(max_cols_used >= x+rdata[i].width) else x+rdata[i].width
                                rec_done = True
                                for r in range(y,y+rdata[i].height):
                                    for c in range(x,x+rdata[i].width):
                                        Im_Data[r][c] = rdata[i].index
                                break
                            else:
                                w_enc,x_enc = Im_Rec_Data[Im_Data[row_notvalid][col_notvalid]].width, Im_Rec_Data[Im_Data[row_notvalid][col_notvalid]].x
                                x = x_enc + w_enc 
                                continue        
                        else:
                            x = x + rdata[i].width
                            continue
                    else:
                        w_enc,x_enc = Im_Rec_Data[Im_Data[y][x]].width, Im_Rec_Data[Im_Data[y][x]].x 
                        x = x_enc + w_enc
                        continue
                    
        if(not rec_done):
            return -1,None,None                    

    return rdata,[cells_packed,max_rows_used,max_cols_used],True
   
