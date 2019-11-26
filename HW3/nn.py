import networkx as nx


import pprint
import random
import numpy as np

pp = pprint.PrettyPrinter(indent=4)

def add_layer(graph, in_size, out_size):
    
    if graph.nodes:
        num_nodes = graph.number_of_nodes()
        last_layer_nodes = list(graph.nodes)[-in_size:]
        next_layer_nodes = list(range(num_nodes,num_nodes+out_size))
        graph.add_nodes_from(next_layer_nodes)
        
        for i in last_layer_nodes:
            for j in next_layer_nodes:
                graph.add_edge(i,j)

    else:
        graph.add_nodes_from(range(in_size+out_size))
        for i in range(in_size):
            for j in range(in_size,in_size+out_size):
                graph.add_edge(i,j)

def threshold_activation(x):
        if x < 0:
            return 0
        else:
            return 1

def sigmoid(x):
    return (1/(1+np.exp(-x)))

class Network():
    def __init__(self,activation):
        self.layers=[]
        self.layer_values = []
        self.graph = nx.Graph()
        self.weights = {}
        self.in_size = 0
        self.activation = activation

    def add_layer(self,in_size,out_size):
        # Not first layer
        if self.graph.nodes:
            num_nodes = self.graph.number_of_nodes()
            last_layer_nodes = list(self.graph.nodes)[-in_size:]
            next_layer_nodes = list(range(num_nodes,num_nodes+out_size))
            
            self.graph.add_nodes_from(next_layer_nodes)
            self.layers.append(next_layer_nodes)

            #Fully connect last layer to this layer
            for i in last_layer_nodes:
                for j in next_layer_nodes:
                    self.weights[(i,j)] = 1
                    self.graph.add_edge(i,j)

            #Hook up bias layer
            for i in next_layer_nodes:
                self.weights[(0,i)] = 1
                self.graph.add_edge(0,i)

            
        else:
            #Add a dummy input node for biases
            self.in_size = in_size


            in_size+=1

            to_add = range(in_size+out_size)
            self.graph.add_nodes_from(to_add)

            self.layers.append(list(range(1,in_size)))
            self.layers.append(list(range(in_size,in_size+out_size)))


            for i in range(in_size):
                for j in range(in_size,in_size+out_size):
                    self.weights[(i,j)] = 1
                    self.graph.add_edge(i,j)

    def classify(self, x):
        self.layer_values = []
        if len(x) != self.in_size:
            print("Invalid input size")
            return None
        else:
            #Dummy var for bias
            #x.append(1)

            prev_layer = self.layers[0]
            current_layer = self.layers[1]
            prev_values = x

            i = 1
            while current_layer != None:  
                #Dummy var for bias
                prev_values.append(1)
                new_values = []
                self.layer_values.append(prev_values)
                #print(prev_values)

                for j in current_layer:

                    curr_weights = [self.weights[i,j] for i in prev_layer]
                    curr_weights.append(self.weights[0,j])

                    dot = sum([value*weight for value,weight in zip(prev_values,curr_weights)])
                    res = self.activation(dot)
                    new_values.append(res)

                

                # Iterate
                #print("New Values",new_values)
                #print(new_values)
                prev_values = new_values
                prev_layer = current_layer
                if i+1 < len(self.layers):
                    current_layer = self.layers[i+1]
                    i = i+1
                else:
                    current_layer = None

                #print("----")

            self.layer_values.append(prev_values)
            return prev_values
        
    def weight_update(self,w,expected,result,inp):
        self.weights[w] = self.weights[w] + (expected-result)*inp

    def weight_update_sigmoid(self,w,expected,result,inp):
        pass


    def backprop(self,expected):
        #Update internal
        o = self.layer_values[2]
        t = expected
        h = self.layer_values[1][0:2]
        x = self.layer_values[0]


        #print(o,t)
        delta_o = [(t[i]-o[i])*o[i]*(1-o[i]) for i in range(0,2)]


        #for j,n in enumerate(self.layers[1]):
        #    for k,m in enumerate(self.layers[2]):
        #        delta = h[j]*delta_o[k]
                #print(self.weights[n,m])
        #        self.weights[n,m] = self.weights[n,m]+delta
                #print(self.weights[n,m])
                #print(delta)
                #self.weights[]
                #print(j,k)
        #print(h)

        self.weights[3,5] = self.weights[3,5] + h[0]*delta_o[0]
        self.weights[3,6] = self.weights[3,6] + h[0]*delta_o[1]

        self.weights[4,5] = self.weights[4,5] + h[1]*delta_o[0]
        self.weights[4,6] = self.weights[4,6] + h[1]*delta_o[1]

        delta_h = [0, 0]
        #print(self.layers[1])
        #Node 3
        delta_h[0] = h[0]*(1-h[0])*(self.weights[3,5]*delta_o[0]+self.weights[3,6]*delta_o[1])
        delta_h[1] = h[1]*(1-h[1])*(self.weights[4,5]*delta_o[0]+self.weights[4,6]*delta_o[1])


        

        self.weights[1,3] = self.weights[1,3] + x[0]*delta_h[0]
        self.weights[1,4] = self.weights[1,4] + x[0]*delta_h[1]

        self.weights[2,3] = self.weights[2,3] + x[1]*delta_h[0]
        self.weights[2,4] = self.weights[2,4] + x[1]*delta_h[1]

        self.weights[0,3] = self.weights[0,3] + 1*delta_h[0]
        self.weights[0,4] = self.weights[0,4] + 1*delta_h[1]

        self.weights[0,5] = self.weights[0,5] + 1*delta_o[0]
        self.weights[0,6] = self.weights[0,5] + 1*delta_o[1]

    #Only good for one layer network
    def update_weights(self, expected):
        output_layer = self.layer_values[-1]
        input_layer = self.layer_values[0]
        for en,j in enumerate(self.layers[-1]):
            expect = expected[en]
            actual = output_layer[en]
            input_val = input_layer[en]
            for i in self.layers[0]:
                self.weight_update((i,j),expect,actual,input_val)

            self.weight_update((0,j),expect,actual,1)
        
    def randomize_weights(self):
        for k in self.weights:
            self.weights[k] = random.random()


    def print_graph(self):
        print("Nodes")
        pp.pprint(list(self.graph.nodes))

        print("Layers")
        pp.pprint(self.layers)
        
        print("Edges")
        pp.pprint(list(self.graph.edges))

        print("Weights")
        pp.pprint(self.weights)


