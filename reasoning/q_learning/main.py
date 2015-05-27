from q_learning import Q_learning

class Agent( Q_learning ):
    """Implement these actions"""
    def execute_action(self, state, action ):
        pass
    def list_actions(self, state ):
        pass
    def reward(self, state ):
        pass
    def final_state(self, state ):
        pass
#end class


state = # initial_state

while not agent.final_state( state ):
    agent.forward( state )