import numpy as np
import math
import random

class NPNeuralNet:
    
    def __init__(self,n_inputs, n_outputs, n_hiddens, n_hidden_layers):
        self.n_inputs = n_inputs
        self.n_hiddens = n_hiddens
        self.n_outputs = n_outputs
        self.n_hidden_layers = n_hidden_layers
        
        if n_hidden_layers == 0:
            self.n_weights = ((n_inputs+1)*n_outputs)
        else:
            self.n_weights = (n_inputs+1)*n_hiddens+\
                             (n_hiddens**2+n_hiddens)*(n_hidden_layers-1)+\
                             n_hiddens*n_outputs+n_outputs
        
        # init weights
        self.set_weights( self.generate_weights() )
    
    def generate_weights(self, low=-0.1, high=0.1):
        return np.random.uniform(low, high, size=(1,self.n_weights)).tolist()[0]
    
    def unpack(self, weight_list ):
        if self.n_hidden_layers == 0:
            return [ np.array(weight_list[:(self.n_inputs+1)]).reshape(self.n_inputs+1,self.n_outputs) ]
        else:
            weight_layers = [ np.array(weight_list[:(self.n_inputs+1)*self.n_hiddens]).reshape(self.n_inputs+1,self.n_hiddens) ]
            weight_layers += [ np.array(weight_list[(self.n_inputs+1)*self.n_hiddens+(i*(self.n_hiddens**2+self.n_hiddens)):(self.n_inputs+1)*self.n_hiddens+((i+1)*(self.n_hiddens**2+self.n_hiddens))]).reshape(self.n_hiddens+1,self.n_hiddens) for i in xrange(self.n_hidden_layers-1) ]
            weight_layers += [ np.array(weight_list[(self.n_inputs+1)*self.n_hiddens+((self.n_hidden_layers-1)*(self.n_hiddens**2+self.n_hiddens)):]).reshape(self.n_hiddens+1,self.n_outputs) ]
        return weight_layers
        
    def set_weights(self, weight_list ):
        self.weights = self.unpack( weight_list )
    
    def get_weights(self, ):
        # return weight vector
        return np.hstack(l.flat for l in self.weights)
        
    def get_n_weights(self, ):
        return self.n_weights
    
    
    def update(self, input_values, activation_function ):
        def addOnes(A):
            return np.hstack((np.ones((A.shape[0],1)),A))
        #end addOnes
        def forward( layer_input, weight_layer, activation_function ):
            output = layer_input.dot(weight_layer)
            if activation_function: 
                return activation_function(output)
            return output
        #end forward
        
        output = input_values
        for layer in self.weights[:-1]:
            output = forward( addOnes(output), layer, activation_function )
        output = forward( addOnes(output), self.weights[-1], None )
        
        
        return output[0]

#input_values = np.random.normal(size=(1,n_inputs))
#n_inputs, n_outputs, n_hiddens, n_hidden_layers
#nn = NPNeuralNet(2,1,2,1)