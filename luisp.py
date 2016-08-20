import sys
import traceback

def repl(prompt='<luisp> '):
    "A prompt-read-eval-print loop."
    while True:
        try:
            val = raw_input(prompt)
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
