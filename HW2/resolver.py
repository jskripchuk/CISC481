import uuid

def pred(name, *var_list):
    return {
        "name": name,
        "vars": list(var_list)
    }

KB_1 = [
    [pred("grandparent", "?x", "?y"), pred("parent", "?x", "?z"), pred("parent", "?z", "?y")],
    [pred("parent", "Brian", "Doug")],
    [pred("parent", "Doug", "Mary")],
    [pred("parent", "Mary", "Sue")]
]

GOAL_1 = pred("grandparent", "?x1", "?y1")

KB_2 = [
    [pred("aunt","?x","?y"), pred("sister","?x","?z"), pred("mother","?z","?y")],
    [pred("aunt","?x","?y"), pred("sister","?x","?z"), pred("father","?z","?y")],
    [pred("sister","Mary","Sue")],
    [pred("sister","Mary","Doug")],
    [pred("father","Doug","John")],
    [pred("mother","Sue","Paul")]
]

GOAL_2 = pred("aunt","?x","?y")

KB_3 = [
    [pred("simple_sentence", "?x", "?y", "?z", "?u" ,"?v"),
     pred("noun_phrase", "?x", "?y"),
     pred("verb_phrase", "?z", "?u", "?v")],

    [pred("noun_phrase", "?x", "?y"), pred("article", "?x"), pred("noun", "?y")],
    [pred("verb_phrase","?x","?y","?z"), pred("verb","?x"), pred("noun_phrase","?y","?z")],
    [pred("article","a")],
    [pred("article","the")],
    [pred("noun","man")],
    [pred("noun","dog")],
    [pred("verb","likes")],
    [pred("verb","bites")]

    ]

GOAL_3 = pred("simple_sentence","?x","?y","?z","?u","?v")

KB_4 = [
    [pred("ancestor", "?x","?y"), pred("parent","?x","?y")],
    [pred("ancestor","?x","?y"), pred("ancestor","?x","?z"), pred("parent","?z","?y")],
    [pred("parent","Mary","Paul")],
    [pred("parent","Sue","Mary")]
]

GOAL_4 = pred("ancestor","?x","?y")

KB_5 = [
    [pred("ancestor","?x","?y"), pred("ancestor","?x","?z"), pred("parent","?z","?y")],
    [pred("ancestor", "?x","?y"), pred("parent","?x","?y")],
    [pred("parent","Mary","Paul")],
    [pred("parent","Sue","Mary")]
]

GOAL_5 = pred("ancestor","?x","?y")


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

def resolve(kb, goal, mode="dfs",max_depth=300):
    print("MODE",mode)
    #print(kb)

    #print(kb)

    
    #bindings = {}
    if mode == "dfs":
        open_list = []
        open_list.append( ([goal], {}) )
    else:
        open_list = queue.Queue()
        open_list.put( ([goal], {}) )

    i=0
    #pp.pprint(open_list)
    print("----")

    successes = []

    while open_list:
        #print("LOOP",i)
        #print("OPEN LIST")

        #pp.pprint(open_list)

        kb = [uniqify(x) for x in kb]
        #print(open_list.qsize())
        #print(lst(open_list))
        if mode == "dfs":
            current_node = open_list.pop()
        else:
            #print(open_list.queue)
            if open_list.qsize() == 0:
                break
            current_node = open_list.get()
            #print(current_node)

        current_clause = current_node[0]
        current_bindings = current_node[1]

        """
        print("CURRENT CLAUSE")
        pp.pprint(current_clause)
        print("CURRENT BINDINGS")
        pp.pprint(current_bindings)
        print()
        """
        

        #to_resolve = kb[0][0]
        #print("START RESOLVING")
        for clause in kb:
            #pp.pprint(clause)
            #print(current_clause)

            #current_clause = uniqify(clause)
            #clause = uniqify(clause)
            #print(clause)
            #print(current_clause)
            to_resolve = clause[0]
            predicate = current_clause[0]
            #or predicate in current_clause:
            if can_resolve(predicate,to_resolve):
                """
                #print("RESOLVING",predicate,to_resolve)
                #print("")
                #print("RESOLVING")
                pp.pprint(predicate)
                #print("WITH")
                pp.pprint(to_resolve)
                #print("WITH BINDINGS")
                pp.pprint(current_bindings)
                """
                
                infinite_loop = False

                if infinite_loop:
                    new_clause = copy.deepcopy(clause[1:])
                    new_clause.extend(current_clause[1:])
                else:
                    new_clause = copy.deepcopy(current_clause[1:])
                    new_clause.extend(clause[1:])
                    

                #pp.pprint(clause)
               # print("RESULTING IN")
                #pp.pprint(new_clause)
                #print(clause[1:])
                #print(current_clause[1:])
                #print(new_clause)
                #print(current_bindings)
                unify_results = unify(predicate,to_resolve,current_bindings)

                #print("UNIFY RESULT",unify_results)
                #print("---------")
                
                #if unify_results == {}:
                #    print("WE DID IT REDDIT")
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
                #    print("WE REDDIT, DID IT")
                    successes.append(unify_results)
        

        #print("YEET")
        if i > max_depth:
            print("ERR: Max Depth of",str(max_depth),"Reached")
            return None
        
        i = i+1
        #input()
        #print("#################")
        #input()
        #print("############")

    #print("YEET")

    #print("HUGE SUCCESS",successes)
    
    for i,bindings in enumerate(successes):
        #print(bindings)
        print("BINDING",i)
        for var in goal["vars"]:
            b = binding(var, bindings)
            print(var,"/",b)

    return 0

def test_resolve():
    
    """
    print("RESOLVE 1")
    res = resolve(KB_1,GOAL_1,mode="bfs")
    #print(res)
    print("RESOLVE 2")
    res = resolve(KB_2,GOAL_2,mode="bfs")
    """
    
    
    #print("RESOLVE 3")
    #res = resolve(KB_3,GOAL_3)


    

    print("RESOLVE 4")
    res = resolve(KB_4,GOAL_4,mode="bfs")

    print("RESOLVE 5")
    res = resolve(KB_5,GOAL_5,mode="bfs")
    
    #print(res)
    #print(res)

def main():
    #test_resolve()
    #test_unify()
    #test_unify2()
    #test_bindings()
    #uniqify("hi")
    #test_uniqify()
    print("-----")
    test_resolve()

if __name__ == "__main__":
    main()


