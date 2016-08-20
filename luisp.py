import sys
import traceback

Symbol = str
isa = isinstance

class Env(dict):
    "An environment: a dict of {'var': val} pairs with an outer Env."

    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        return self if var in self else self.outer.find(var)

def parse(s):
    "Parse a Luisp expression from a string."
    return read_from(tokenize(s))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

def read_from(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        tokens.pop(0) # pop off the ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    if not isa(exp, list):
        return str(exp)
    else:
        return "(" + " ".join(map(to_string, exp)) + ")"

def repl(prompt='<luisp> '):
    "A prompt-read-eval-print loop."
    while True:
        try:
            val = parse(raw_input(prompt))
            if val is not None:
                print to_string(val)
        except KeyboardInterrupt:
            print "\nExiting luisp\n"
            sys.exit();
        except:
            handle_error()

def handle_error():
    print "Oops! Well, at least there's a Python stack trace:\n"
    traceback.print_exc()

repl()
