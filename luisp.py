#!/usr/bin/env python2
import readline
import sys
import traceback

isa = isinstance

class Symbol(str):
    pass

class UndefinedSymbol(Exception):
    def __init__(self, symbol_name):
        self.symbol_name = symbol_name

    def __str__(self):
        return repr(self.symbol_name)

class Env(dict):
    "An environment: a dict of {'var': val} pairs with an outer Env."

    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer:
            return self.outer.find(var)
        else:
            raise KeyError(var)

def add_globals(env):
    "Add some built-in procedures and variables to the environment."
    import math
    import operator
    env.update({
        '+': lambda *args: reduce(operator.add, args),
        '-': lambda *args: operator.sub(0, *args) if len(args) == 1 else operator.sub(*args),
        '*': operator.mul,
        '/': operator.div,
        '<': operator.lt,
        '>': operator.gt,
        'sqrt': math.sqrt
    })
    env.update({'True': True, 'False': False})
    return env

global_env = add_globals(Env())

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
    import re
    "Numbers become numbers; every other token is a symbol."
    try:
        # check for quoted string regex
        match = re.compile("\"(.*)\"").match(token)
        if match:
            string_group, = match.groups()
            return str(string_group)
        else:
            return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    if type(exp) == str:
        return '"%s"' % exp
    elif isa(exp, list):
        return "(" + " ".join(map(to_string, exp)) + ")"
    else:
        return str(exp)

def eval(x, env=global_env):
    "Evaluate an expression in an environment"
    if isinstance(x, Symbol):   # variable reference
        try:
            return env.find(x)[x]
        except KeyError as e:
            raise UndefinedSymbol(x)
    elif not isinstance(x, list):   # constant literal
        return x
    elif x[0] == 'quote' or x[0] == 'q': # (quote exp), or (q exp)
        (_, exp) = x
        return exp
    elif x[0] == 'atom?': # (atom? exp)
        (_, exp) = x
        return not isinstance(eval(exp, env), list)
    elif x[0] == 'eq?': # (eq? exp1 exp2)
        (_, exp1, exp2) = x
        v1, v2 = eval(exp1, env), eval(exp2, env)
        return (not isinstance(v1, list)) and (v1 == v2)
    elif x[0] == 'car': # (car exp)
        (_, exp) = x
        return eval(exp, env)[0]
    elif x[0] == 'cdr': # (cdr exp)
        (_, exp) = x
        return eval(exp, env)[1:]
    elif x[0] == 'cons': # (cons exp1 exp2)
        (_, exp1, exp2) = x
        # Copy the list
        lis = eval(exp2, env)[:]
        lis.insert(0, eval(exp1, env))
        return lis
    elif x[0] == 'define':
        (_, exp, val) = x
        env[exp] = eval(val, env)
        return None
    elif x[0] == 'lambda': # (lambda (x) (+ x  1))
        (_, arguments, exp) = x
        return lambda *args: eval(exp, Env(arguments, args, outer=env))
    elif x[0] == 'if':
        (_, cond, if_exp, else_exp) = x
        if eval(cond, env):
            return eval(if_exp, env)
        else:
            return eval(else_exp, env)
    elif x[0] == 'cond':
        x.pop(0)
        for exp in x:
            cond, cond_exp = exp
            if eval(cond, env):
                return eval(cond_exp, env)
    elif x[0] == 'conc':
        x.pop(0)
        val = None
        for exp in x:
            if not val:
                val = eval(exp, env)
            else:
                val = val + eval(exp, env)
        return val
    elif x[0] == 'null?':
        (_, exp) = x
        return eval(exp, env) == []
    else:   # (proc exp*)
        exps = [eval(exp, env) for exp in x]
        proc = exps.pop(0)
        return proc(*exps)

def repl(prompt='<luisp> '):
    "A prompt-read-eval-print loop."
    while True:
        try:
            val = eval(parse(raw_input(prompt)))
            if val is not None:
                print to_string(val)
        except KeyboardInterrupt:
            print "\nExiting luisp\n"
            sys.exit();
        except UndefinedSymbol as e:
            print "Undefined symbol: %s" % e
        except:
            handle_error()

def handle_error():
    print "Oops! Well, at least there's a Python stack trace:\n"
    traceback.print_exc()

def load(filename):
    print "Loading and executing %s" % filename
    f = open(filename, "r")
    program = f.readlines()
    f.close()
    line_number = 0
    for line in program:
        line_number += 1
        if not line or line == '\n':
            continue
        try:
            val = eval(parse(line))
            if val is not None:
                print to_string(val)
        except Exception as e:
            print "Error %s on line %d" % (e, line_number)
            handle_error()

# For CLI
if __name__ == "__main__":
    if len(sys.argv) > 1:
        load(sys.argv[1])
        repl()
    else:
        repl()
