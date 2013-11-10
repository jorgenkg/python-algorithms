import numpy as np
import random
import copy

"""
Loads a sudoku.txt file
0 3 0 5 9 7 4 0 0
0 7 2 0 0 6 0 0 0
0 0 0 0 0 0 9 8 0
0 0 9 0 5 1 3 0 0
5 0 0 0 3 0 0 0 6
0 0 6 7 0 0 2 0 0
0 2 5 0 0 0 0 0 0
0 0 0 4 0 0 5 1 0
0 0 8 1 0 5 0 2 0
"""

"""
Sudoku solver

CSP:
1) Fills in the fields where there is only one valid digit.
2) Repeat step one until there are no more digits to fill in.
Backtrack search:
3) Find the field with the smallest domain of valid digits.
4) Choose a random digit from the domain.
5) Skip to step 1. If it encounters an empty domain, it will mark
the randomly chosen value as illegal and skip to step 1 again in case
this reduces the domain to one digit.
"""

class Field:
    def __init__(self, x,y,value,n_sudoku ):
        self.x = x
        self.y = y
        self.value = value
        self.neigbors = set()
        self.domain = set()
        self.denied_values = set()
    
    def __repr__(self, ):
        return u"%s" % str(self.domain)
        #return u"%s [%d,%d]" % (self.value, self.x, self.y)
    
    def related_to(self, elements ):
        """
        Used during loading
        """
        self.neigbors.update( [elem for elem in elements if elem!=self] )
#end Class

def load_board( file ):
    matrix = np.loadtxt( file,dtype=int )
    n_sudoku = int(np.sqrt(matrix.shape[0]))
    
    fields = np.empty(shape=matrix.shape, dtype="object")
    for y,row in enumerate(matrix):
        """
        Create objects
        """
        for x,column in enumerate(row):
            fields[y,x] = Field(y,x,column,n_sudoku)
    
    for y_box in xrange(0,matrix.shape[0],n_sudoku):
        """
        Register boxes
        """
        for x_box in xrange(0,matrix.shape[0],n_sudoku):
            elements = list(fields[y_box:y_box+n_sudoku,x_box:x_box+n_sudoku].flat)
            filter(
                lambda x: x.related_to( elements ),
                elements
            )
    
    for row in fields:
        """
        Register rows
        """
        elements = list(row.flat)
        filter(
            lambda x: x.related_to( elements ),
            elements
        )
    
    for column in fields.T:
        """
        Register columns
        """
        elements = list(column.flat)
        filter(
            lambda x: x.related_to( elements ),
            elements
        )
    
    
    return list(fields.flat)
#end 


def perform_unary( fields ):
    n_sudoku = int(np.sqrt(len(fields)))
    default_domain = set(xrange(1,n_sudoku+1))
    
    change = True
    while change:
        finished = True
        change = False
        
        for field in fields:
            
            if field.value!=0:
                field.domain = set([field.value])
            else:
                finished = False
                blocked = {x.value for x in field.neigbors} | field.denied_values
                field.domain = default_domain - blocked
                if len(field.domain)==0:
                    raise Exception("Empty domain")
                elif len(field.domain)==1:
                    field.value = field.domain.pop()
                    change = True
    
    return fields, finished
#end 


def backtrack_search( fields ):
    def get_undecided( fields ):
        return sorted(
                    [field for field in fields if len(field.domain)>=2],
                    key=lambda x:len(x.domain),
                    reverse = True
                )
    #end get_undecided
    
    done = False
    while not done:
        restore_point = copy.deepcopy(fields)
        population = get_undecided(fields)
        origin_field = None
        
        while population:
            field = population.pop()
            field.value = field.domain.pop()
            
            if not origin_field:
                origin_field = field
    
            try:
                fields,done = perform_unary( fields )
                population = get_undecided( fields )
            except Exception, e:
                fields = restore_point
                
                for field in fields:
                    if field.x == origin_field.x and field.y==origin_field.y:
                        field.denied_values.add( origin_field.value )
                
                fields,done = perform_unary( fields )
                break 
        #endwhile
    
    return fields


board = load_board( "sudoku.txt" )

fields, done = perform_unary( board )

if not done:
    fields = backtrack_search( fields )


visual = np.empty(shape=(int(np.sqrt(len(fields))),int(np.sqrt(len(fields)))),dtype=int)
for field in fields:
    visual[field.x,field.y] = field.value

print visual