TRAINING = [
    ([0,0], [0,0]),
    ([0,1], [0,1]),
    ([1,0], [0,1]),
    ([1,1], [1,0])
]

import copy

def test():
    g = Network(threshold_activation)
    g.add_layer(2,2)
    #g.add_layer(2,2)

    #print(TRAINING)
    #g.randomize_weights()
    print(g.weights)

    for pair in copy.deepcopy(TRAINING):
        #print(g.weights)
        x = pair[0]
        y = pair[1]
        print(g.classify(x))

    for i in range(0,20):
        for pair in copy.deepcopy(TRAINING):
            x = pair[0]
            y = pair[1]

            res = g.classify(x)
            g.update_weights(y)

    print("-----------")
    print(g.weights)
    #print("--------")

    for pair in copy.deepcopy(TRAINING):
        x = pair[0]
        y = pair[1]
        print(g.classify(x))

    

def sig_result(inp):
    return [x > 0.5 for x in inp]

def loss(inp, exp):
    return sum([(x-y)**2 for x,y in zip(inp,exp)])

import csv

def two_layer():
    g = Network(sigmoid)
    g.add_layer(2,2)
    g.add_layer(2,2)
    g.randomize_weights()
    losses = []

    print(g.weights)
    for i in range(0,6000):
        #print("-----")
        for pair in copy.deepcopy(TRAINING):
            x = pair[0]
            y = pair[1]
            res = g.classify(x)
            losses.append(loss(res,y))
            #print(loss(res,y))
            g.backprop(y)

    print(losses[-1])

    for pair in copy.deepcopy(TRAINING):
            x = pair[0]
            y = pair[1]
            res = g.classify(x)
            print(res)
            print(sig_result(res))

    #print(len(losses))
    #print(losses)
    with open("./losses.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        for r in losses:
            wr.writerow([r])

def main():
    #test()
    two_layer()
    

    


    #print(sigmoid(-100))
    
        #print(g.layer_values)
    #res = g.classify( [1,0] )
    #print(g.layers)
    #print(g.layer_values)
    #g.update_weights([0,1])
    #print(res)

if __name__ == "__main__":
    main()
