import random
import math
import itertools

"""
minimizing

Observation:
* each node should generate the same number of neighbors
* be aware of poor performance under spiky neighborhoods
* yields better results than local search and multisstart search after t time
* should not be used on TSP or similar problems

This example will sort the digits 0123456789 #note that 0 will be removed from the integer
"""

class Node:
    def __init__(self, value):
        # **IMPLEMENT**
        # The node must contain a cost value
        self.cost = int(value)
        self.neighbors = None
    
    @property
    def neigh(self):
        if self.neighbors:
            return self.neighbors
        else:
            self.neighbors = self.generate_neighbors()
            return self.neighbors
    
    def generate_neighbors(self):
        # **IMPLEMENT**
        # generate neighbors
        value = str(self.cost)
        return [value[:i-1]+value[j-1]+value[i:j-1]+value[i-1]+value[j:] for i in range(1,len(value)) for j in range(i+1,len(value)+1)]

def initial_temp():
    # **IMPLEMENT**
    # f.ex upper bound on (max cost - min cost)
    return 987654321.0

def dependant_initial_t( temperature,node,neighbor ):
    # Increase the temperature to make this neighbor a very likely choice
    # This function may not decrease the temperature
    x = temperature/(node.cost-neighbor.cost+1)*math.log1p(100/99)
    return temperature/x if 1>x>0 else temperature

def reduce_t( temperature,repetitions ):
    # common function for temperatur reduction
    return temperature/math.log(repetitions+2,2)

def sa( start_node ):
    node = start_node
    d = len( start_node.neigh ) # number of repetitions pr temperature value
    temperature = initial_temp( )
    
    repetitions = 0
    while temperature>0.001 and node.cost > 123456789:
        neighbor = Node(random.choice( node.neigh )) # choose random neigh
        if neighbor.cost < node.cost: 
            node = neighbor
        else:
            annealing = random.uniform(0,1)
            if annealing < math.exp(-(neighbor.cost-node.cost)/temperature):
                node = neighbor
        repetitions += 1
        
        if repetitions<d: 
            # set a dependant initial temperature
            temperature = dependant_initial_t( temperature,node,neighbor )
        elif repetitions%d==0:             
            temperature = reduce_t( temperature,repetitions )
    #end while
    return node.cost

print sa( Node(value='5647382910') )