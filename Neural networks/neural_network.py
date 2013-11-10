import math
import random

BIAS = -1

"""
To view the structure of the Neural Network, type
print [network_name]
"""

class Neuron:
    def __init__(self, n_inputs ):
        self.n_inputs = n_inputs
        self.set_weights( [random.uniform(0,1) for x in range(0,n_inputs+1)] ) # +1 for bias weight
    
    def sum(self, inputs ):
        # Does not include the bias
        return sum(val*self.weights[i] for i,val in enumerate(inputs))
    
    def set_weights(self, weights ):
        self.weights = weights
    
    def __str__(self):
        return 'Weights: %s, Bias: %s' % ( str(self.weights[:-1]),str(self.weights[-1]) )

class NeuronLayer:
    def __init__(self, n_neurons, n_inputs):
        self.n_neurons = n_neurons
        self.neurons = [Neuron( n_inputs ) for _ in range(0,self.n_neurons)]
    
    def __str__(self):
        return 'Layer:\n\t'+'\n\t'.join([str(neuron) for neuron in self.neurons])+''

class NeuralNetwork:
    def __init__(self, n_inputs, n_outputs, n_neurons_to_hl, n_hidden_layers):
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_hidden_layers = n_hidden_layers
        self.n_neurons_to_hl = n_neurons_to_hl
        
        # Do not touch
        self._create_network()
        self._n_weights = None
        # end
    
    def _create_network(self):
        if self.n_hidden_layers>0:
            # create the first layer
            self.layers = [NeuronLayer( self.n_neurons_to_hl,self.n_inputs )]
            
            # create hidden layers
            self.layers += [NeuronLayer( self.n_neurons_to_hl,self.n_neurons_to_hl ) for _ in range(0,self.n_hidden_layers)]
            
            # hidden-to-output layer
            self.layers += [NeuronLayer( self.n_outputs,self.n_neurons_to_hl )]
        else:
            # If we don't require hidden layers
            self.layers = [NeuronLayer( self.n_outputs,self.n_inputs )]
    
    def get_weights(self):
        weights = []
        
        for layer in self.layers:
            for neuron in layer.neurons:
                weights += neuron.weights
        
        return weights
    
    @property
    def n_weights(self):
        if not self._n_weights:
            self._n_weights = 0
            for layer in self.layers:
                for neuron in layer.neurons:
                    self._n_weights += neuron.n_inputs+1 # +1 for bias weight
        return self._n_weights
    
    def set_weights(self, weights ):
        assert len(weights)==self.n_weights, "Incorrect amount of weights."
        
        stop = 0
        for layer in self.layers:
            for neuron in layer.neurons:
                start, stop = stop, stop+(neuron.n_inputs+1)
                neuron.set_weights( weights[start:stop] )
        return self
    
    def update(self, inputs ):
        assert len(inputs)==self.n_inputs, "Incorrect amount of inputs."
        
        for layer in self.layers:
            outputs = []
            for neuron in layer.neurons:
                tot = neuron.sum(inputs) + neuron.weights[-1]*BIAS
                outputs.append( self.sigmoid(tot) )
            inputs = outputs   
        return outputs
    
    def sigmoid(self, activation,response=1 ):
        # the activation function
        try:
            return 1/(1+math.e**(-activation/response))
        except OverflowError:
            return float("inf")
    
    def __str__(self):
        return '\n'.join([str(i+1)+' '+str(layer) for i,layer in enumerate(self.layers)])






#n_inputs, n_outputs, n_neurons_to_hl, n_hidden_layers
#a = NeuralNetwork(2,1,2,1)
#print a.update([1,1])