from Rect import *
from code_timer import *
from itertools import count 

 
def All_Rec_Packed(rec_data):
    for rec in rec_data:
        if(not rec.is_packed):
            return False
    return True

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
    cells_packed,max_rows_used,max_cols_used = 0,1,1
    Im_Data = [[0]*Im_Width for r in range(Im_Height)]
    # print(Im_Data)
    
    for i in range(len(rec_data)):
        # print(rec_data[i].index,rec_data[i].width,rec_data[i].height)
        rec_done = False
        for y in range(Im_Height):
            if(y+rec_data[i].height > Im_Height or rec_done):
                break
            else:
                for x in range(Im_Width):
                    if(x+rec_data[i].width > Im_Width):
                        break
                    if(Im_Data[y][x] == 0 and Im_Data[y+rec_data[i].height-1][x+rec_data[i].width-1] == 0):
                        # print("Might be possible at x,y",y,x)
                        isvalid = True
                        for r in range(y,y+rec_data[i].height):
                            if(isvalid):
                                for c in range(x,x+rec_data[i].width):
                                    if(Im_Data[r][c] == 1):
                                        isvalid = False
                                        break
                            else:
                                break
                        if(isvalid):
                            for r in range(y,y+rec_data[i].height):
                                for c in range(x,x+rec_data[i].width):
                                    cells_packed += 1
                                    Im_Data[r][c] = 1
                            max_rows_used,max_cols_used = max(max_rows_used,y+rec_data[i].height),max(max_cols_used,x+rec_data[i].width)
                            rec_data[i].packed()
                            rec_data[i].set_pos(x,y)
                            rec_done = True
                            break
        if(not rec_done):
            return -1,None,None                    
        # for r in Im_Data:
        #     print(r)
        # print()
    
    return rec_data,[cells_packed,max_rows_used,max_cols_used],True

    # if(All_Rec_Packed(rec_data)):    
    #     return rec_data,[cells_packed,max_rows_used,max_cols_used],True
    # else:
    #     return -1,None,None


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
    
    TODO - Figure out a way to capitalise on smaller runtimes buy smartly generating initial guesses 
           and working the way around from there to achieve max efficiency

    Args:
        rec_data (List of Rec objects): The Gates as Rec Objects in a list 
        Im_Width (_type_): Image Width in which we try to fit the gates
        Im_Height (_type_): Image Height in which we try to fit the gates
    """
    
    
    cells_packed,max_rows_used,max_cols_used = 0,1,1
    Im_Data = [[0]*Im_Width for r in range(Im_Height)]
    # Im_Data_R_index = [[0]*Im_Width for r in range(Im_Height)]
    Im_Rec_Data = {rec_data[i].index : rec_data[i] for i in range(len(rec_data))}
    # print(Im_Data)
    
    for i in range(len(rec_data)):
        rec_done = False
        x,y = 0,0
        for _infit in count(0,1):
            if (y + rec_data[i].height > Im_Height or rec_done):
                break
            else:
                if(x + rec_data[i].width > Im_Width):
                    x,y = 0,y+1
                    continue
                else:
                    if(Im_Data[y][x] == 0):
                        if(Im_Data[y+rec_data[i].height-1][x+rec_data[i].width-1] == 0):
                            isvalid = True
                            for r in range(y,y+rec_data[i].height):
                                if(isvalid):
                                    for c in range(x,x+rec_data[i].width):
                                        if(Im_Data[r][c] != 0):
                                            isvalid = False
                                            row_notvalid,col_notvalid = r,c
                                            break
                                            
                                else:
                                    break
                                
                            if(isvalid):
                                rec_data[i].packed()
                                rec_data[i].set_pos(x,y)
                                max_rows_used,max_cols_used = max(max_rows_used,y+rec_data[i].height),max(max_cols_used,x+rec_data[i].width)
                                rec_done = True
                                for r in range(y,y+rec_data[i].height):
                                    for c in range(x,x+rec_data[i].width):
                                        cells_packed += 1
                                        Im_Data[r][c] = rec_data[i].index
                                break
                            else:
                                # print(f"Index checking : {Im_Data[r][c]} at {r}, {c}")
                                w_enc,x_enc = Im_Rec_Data[Im_Data[row_notvalid][col_notvalid]].width, Im_Rec_Data[Im_Data[row_notvalid][col_notvalid]].x
                                x = x_enc + w_enc 
                                continue        
                        else:
                            x = x + rec_data[i].width
                            continue
                    else:
                        w_enc,x_enc = Im_Rec_Data[Im_Data[y][x]].width, Im_Rec_Data[Im_Data[y][x]].x 
                        x = x_enc + w_enc
                        continue
                    
        if(not rec_done):
            return -1,None,None                    
        # for r in Im_Data:
        #     print(r)
        # print()
    
    return rec_data,[cells_packed,max_rows_used,max_cols_used],True
    # if(All_Rec_Packed(rec_data)):    
    #     return rec_data,[cells_packed,max_rows_used,max_cols_used],True
    # else:
    #     return -1,None,None    
