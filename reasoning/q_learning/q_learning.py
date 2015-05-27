import collections
import random

settings = {
    "trace_decay"   : 0.3,
    "discount"      : 0.8, # Range [0, 1] : closer to 1 signifies "deep belief"
    "k_increase"    : 0.005
}

class Q_learning( object ):
    def __init__(self, **kwargs ):
        settings.update( kwargs )
        self.__dict__.update( settings )
        
        self.q_values = collections.defaultdict( float )            # Contains the Q values
        self.n_visits = collections.defaultdict( int )              # Times entered a given state
        self.k = 1.0                                                # Used in the explorative, weighted selection
        
        self.eligibility_trace = collections.defaultdict(lambda:1.) # TD(lambda)
        self.trace = []                                             # Chronological path of visited states
    #end
    
    def execute_action(self, state, action ):
        assert False, "Q_learning.class requires you to implement the function `execute_action`"
        return None # the state entered
    #pass
    
    def list_actions(self, state ):
        """NOTE: remember to define a end state"""
        assert False, "Q_learning.class requires you to implement the function `list_actions`"
        return [] # list of actions
    #pass

    def reward(self, state ):
        assert False, "Q_learning.class requires you to implement the function `reward`"
        return 0.0 # float value
    #end
    
    def get_Q(self, state, action ):
        # May be used as a afterstate function. 
        return self.q_values[ (state, action) ]
    #end
    
    def explore_move(self, state ):
        self.k += self.k_increase
        
        # No moves available
        if not self.list_actions(state):
            return 0, None
            
        options = [
              (self.k**self.get_Q( state, action ), action)
              for action in self.list_actions(state)
           ]
        
        total = sum( q for q, action in options )
        
        # Don't bother with a roulette if all weights are zero
        if total==0:
            return random.choice( options )
        
        # Ranked random selection
        chosen = random.uniform( 0, total )
        for value, action in reversed(options):
            chosen -= value
            if chosen<=0:
                return value, action
        
        assert False, "No action were chosen by the explore_move()"
    # end
    
    def greedy_move(self, state ):
        best, chosen = -float("inf"), []
        
        for action in self.list_actions( state ):
            state_q = self.get_Q( state, action )
            
            if state_q == best:
                chosen.append( action )
            elif state_q > best:
                chosen = [ action ]
                best = state_q
        
        return best, random.choice( chosen ) if chosen else None
    #end
    
    def backtrack(self, state, final_reward ):
        self.trace.reverse() # final state was at the end of the list
        
        factor = self.discount * self.trace_decay
        
        for i, key in enumerate(self.trace):
            self.eligibility_trace[ key ] += factor**i * final_reward
        
        self.trace = []
    
    def Q(self, state, action ):
        def learning_rate( key ):
            self.n_visits[ key ] += 1
            return 1.0/(1+self.n_visits[ key ])
        #end
    
        key = (state, action)
        self.trace.append( key )
        
        alpha = learning_rate(key) # 1 if fully deterministic environment
        
        next_state = self.execute_action( state, action )
        next_state_q, next_state_action = self.greedy_move( next_state )
    
        state_reward = self.reward( next_state )
        new_knowledge = state_reward + self.discount * next_state_q - self.get_Q( state, action )
        
        self.q_values[ (state, action) ] += alpha * new_knowledge * self.eligibility_trace[ (state, action) ]
        
        return next_state
    #end
    
    def forward(self, state, GREEDY=False ):
        if GREEDY:
            next_action = self.greedy_move( state )[1]
        else:
            next_action = self.explore_move( state )[1]
            
        
        next_state = self.Q( state, next_action )
        
        return next_state
    #end
#end class

