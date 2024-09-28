Test Case Analysis :


Time Complexity Analysis :

1. Initial Packing - Depends linearly on the number of gates
2. Annealing - Depends linealry on the number of pertubrations per iteration
             - If the cooling rate is constant and the intial temperateure is fixed then the number of
               iterations is fixed (By virture of the exponentials and logarithms involved)
             - In a given perturbation procedure most of the operations are constant time
             - Only recalculation of cost_delta takes time
             - recalculation will take time of order of O(w_i + w_j) where w_i and w_j are the number of wires
               connected to the gates i and j, which in worse case can be O(W) where n is the number of wires
               in the circuit 

               (Imagine two gates and all the connections from g1--->g2 and g2--->g1)

             - In practice and practically predicting time Complexity is a complex task since the test case generationa
               as well as the perturbation process are pseudo-random and can only be done by running multiple test cases
               and observing the time taken 



Generate a lot of edge cases :

1. Manually Generate a test case with gates where pins can be placed on top
    of each other to give 0 output -- argue why our algorithm does based

2. Manually Generate a test case where most of the wires emanate from a single gate and 
    other gates have only one wire going into them 

3. Manually Generate a test case where the number where the connections are circular / cyclic
    and check the performance of our algorithm



Paramters to Vary :

1. Number of Gates , Number of Pins and ---Number of Wires---
2. For a given large test cases , we can vary the number of pertubrations per iteration of annealing
   and show the tradeoff of time vs reduced wirelength