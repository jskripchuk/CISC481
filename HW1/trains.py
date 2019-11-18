"""
James Skripchuk
CISC481: AI
HW 1

I have times for iterative deepening in iter_deep_results, Yard 2 takes around 500 seconds to complete.
All A* searchers should be < 10 seconds.

PLEASE SEE README FOR RUNNING INSTRUCTIONS
"""

from enum import Enum
import copy
import math
import queue
import sys
import functools 
import heapq
import time

###Defining Yards
yard_1_connection = [[1, 2], [1, 3], [3, 5], [4, 5], [2, 6], [5, 6]]
init_state = [ "*", "e", "", "bca", "", "d"]
goal_state = ["*abcde", "","","","",""]
yard_1 = (yard_1_connection,init_state,goal_state)

yard_2_connection = [[1,2], [1,5], [2,3], [2,4]]
init_state_2 = ["*", "d", "b", "ae", "c"]
goal_state_2 = ["*abcde", "","","",""]
yard_2 = (yard_2_connection,init_state_2, goal_state_2)

yard_3_connection = [[1, 2], [1,3]]
init_state_3 = ["*", "a", "b"]
goal_state_3 = ["*ab", "", ""]
yard_3 = (yard_3_connection,init_state_3,goal_state_3)

yard_4_connection = [[1,2], [1,3], [1,4]]
init_state_4 = ["*", "a", "bc", "d"]
goal_state_4 = ["*abcd","","",""]
yard_4 = (yard_4_connection, init_state_4, goal_state_4)

yard_5_connection = [[1,2], [1,3], [1,4]]
init_state_5 = ["*", "a", "cb", "d"]
goal_state_5 = ["*abcd", "","",""]
yard_5 = (yard_5_connection, init_state_5, goal_state_5)

yards = [yard_1, yard_2, yard_3, yard_4, yard_5]

class Direction(Enum):
    RIGHT = 0
    LEFT = 1

"""
PROBLEM 1:
"""
def possible_actions(yard, state):
    actions = []
    for connection in yard:
        from_track = state[connection[0]-1]
        to_track = state[connection[1]-1]
        if "*" in from_track or "*" in to_track:
                #Don't make moves if there are no cars on the other side
                if len(to_track) != 0:
                    actions.append( (Direction.LEFT, connection[1], connection[0]) )

                if len(from_track) != 0:
                    actions.append( (Direction.RIGHT, connection[0], connection[1]) )
   
    return actions


"""
PROBLEM 2:
"""
def result(action, state):
    direct = action[0]
    from_track = action[1]-1
    to_track = action[2]-1

    new_state = copy.deepcopy(state)

    if direct == Direction.LEFT:
        if len(state[from_track]) != 0:
            new_state[to_track]+=new_state[from_track][0]
            new_state[from_track] = new_state[from_track][1:]
    elif direct == Direction.RIGHT:
        if len(state[from_track]) != 0:
            new_state[to_track] = new_state[from_track][-1]+new_state[to_track]
            new_state[from_track] = new_state[from_track][:-1]


    return new_state


"""
PROBLEM 3:
I actually made a second function called expand_action that does the same thing as expand
but also keeps track of the action that resulted in that state. Don't want to repeat my
code twice.
"""
def expand(state, yard):
    actions = possible_actions(yard, state)
    return [result(act, state) for act in actions]

def expand_action(state,yard):
    actions = possible_actions(yard, state)
    return [(act, result(act, state)) for act in actions]

#Testing
def test_possible_action():
    print("Yard 1")
    print(possible_actions(yard_1_connection, init_state))
    print(possible_actions(yard_1_connection, [ "*b", "e", "", "ca", "", "d"]))

    print("Yard 2")
    print(possible_actions(yard_2_connection, init_state_2))
    print(possible_actions(yard_2_connection, ["*d", "", "b", "ae", "c"]))

    print("Yard 3")
    print(possible_actions(yard_3_connection, init_state_3))
    print(possible_actions(yard_3_connection, ["*a", "", "b"]))

    print("Y1 (LEFT 2 1)")
    print(result((Direction.LEFT, 2,1), init_state))
    print("Y2 (RIGHT 1 2)")
    print(result((Direction.RIGHT, 1,2), init_state))

    print("Expand Yard 1")
    print(expand(init_state,yard_1_connection))

"""
Problem 4

For my blind search, I used iterative deepening.

Iterative deepening is proven optimal like breadth first search,
but is less taxing on my memory since the worst case memory usage is O(d), 
where d is the maximum depth of the result node.

I don't keep track of nodes I've visited before, so it's truly blind.
"""
#Class for search tree nodes
class SearchNode:
    def __init__(self, state):
        self.state = state
        self.action = None
        self.children = []
        self.parent = None
        self.level = 0
        self.g_score = math.inf
        self.f_score = math.inf
    
    #Comparision for the A* search
    def __lt__(self, other):
        return self.f_score < other.f_score


#Recursive implementation of iterative deepening
def iterative_deepening(root, yard, goal, max_depth):
    if root.state == goal:
        return root
    
    #If we're at the max level, return
    if root.level == max_depth:
        return None

    #Find children of current state
    for action_state in expand_action(root.state, yard):
        new_node = SearchNode(action_state[1])
        new_node.action = action_state[0]
        new_node.parent = root
        new_node.level = new_node.parent.level+1 
        root.children.append(new_node)

    #Explore children
    while len(root.children) != 0:
        cur = root.children.pop()
        result = iterative_deepening(cur, yard, goal, max_depth)

        if result != None:
            return result
        else:
            del cur


#Helper function for the depth first search
def search(yard, init, goal):
    root = SearchNode(init)
    max_depth = 18
    for i in range(0, max_depth):
        root = SearchNode(init)
        res = iterative_deepening(root,yard,goal,i)
        if res != None:
            return res
        else:
            pass

    return None

