import heapq
import random

"""
Beam search
* The goal value must be set in the heuristic parameter.
"""


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
#end Node


def heuristic( node,goal=100 ):
    """
    Implement: calculating heuristic
    """
    node.h_score = abs(node.value-goal) # Evaluate the node
    return (node.h_score, node)
#end heuristic


def beam_search( origin, max_iterations=1000, max_children=12 ):
    
    node_list = [ (-1,origin) ]
    current_node = Node(None) #init for while loop
    
    while current_node.h_score != 0:
        _,current_node = heapq.heappop( node_list ) # select the best node.
        
        filter( 
                # Add newly generated children to the node list.
                lambda node: heapq.heappush( node_list, node ),  
                map( heuristic, current_node.generate_children() )
            )
            
        node_list = node_list[:max_children]
    #endwhile
    
    return current_node
# end beam_search


print beam_search( Node(1) )
    
        
        
    
    
    