import heapq
import random

class Node:
    def __init__(self, value ):
        self.value = value
        self.h_score = None
    
    def generate_children(self, ):
        """
        Implement: generating children
        """
        children = [Node(self.value+random.randint(-5,5)) for _ in xrange(3)]
        return children
    
    def __repr__(self, ):
        return str(self.value)
    
    def __hash__(self, ):
        return str(self.value )
#end Node


def heuristic( node,goal=100 ):
    """
    Implement: calculating heuristic
    """
    node.h_score = abs(node.value-goal) # Evaluate the node
    return (node.h_score, node)
#end heuristic


def beam_search( origin, tabu_size=5, max_iterations=1000, max_children=4 ):
    node_list = [ (-1,origin) ]
    current_node = Node(None) #init for while loop
    tabu_set = []
    
    while current_node.h_score != 0:
        _, current_node = heapq.heappop( node_list ) # select the best node.
        while current_node.value in tabu_set:
              _, current_node = heapq.heappop( node_list ) # select the best node.
        tabu_set = [current_node.value] + tabu_set[:tabu_size-1]
        print current_node.value, tabu_set
        
        for node in current_node.generate_children():
           if node.value not in tabu_set:
              heapq.heappush( node_list, heuristic( node ))
            
        node_list = node_list[:max_children]
    #endwhile
    
    return current_node
# end beam_search


print beam_search( Node(1) )
    
        
        
    
    
    