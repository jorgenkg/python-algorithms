import heapq
import math
import itertools


exists = {} # Keep track of existing nodes, so that one node may have multiple parents. 
            # This is required if you wish to find the optimal path.
exist_key = set() # for a faster existence check.

class AstarNode( object ):
   def __init__(self, ):
      self.parent = None
      self.f_score = None
      self.h_score = None
      self.is_expanded = False
      self.is_observed = False
      self.g_score = ( )
#end necessary values


class Node( AstarNode ):
   def __init__(self, ):
      super(Node, self).__init__()
      self.key = " " # unique key for hashing purposes.

   def generate_children(self):
      """
      Implement: generate children
      """
      children = []
      for child in children:
          node = Node( child )
          if node.key not in exist_key:
             exists.update({node.key:node})
             exist_key.add(node.key)
          children.append(exists[node.key])
      return children
#end


def heuristic(node):
   """
   Implement: heuristc
   """
   return 1

def distance(parent,child):
   """
   We dont have any definition of the distance between two nodes.
   """
   return 1
   

def astar(start):
   start.g_score = 0
   start.h_score = heuristic(start)
   start.f_score = start.g_score + start.h_score
   start.is_observed = True
   queued_nodes = [ (start.f_score,start) ]
   
   
   while not queued_nodes.empty():
      current = heapq.heappop(queued_nodes)[1] # [f_score, node]
      if current.h_score == 0:
         return construct_path(current)
      else:
         current.is_observed = True
         children = current.generate_children()
         current.is_expanded = True
         for child in children:
            evaled_g_score = current.g_score + distance(current,child)
            if evaled_g_score<child.g_score:
               if child.is_expanded:
                  child.parent = current
                  child.g_score = evaled_g_score
                  child.f_score = child.g_score + child.h_score
                  current.is_expanded = False
                  child.is_observed = False
                  heapq.heappush( queued_nodes, (child.f_score,child) )
               elif child.is_observed:
                  child.parent = current
                  child.g_score = evaled_g_score
               else:
                  current.is_observed = True
                  child.parent = current
                  child.g_score = evaled_g_score
                  child.h_score = heuristic(child)
                  child.f_score = child.g_score + child.h_score
                  heapq.heappush( queued_nodes, (child.f_score,child) )
   return Exception('No result')

def construct_path(node):
   tmp = []
   while node.parent:
       tmp.append( node.parent )
       node = node.parent
   return tmp


"""
Example usage:
print astar(  )
"""
