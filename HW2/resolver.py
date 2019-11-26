import uuid
import copy
import queue
import os
import parser
import argparse

MAX_DEPTH = 300

# A predicate is it's name and vars
def pred(name, *var_list):
    return {
        "name": name,
        "vars": list(var_list)
    }

####################
# HELPER FUNCTIONS #
####################

# Chases the bindings of a variable through the variable dict
def binding(v, bindings):
    # If there's no binding, return None
    if not v in bindings:
        return None

    while v in bindings:
        v = bindings[v]

    return v

def test_bindings():
    bindings = {
        "?x": "?y",
        "?y": "?z",
        "?w": "?q",
        "?z": "?w",
        "?aa": "?t",
        "?t": "?Wow"
    }

    pred1 = pred("apple", "?xaaaa", "?aa")
    print(pred1)
    print(bindings)
    print(replace_bindings(pred1,bindings))

# Use a UUID as a unique symbol
def get_unique_symbol():
    gen = uuid.uuid4()
    gen = str(gen)
    return "?"+gen

# Uniquifies a clause
def uniquify(clause):
    clause_copy = copy.deepcopy(clause)
    unique_dict = {}

    for predicate in clause_copy:
        for i,var in enumerate(predicate["vars"]):
            if is_var(var):
                if not var in unique_dict:
                    unique_dict[var] = get_unique_symbol()

                predicate["vars"][i] = unique_dict[var]
    
    return clause_copy

def test_uniquify():
    test_clause = [pred("p","?x","?y"), 
            pred("a", "?x", "?z"), 
            pred("a","?z","?y")]

    test_clause = [pred("p","?x","?y")]


    u = uniquify(test_clause)

    print(test_clause)
    print(u)

# Takes in a predicate and replaces it's bindings based off of the bindings dict
def replace_bindings(predicate, bindings):
    pred_copy = copy.deepcopy(predicate)
    for i, var in enumerate(pred_copy["vars"]):
        bind = binding(var,bindings)
        if bind:
            pred_copy["vars"][i] = bind

    return pred_copy

# Replace the bindings for a whole clause
def replace_bindings_clause(clause, bindings):
    new_clause = []
    for predicate in clause:
        new_pred = replace_bindings(predicate,bindings)
        new_clause.append(new_pred)

    return new_clause

###############
# UNIFICATION #
###############

# Code is adapted from general unification algorithm
# https://www.javatpoint.com/ai-unification-in-first-order-logic
# And this python implementation
# https://eli.thegreenplace.net/2018/unification/

def is_var(var):
    try:
        return var[0]=="?"
    except:
        return False


# See if var v occurs in term t
def occurs(v,term,subst={}):
    # If they're equal
    if v == term:
        return True
    # If term is a var
    elif is_var(term):
        if subst and term in subst:
            term = subst[term]

        return v == term
    # If term is a predicate
    elif isinstance(term,dict):
        if subst:
            pred1 = replace_bindings(pred1,subst)

        # See if v occurs in term
        for var in pred1["vars"]:
            if v == var:
                return True
        
        return False
    else:
        return False

# Unifies variable v with term t
def unify_var(v, x, subst={}):
    if v in subst:
        return unify(subst[v], x, subst)
    elif is_var(x) and x in subst:
        return unify(v, subst[x], subst)
    elif occurs(v,x,subst):
        return None
    else:
        subst[v] = x
        return subst


def unify_helper(x, y, subst={}):
    if subst == None:
        return None
    if x == y:
        return subst
    elif is_var(x):
        return unify_var(x,y,subst)
    elif is_var(y):
        return unify_var(y,x,subst)
    elif isinstance(x,dict) and isinstance(y,dict):
        for i,var in enumerate(x["vars"]):
            subst = unify(x["vars"][i], y["vars"][i], subst)
        return subst
    else:
        return None

# Can (try and) unify two predicates if they have the same name and same number of vars
def can_unify(pred1, pred2):
    return pred1["name"] == pred2["name"] and len(pred1['vars'])==len(pred2['vars'])

# Unify two predicates
# Returns {} for a successful unification with no bindings
# Returns None for a failure in unification
def unify(p1,p2,subst={}):
    return unify_helper(p1,p2,copy.deepcopy(subst))

def test_unify2():
    p1 = {"name":"parent",
        "vars": ['?z','?y']}
    p2 = {"name": "parent",
        "vars": ["Brian","Doug"]}
    b = {'?x1': '?x', '?y1': '?y', '?x': 'Mary', '?z': 'Sue'}
    res = unify(p1,p2,b)
    print(res)

def test_unify():
    pred1 = pred("p", "?x")
    pred2 = pred("p", "?y")
    print(pred1)
    print(pred2)
    res = unify(pred1,pred2)
    print(res)
    print("------")

    
    pred1 = pred("p", "?x","?y")
    pred2 = pred("p", "?z","?w")
    res = unify(pred1,pred2, {"?x":"?w"})
    print(pred1)
    print(pred1)
    print(res)
    print("-------")
    
    preda = pred("p", "?x","Brandon")
    predb = pred("p", "?z","?w")
    print(preda)
    print(predb)
    res = unify(preda,predb)
    print(res)

##############
# RESOLUTION #
##############

