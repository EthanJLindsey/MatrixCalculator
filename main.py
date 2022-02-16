import os
from time import perf_counter
from matrix import matrix
import constants as c

__typeErrorMessage = 'Expected {}, got {} for {}'

def timeMe(f, *args):
    start = perf_counter()
    output = f(*args)
    print(f'Seconds taken: {perf_counter() - start:.4f}')
    return output

def initargs(args):
    for i in range(0,len(args)):
        if args[i] in globals(): args[i] = globals()[args[i]]
        elif args[i].isdigit(): args[i] = int(args[i])
        else:
            m = matrix(args[i])
            if m.load(args[i]+'.txt') != 0:
                args[i] = m
                print(args[i].name)
    return args

def replaceRange(list, r1, r2, val):
    for i in range(r1, r2): list.pop(r1)
    list[r1] = val
    return list

def evaluate(list : list):
    while '^' in list:
        i = list.index('^')
        replaceRange(list, i - 1, i + 1, list[i - 1] ** list[i + 1])
    while '*' in list:
        i = list.index('*')
        replaceRange(list, i - 1, i + 1, list[i - 1] * list[i + 1])
    while '+' in list:
        i = list.index('+')
        replaceRange(list, i - 1, i + 1, list[i - 1] + list[i + 1])
    return list

def contcmd(args): return c.CONTINUE

def quitcmd(args): return c.BREAK

def helpcmd(args):
    print()
    return c.CONTINUE

def setcmd(args):
    if not len(args) > 0 or type(args[0]) is int or args[0] in commands.keys(): return c.FAIL
    globals()[args[0]] = evaluate(args[1 : len(args)])[0]
    return c.CONTINUE

def savecmd(args):
    if not len(args) > 1 or args[0] in commands.keys(): return c.FAIL
    r = evaluate(args[1 : len(args)])[0]
    with open(args[0]+'.txt','w') as f: f.write(str(r))
    return c.CONTINUE

def timecmd(args):
    return timeMe(evaluate, args)

def newcmd(args):
    if type(args[0]) == matrix:
        args[0].name(input('What is the name of this matrix?'))
        c = 1
        i = ''
        while i != n:
            i = input('Enter the '+c+'th row separated by space').split(' ')
            while args[0].rows != 0 and len(i) != args[0].rows:
                i = input('Expected input of '+args[0].columns+' columns, got '+len(i)+'. Is the matrix complete? (y/n)')
                if i == 'y' or i == 'n': continue
                print('Invalid input. Please type \'y\' for yes or \'n\' for no.')
            args[0].grid.append(i)
            args[0].columns = len(i)
        args[0].rows = c
    else: print(type(args[0]))
    return args

def removecmd(args):
    os.remove(args[0].name+'.txt')
    return c.CONTINUE


commands = {
    '' : contcmd,
    'quit': quitcmd,
    'help': helpcmd,
    'set': setcmd,
    'save' : savecmd,
    'time' : timecmd,
    'new' : newcmd,
    'remove' : removecmd
}

print('\nWelcome to my matrix application! Type \'help\' for a list of commands or \'quit\' to exit.')
def main():
    while True:
        args = input("$ ").split(' ') # command input
        initargs(args)

        if args[0] not in commands.keys(): args = evaluate(args)
        else:
            if callable(commands[args[0]]): args = commands[args[0]](args[1 : len(args)])
            if args == c.BREAK : break
            if args == c.CONTINUE : continue
        for arg in args: print(arg, end=' ')
        print()

if __name__ == '__main__':
    main()