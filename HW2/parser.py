#Stolen from
#https://norvig.com/lispy.html

Symbol = str              # A Scheme Symbol is implemented as a Python str
Number = (int, float)     # A Scheme Number is implemented as a Python int or float
Atom   = (Symbol, Number) # A Scheme Atom is a Symbol or Number
List   = list             # A Scheme List is implemented as a Python list
Exp    = (Atom, List)     # A Scheme expression is an Atom or List
Env    = dict             # A Scheme environment (defined below) 
                          # is a mapping of {variable: value}
                          

def tokenize(chars: str) -> list:
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program: str) -> Exp:
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens: list) -> Exp:
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)


    #res = [convert(l) for l in res]
    #print(res)



#print(parse_parentheses('a(b(cd)f)')) # ['a', ['b', ['c', 'd'], 'f']]

def pred(name, var_list):
    return {
        "name": name,
        "vars": var_list
    }

def lst_to_pred(lst):
    name = lst[0]
    v = lst[1:]
    return pred(name,v)


def parse_file(filename):
    f = open(filename)
    a = f.read()
    f.close()

    a = a.split("\n\n")  

    
        
    kb_parse = parse(a[0])
    kb_name = kb_parse[1]
    kb = kb_parse[3:][0]

    CLAUSES = []
    for clause in kb:
        current_clause = [lst_to_pred(x) for x in clause]
        CLAUSES.append(current_clause)

    goal = lst_to_pred(parse(a[1])[3][0])

    return CLAUSES, goal, kb_name

    #print(CLAUSES)
        #print(clause)  

