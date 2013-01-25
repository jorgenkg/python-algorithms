from Queue import PriorityQueue

exists = {} # Keep track of existing nodes, so that one node may have multiple parents. Required to find optimal path.

class AstarNode:
   parent = None
   f_score = None
   h_score = None
   is_expanded = False
   is_observed = False
   g_score = ( )
   children = [ ]
   
   def generate_children(self):
      # INITIATE children
      n = Node()
      if n.key not in exists.keys():
         exists.update({n.key:n})
      self.children.append(exists[n.key])

class Node( AstarNode ):
    key = 'key_string' # requires a unique key for each node.
    """
        Here goes your node info
    """

def heuristic(node,goal):
   """
       Define a heuristic for you search
   """

def distance(parent,child):
   """
       How far is it between these two neighbouring nodes?
       This is the edge weight in a weighted graph
   """

def astar(start,goal):
   queued_nodes = PriorityQueue()
   start.g_score = 0
   start.h_score = heuristic(start,goal)
   start.f_score = start.g_score + start.h_score
   start.is_observed = True
   queued_nodes.put((start.f_score,start))
   
   while not queued_nodes.empty():
      current = queued_nodes.get()[1] # [f_score, node]
      
      if current.h_score == 0:
         return construct_path(current)
      else:
         current.is_observed = True
         current.generate_children()
         current.is_expanded = True
         for child in current.children:
            evaled_g_score = current.g_score + distance(current,child)
            if evaled_g_score<child.g_score:
               if child.is_expanded:
                  child.parent = current
                  child.g_score = evaled_g_score
                  child.f_score = child.g_score + child.h_score
                  current.is_expanded = False
                  child.is_observed = False
                  queued_nodes.put((child.f_score,child))
               elif child.is_observed:
                  child.parent = current
                  child.g_score = evaled_g_score
               else:
                  current.is_observed = True
                  child.parent = current
                  child.g_score = evaled_g_score
                  child.h_score = heuristic(child,goal)
                  child.f_score = child.g_score + child.h_score
                  queued_nodes.put((child.f_score,child))
   return Exception('No result')


def construct_path(node):
   if node.parent:
      return construct_path(node.parent) + [node]
   else:
      return [node]