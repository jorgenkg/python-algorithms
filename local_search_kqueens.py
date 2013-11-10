import random
import math
import itertools
import heapq
import numpy as np
np.seterr(divide="raise")


"""
TODO

rewrite to state domains
   queens instead of boards
"""


class Board:
    def __init__(self, gene ):
        # The node must contain a cost value
        self.gene = gene
        self.cost = objective_function( gene )
    
def objective_function( gene ):
   n = gene.shape[0] # board size
   k = 1             # number of queens allowed in same row
   horizonal = np.sum(gene, axis=1)-k
   vertical = np.sum(gene, axis=0)-k
   diag1 = np.array([
                      sum(gene.diagonal(k-n+i))
                      for i in xrange(2*(n-k)+1)
                  ])-k
   diag2 = np.array([
                      sum(np.fliplr(gene).diagonal(k-n+i))
                      for i in xrange(2*(n-k)+1)
                  ])-k

   return  np.sum(horizonal[horizonal>0],axis=0) + \
          np.sum(vertical[vertical>0],axis=0) + \
          np.sum(diag2[diag2>0],axis=0) + \
          np.sum(diag1[diag1>0],axis=0)


def generate_permutations( numpy_array ):
   size = numpy_array.shape[0]
   container = np.zeros(shape=(size,size))
   
   for i in xrange( size ):
      container[i,i]=1
   
   return container

def local_search( start_node, goal_cost=0 ):
    node = start_node
    
    while node.cost > goal_cost:
      
      while True:
         """
         Pick a random row and check if it is causing conflicts
         """
         i = random.randint( 0, start_node.gene.shape[0]-1 ) # select row to manipulate
         tmp = np.copy( node.gene )
         tmp[i,:]=0
         if objective_function(tmp)<node.cost:
            # Yep, this caused some conflicts
            break
      
      neighbors = [ (float("inf"),None) ]

      for modified in generate_permutations(node.gene[i]):
        tmp = np.copy( node.gene )
        tmp[i] = modified
        node = Board(tmp)
        
        if node.cost == neighbors[0][0]:
           neighbors.append((node.cost,node))
        elif node.cost<neighbors[0][0]:
           neighbors = [ (node.cost,node)]
           
      
      node = random.choice(neighbors)[1]
    #end while
    
    return node



n=10 # bord size
gene = np.array([[0]*i+[1]+[0]*(n-i-1) for i in range(n)]).reshape(n,n)

print local_search( 
                     Board( gene )
                  ).gene