"""
PROBLEM 5:

The amount of possible states is: 
c!*nCr(c+t-1,t-1)

nCr(c+t-1,t-1): This is the canonical formula for the 
    generic question, "how many ways can we put c unlabeled balls
    into t buckets, and buckets can have zero balls". 
    (https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics))

    We can think of our train cars as the balls and our tracks as the buckets.

Now, if we just had the above nCr formula, the ordering of the cars within the tracks
would not matter. Since that does in fact matter, we multiply by c!, which the 
number of possible permutations you can arrange the cars.
"""

"""
PROBLEM 6:

For my algorithm, I chose A*.

My heuristic works as follows:

    1)
    Take the current state list and 'flatten' it into a string.
    E.G ["*","","acd","","b"] -> "*acdb"
    
    If the connectivity list is defined in ascending order (ie left to right), 
        this provides a decent enough approximation on the current "order" of the cars.

    2) 
    Do the same with the goal state list

    3)
    Return the Hamming distance between the two strings.
    
    The Hamming distance is how many edits need to be made to one string to turn it into the other.
    So, if a car is in the wrong place, it adds 1 to the hamming distance. 
    
    This heuristic is admissible because to get one car to another place, it requires AT LEAST one move, so we cannot overestimate.

    (I originally had this idea first, but then discarded it for something else, but then realized that my shiner and faster
        heuristic wasn't actually optimal)
"""

#Stolen from
#http://code.activestate.com/recipes/499304-hamming-distance/
def hamdist(str1, str2):
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def hamming_dist_h(current, goal):
    current_state_str = functools.reduce(lambda a,b: a+b, current)
    goal_state_str = functools.reduce(lambda a,b: a+b, goal)

    return hamdist(current_state_str,goal_state_str)

#Based off of Wikipedia psudocode
#https://en.wikipedia.org/wiki/A*_search_algorithm
def a_star(yard, init, goal, h):
    root = SearchNode(init)
    root.g_score = 0
    root.f_score = h(root.state, goal)

    openSet = []
    closedSet = {}
    heapq.heappush(openSet, root)

    while len(openSet) != 0:
        current = heapq.heappop(openSet)

        if current.state == goal:
            return current

        closedSet[str(current.state)] = 1
        
        #Generate children of node
        for action_state in expand_action(current.state, yard):
            new_node = SearchNode(action_state[1])
            new_node.action = action_state[0]
            new_node.parent = current
            new_node.level = new_node.parent.level+1 
            current.children.append(new_node)

        for child in current.children:
            if str(child.state) not in closedSet.keys():
                tentative_gScore = current.g_score+1

                if tentative_gScore < child.g_score:
                    child.parent = current
                    child.g_score = tentative_gScore
                    child.f_score = child.g_score+h(child.state,goal)
                    
                    heapq.heappush(openSet,child)

    return False


#Print solution path
def print_path(res):
    if res != None:
        cur = res

        path = []
        while cur.parent != None:
            path.append((cur.state, cur.action))
            cur = cur.parent

        path.append((cur.state,cur.action))
        path.reverse()

        print("States:", len(path), "| Actions Taken:",len(path)-1)
        for i in path:
            print(i[0],i[1])

#A* search on default yards
def heuristic_search(yard_list):
    print("A* Search")
    for i, yard in enumerate(yards):
        if i in yard_list:
            print("Yard",i+1)

            start = time.time()
            res = a_star(yard[0], yard[1], yard[2],hamming_dist_h)
            print("Elapsed Time:",time.time()-start)

            print_path(res)

#Depth first search on default yards
def depth_first(yard_list):
    print("Iterative Deepening")
    for i, yard in enumerate(yards):
        if i in yard_list:
            print("Yard",i+1)

            start = time.time()
            res = search(yard[0], yard[1], yard[2])
            print("Elapsed: ",time.time()-start)

            print_path(res)



import argparse

def main():
    parser = argparse.ArgumentParser(description="AI Train Search Problem")
    parser.add_argument("--custom", type=str)
    parser.add_argument("--search_method", type=str)
    parser.add_argument("--yards", nargs='+',type=str)
    parser.add_argument("--test_actions", action="store_true")
    args = parser.parse_args()

    if args.test_actions:
        test_possible_action()
    else:
        if args.custom:
            custom_file = []
            with open(args.custom) as my_file:
                custom_file = my_file.readlines()
            
            custom_file = [x.replace("\n","") for x in custom_file]
            custom_file = [x.replace("[","") for x in custom_file]
            custom_file = [x.replace("]","") for x in custom_file]
            custom_file = [x.replace(" ","") for x in custom_file]
            custom_file = [x.split(",") for x in custom_file]

            connect_yard = []
            i = 0
            while i < len(custom_file[0])-1:
                connect_yard.append([int(custom_file[0][i]), int(custom_file[0][i+1])])
                i+=2
            
            init_state = custom_file[1]
            goal_state = custom_file[2]

            result = None
            print("Custom Yard:",args.custom)
            print(connect_yard)
            print("Init:",init_state)
            print("Goal:",goal_state)
            if args.search_method == "A*":
                print("A* Search")
                result = a_star(connect_yard, init_state, goal_state, hamming_dist_h)
            else:
                print("Iterative Deepening")
                result = search(connect_yard,init_state,goal_state)

            print_path(result)
        else:
            if args.yards:
                yard_list = [int(x)-1 for x in args.yards]
            else:
                yard_list = range(0,4)
            
            if args.search_method == "A*":
                heuristic_search(yard_list)
            else:
                depth_first(yard_list)

if __name__ == "__main__":
    main()