# Resolution Algorithm
def resolve(kb, goal, mode="dfs",max_depth=MAX_DEPTH,infinite_loop=True):

    # Use a stack for DFS
    if mode == "dfs":
        open_list = []
        open_list.append( ([goal], {}) )
    
    # Use a queue for BFS
    else:
        open_list = queue.Queue()
        open_list.put( ([goal], {}) )

    depth=0

    # Successfuly proved results
    successes = []

    # If open list has something in it
    while open_list:

        # Generate fresh premises 
        kb = [uniquify(x) for x in kb]

        # Get next node
        if mode == "dfs":
            current_node = open_list.pop()
        else:
            if open_list.qsize() == 0:
                break
            current_node = open_list.get()

        current_clause = current_node[0]
        current_bindings = current_node[1]

        # For every clause in the KB
        for clause in kb:

            # See if we can unify the first predicate in the clause with our current predicate
            to_resolve = clause[0]
            predicate = current_clause[0]
            if can_unify(predicate,to_resolve):
                
                # If we want to avoid the infinite loop problem we switch the order in which we resolve the clauses
                # You can change it for yourself in the code and see what happens
                # But he said we're supposed to get an infinite loop :)
                if infinite_loop:
                    new_clause = copy.deepcopy(clause[1:])
                    new_clause.extend(current_clause[1:])
                else:
                    new_clause = copy.deepcopy(current_clause[1:])
                    new_clause.extend(clause[1:])
                    
                unify_results = unify(predicate,to_resolve,current_bindings)

                # If we don't get an empty clause or failed resolution
                # Put the remainder of the clause on the open list
                if unify_results != None and new_clause != []:
                    if mode == "dfs":
                        open_list.append(
                            (new_clause, 
                            unify_results
                        ))
                    else:
                        open_list.put(
                            (new_clause, 
                            unify_results
                        ))

                # If we get an empty clause, the resolution was successful!
                if new_clause == [] and unify_results != None:
                    successes.append(unify_results)
        
        # Bail out if we reach too low a depth
        if depth > max_depth:
            print("ERR: Max Depth of",str(max_depth),"Reached")
            return None
        
        depth = depth+1

    return successes

################
# USER RUNNING #
################

def print_binding_list(binding_list, goal):
    for i,bindings in enumerate(binding_list):
        final_bindings = "["
        for var in goal["vars"]:
            b = binding(var, bindings)
            final_bindings += (var+"/"+b+", ")

        final_bindings = final_bindings[0:-2]+"]"
        print(final_bindings)

def resolve_file(filename, mode="dfs", max_depth=MAX_DEPTH):
    search_dic = {"bfs": "Breadth First Search", "dfs": "Depth First Search"}

    PAGE_BREAK_SIZE = 40
    print("#"*PAGE_BREAK_SIZE)
    kb, g, name = parser.parse_file(filename)
    print(name+":")
    print("Resolving using",search_dic[mode])
    print("-"*PAGE_BREAK_SIZE)


    res = resolve(kb,g,mode,max_depth)
    if res:
        print_binding_list(res,g)
    else:
        print("Resolution Failed")
    print("#"*PAGE_BREAK_SIZE)


def test_resolve_folder(folder,mode="dfs",max_depth = 300):
    files = os.listdir(folder)

    for f in files:
        resolve_file(folder+"/"+f,mode,max_depth)
        print()
        print()


def helper_function_test():
    print("Helper Function Tests")

    print("Test Bindings")
    test_bindings()

    print("Test Unify")
    test_unify()
    test_unify2()

    print("Test Uniquify")
    test_uniquify()
    pass

def main():
    parser = argparse.ArgumentParser(description="Resolution Theorem Prover for CISC481. James Skripchuk 2019")
    parser.add_argument("--file", type=str, help="A file containing a set of premise clauses and a goal clause.")
    parser.add_argument("--folder", type=str, help="A folder containing different files of test cases to resolve.")
    parser.add_argument("--method", type=str, help="Search Method. 'bfs' or 'dfs'. Defaults to dfs.")
    parser.add_argument("--max_depth", type=int, help="How long to search until terminating early. Used to prevent infinite loops. Defaults to 300.")
    parser.add_argument("--test_cases", action="store_true", help="Run through the provided test cases.")
    parser.add_argument("--helper_function_test", action="store_true", help="Run through tests on helper functions.")



    args = parser.parse_args()

    method = "dfs"
    max_depth = 300
    folder = ""

    if args.helper_function_test:
        helper_function_test()
    
    if args.method:
        method = args.method

    if method != "dfs" and method != "bfs":
        print("Search method must be 'dfs' or 'bfs'. Run 'python3 resolver.py' -h for details")
        quit()

    if args.max_depth:
        max_depth = args.max_depth

    if args.folder:
        folder = args.folder

    if args.test_cases:
        folder = "./test_cases"
    
    if folder:
        test_resolve_folder(folder,method,max_depth)
    elif args.file:
        resolve_file(args.file, method,max_depth)

    if not folder and not args.file and not args.test_cases:
        print("No file or folder specified. Use --folder, --file, or --test_cases arguments. Run 'python3 resolver.py -h' for details.")


if __name__ == "__main__":
    main()


