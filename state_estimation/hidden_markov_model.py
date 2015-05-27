import numpy as np

def hmm_fwdbwd( initial_state, transitions, history ):
    """
    @param initial_state    A probability vector describing the prob for the initial states
    @param transitions      The transition matrix
    @param history          The history or observation of events 
    """
    def forward( initial_state, transitions, history ):
        probability_vectors = [ np.copy( initial_state ) ]
        for observation in history:
            tmp             = probability_vectors[-1] * transitions * observation
            c               = 1.0/np.sum( tmp )
            probability_vectors.append( c*tmp )
        return probability_vectors
    #end
    
    def backward( transitions, history ):
        backward_vectors    = [ np.ones( (2,1) ) ]
        for observation in reversed( history ):
            tmp             = transitions * observation * backward_vectors[-1]
            c               = 1.0/np.sum( tmp )
            backward_vectors.append( c*tmp )
        return backward_vectors
    #end
    
    def smoothed_probability( probability_vectors, backward_vectors ):
        state_probability   = []
        for forward_vector, backward_vector in zip(probability_vectors, reversed(backward_vectors)):
            tmp             = np.multiply( forward_vector.T, backward_vector )
            c               = 1.0/np.sum( tmp )
            state_probability.append( c*tmp )
        return state_probability
    #end
    
    probability_vectors     = forward( initial_state, transitions, history )
    backward_vectors        = backward( transitions, history )
    state_probability       = smoothed_probability( probability_vectors, backward_vectors )
    
    return state_probability
#end



def create_event( index, events ):
    """
    Creates a new event probability matrix by selecting a 
    column from the event matrix and place them diagonally.
    Eg:
    events matrix:          produced event mat:
    n_features x n_events
    [ 0.9  0.1 ]            [ 0.9  0.0 ]
    [ 0.2  0.8 ]            [ 0.0   0.2]
    """
    return np.diag( events[:,index].flat )
#end

UMBRELLA      = 0
NO_UMBRELLA   = 1

transitions   = np.matrix("0.7 0.3; 0.3 0.7")
events        = np.matrix("0.9 0.1; 0.2 0.8")


history       = [ create_event( UMBRELLA,    events) ]*2 \
              + [ create_event( NO_UMBRELLA, events) ] \
              + [ create_event( UMBRELLA,    events) ]*2

initial_state = np.ones( (1,2) ) * 0.5 # There is a 50-50 prob. for both states

for f in hmm_fwdbwd( initial_state, transitions, history ):
    print f
