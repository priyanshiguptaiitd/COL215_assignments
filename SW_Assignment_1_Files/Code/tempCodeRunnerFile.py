rdv,pack_data,check_pack = Pack_by_Pixel(rec_data,95,135)
    # if(check_pack is not None):
    #     print(parse_Rec_Data_Ouput(rdv),f"\n Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}\n , {pack_data[1]} rows and {pack_data[2]} cols were used")
    #     print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
    #     parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Ouput(rdv))