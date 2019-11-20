import uuid

MAX_DEPTH = 300

def pred(name, *var_list):
    return {
        "name": name,
        "vars": list(var_list)
    }




def binding(v, bindings):
    # If there's no binding, return None
    if not v in bindings:
        return None

    while v in bindings:
        v = bindings[v]

    return v


def get_unique_symbol():
    gen = uuid.uuid4()
    gen = str(gen)
    return "?"+gen[0:8]

import copy
def uniqify(clause):
   # print("UNIQI")
    #print(clause)
    clause_copy = copy.deepcopy(clause)
    unique_dict = {}
    #print(clause_copy)

    for predicate in clause_copy:
        for i,var in enumerate(predicate["vars"]):
            if is_var(var):
                if not var in unique_dict:
                    unique_dict[var] = get_unique_symbol()

                predicate["vars"][i] = unique_dict[var]
    
    return clause_copy

def test_uniqify():
    test_clause = [pred("p","?x","?y"), 
            pred("a", "?x", "?z"), 
            pred("a","?z","?y")]

    test_clause = [pred("p","?x","?y")]


    u = uniqify(test_clause)

    print(test_clause)
    print(u)

def replace_bindings(predicate, bindings):
    pred_copy = copy.deepcopy(predicate)
    for i, var in enumerate(pred_copy["vars"]):
        bind = binding(var,bindings)
        if bind:
            pred_copy["vars"][i] = bind

    return pred_copy

def replace_bindings_clause(clause, bindings):
    new_clause = []
    for predicate in clause:
        new_pred = replace_bindings(predicate,bindings)
        new_clause.append(new_pred)

    return new_clause

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
    print(replace_bindings(pred1,bindings))
    #res = binding("?x", bindings)
    #print(res)

def is_var(var):
    try:
        return var[0]=="?"
    except:
        return False


#See if var v occurs in term t
def occurs(v,term,subst={}):
    #print("DOES ",v, "OCCUR IN", term)

    #If they're equal
    if v == term:
        return True
    #If term is a var
    elif is_var(term):
        if subst and term in subst:
            term = subst[term]

        return v == term
    #If term is a predicate
    elif isinstance(term,dict):
        if subst:
            pred1 = replace_bindings(pred1,subst)

        #See if v occurs in term
        for var in pred1["vars"]:
            if v == var:
                return True
        
        return False
    else:
        return False


def unify_var(v, x, subst={}):
    #print("UNIFYING VAR", v, "with", x, "using", subst)
    if v in subst:
        return unify(subst[v], x, subst)
    elif is_var(x) and x in subst:
        return unify(v, subst[x], subst)
    elif occurs(v,x,subst):
        return None
    else:
        subst[v] = x
        return subst



#Returns {} for a successful unification with no bindings
#Returns None for a failure in unification
def unify_helper(x, y, subst={}):
    #print("UNIFY",x,"and",y)
    #if subst==None:
    #    subst={}
    #else:
    #    subst = copy.deepcopy(subst)
    #print(x,y,subst)
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
        #print("AaaaAA")
        return None

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
    #print(pred1)
    #print(pred2)
    res = unify(pred1,pred2)
    print(res)
    print("------")

    
    pred1 = pred("p", "?x","?y")
    pred2 = pred("p", "?z","?w")
    res = unify(pred1,pred2, {"?x":"?w"})
    print(res)
    
    

    preda = pred("p", "?x","Brandon")
    predb = pred("p", "?z","?w")
    #print(preda)
    #print(predb)
    res = unify(preda,predb)
    print(res)

def can_resolve(pred1, pred2):
    #print("CAN RESOLVE ",pred1,pred2)
    return pred1["name"] == pred2["name"] and len(pred1)==len(pred2)

import pprint
pp = pprint.PrettyPrinter(indent=4)

import queue

def resolve(kb, goal, mode="dfs",max_depth=MAX_DEPTH,infinite_loop=True):
    if mode == "dfs":
        open_list = []
        open_list.append( ([goal], {}) )
    else:
        open_list = queue.Queue()
        open_list.put( ([goal], {}) )

    i=0
    successes = []

    while open_list:
        kb = [uniqify(x) for x in kb]

        if mode == "dfs":
            current_node = open_list.pop()
        else:
            if open_list.qsize() == 0:
                break
            current_node = open_list.get()

        current_clause = current_node[0]
        current_bindings = current_node[1]

        for clause in kb:
            to_resolve = clause[0]
            predicate = current_clause[0]
            if can_resolve(predicate,to_resolve):
                

                if infinite_loop:
                    new_clause = copy.deepcopy(clause[1:])
                    new_clause.extend(current_clause[1:])
                else:
                    new_clause = copy.deepcopy(current_clause[1:])
                    new_clause.extend(clause[1:])
                    
                unify_results = unify(predicate,to_resolve,current_bindings)

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


                if new_clause == [] and unify_results != None:
                    successes.append(unify_results)
        
        if i > max_depth:
            print("ERR: Max Depth of",str(max_depth),"Reached")
            return None
        
        i = i+1

    return successes

def print_binding_list(binding_list, goal):
    for i,bindings in enumerate(binding_list):
        final_bindings = "["
        for var in goal["vars"]:
            b = binding(var, bindings)
            final_bindings += (var+"/"+b+", ")
            #print(var,"/",b)

        final_bindings = final_bindings[0:-2]+"]"
        print(final_bindings)

import parser
import os


import argparse

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


def test_resolve(mode="dfs",max_depth = 300):
    folder = "./test_cases"
    files = os.listdir(folder)

    for f in files:
        resolve_file(folder+"/"+f,mode,max_depth)
        print()
        print()

import argparse

def main():
    parser = argparse.ArgumentParser(description="Resolver")
    parser.add_argument("--file", type=str)
    parser.add_argument("--method", type=str)
    parser.add_argument("--max_depth", type=int)
    parser.add_argument("--test_cases", action="store_true")

    args = parser.parse_args()

    method = "dfs"
    max_depth = 300
    
    if args.method:
        method = args.method

    if args.max_depth:
        max_depth = args.max_depth

    if args.test_cases:
        test_resolve(method,max_depth)
    elif args.file:
        resolve_file(args.file, method,max_depth)


if __name__ == "__main__":
    main()


