from gates_pins import *
from IO_Parser import *

FP_SINGLE_IN = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Code\input.txt"
FP_SINGLE_OUT = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\COL215_assignments\SW Assignments\SW_Assignment_2\Code\output.txt"


gd = parse_Input_Gates(FP_SINGLE_IN)

parse_Output_Gates(gd,FP_SINGLE_OUT)
print(gd)