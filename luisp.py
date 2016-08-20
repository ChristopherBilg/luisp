import sys
import traceback

Symbol = str

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

def repl(prompt='<luisp> '):
    "A prompt-read-eval-print loop."
    while True:
        try:
            val = parse(raw_input(prompt))
            if val is not None:
                print val
        except KeyboardInterrupt:
            print "\nExiting luisp\n"
            sys.exit();
        except:
            handle_error()

def handle_error():
    print "Oops! Well, at least there's a Python stack trace:\n"
    traceback.print_exc()

repl()
