cmd_command_0 = r"cd C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\SW_Assignment_1_Files\Sample_Test_Cases"
cmd_command_1 = r"python visualize_gates.py output.txt input.txt 450 500"
import numpy as np

import random as r 
for j in range(2,6):
    with open(f"tc{j}_100.txt","w") as file:
        for i in range(1,101):
            file.write(f"g{i} {r.randint(1,100)} {r.randint(1,100)} \n")



print("Done")