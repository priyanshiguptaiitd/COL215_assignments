from Rect import *
from Pack_by_Pixels import *
  
def parse_Input_Rectangles(fpath):
    
    rec_data,rec_total_area= list(),0
    max_width,max_height,width_sum,height_sum = 0,0,0,0 
    
    with open(fpath,'r') as file:
        c = 1
        for l in file.readlines():
            rdata = l.split()
            rec_data.append(Rect(c,int(rdata[1]),int(rdata[2])))
            c += 1
            height_sum+= int(rdata[2])
            width_sum += int(rdata[1])
            rec_total_area += int(rdata[1])*int(rdata[2])
            max_width,max_height = max(max_width,int(rdata[1])),max(max_height,int(rdata[1])) 
    
    rec_data.sort(reverse=True,key= lambda t: (t.height,t.width))
    
    return rec_data,rec_total_area,max_width,max_height,width_sum,height_sum

def parse_Rec_Data_Readable(rec_data):
    rec_data_readable = [(rec.index,rec.width,rec.height) for rec in rec_data]
    return rec_data_readable

def parse_Rec_Data_Ouput(rec_data):
    rec_data_output = [(rec.index,rec.x,rec.y) for rec in rec_data]
    return rec_data_output

def parse_Output_Rectangles(optimal_w,optimal_h,rec_data):
    
    with open(r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\output.txt",'w') as file:
        lines_output = list()
        lines_output.append(f"bounding_box {optimal_w} {optimal_h} \n")
        c = 1
        for rdata in rec_data:
            lines_output.append(f"g{rdata[0]} {rdata[1]} {rdata[2]} \n")
        file.writelines(lines_output)
    
    return 1

def Rec_Data_Analysis(rec_data):
    aspect_ratio,w_avg,h_avg,freq = 0,0,0,len(rec_data)
    assert (freq>0), "Don't pass empty Set of Rectangles"
    for rec in rec_data:
        aspect_ratio += rec.width/rec.height
        w_avg += rec.width
        h_avg += rec.height
    return aspect_ratio/freq,w_avg/freq,h_avg/freq          

if(__name__ == "__main__"):
    fp = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\input.txt"
    rec_data,rec_tot_area,mw,mh,ws,hs = parse_Input_Rectangles(fp)
    avg_asp,w_avg,h_avg= Rec_Data_Analysis(rec_data)
    rec_freq = len(rec_data)
    print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} " )
    print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(1.1*(rec_tot_area**0.5))} across {rec_freq} gates")
    rdv,pack_data,check_pack = Pack_by_Pixel_v1(rec_data,1729,1729)
    if(check_pack is not None):
        print(parse_Rec_Data_Ouput(rdv),f"\n Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}\n , {pack_data[1]} rows and {pack_data[2]} cols were used")
        print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
        parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Ouput(rdv))
    
        
