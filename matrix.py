import os

class matrix(object):
    grid = []
    name = ''
    rows = 0
    columns = 0
    
    def __init__(self, name, rows = 0, columns = 0):
        self.name = name
        self.rows = rows
        self.columns = columns
        self.grid = []
    
    def __str__(self) -> str:
        if len(self.grid) == 0: return ''
        maxfront = len(str(self.grid[0][0]).split('.')[0])
        maxback = len(str(self.grid[0][0]).split('.')[1])
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if len(str(self.grid[i][j]).split('.')[0]) >= maxfront: maxfront = len(str(self.grid[i][j]).split('.')[0])
                if len(str(self.grid[i][j]).split('.')[1]) >= maxback: maxback = len(str(self.grid[i][j]).split('.')[1])
        s = ''
        for i in range(0,self.rows):
            d = ' '
            for j in range(0,self.columns):
                if j >= self.columns - 1:
                    if i >= self.columns - 1: d = ''
                    else: d = '\n'
                s += f'{self.grid[i][j]:{maxfront:d}.{maxback:d}f}'+d
        return s
    
    def __add__(self, o):
        if type(o) is matrix:
            r = matrix(self.name+'+'+o.name, self.rows, self.columns)
            for i in range(0,self.rows):
                for j in range(0,self.columns):
                    r = self.grid[i][j] + o.grid[i][j]
            return r
        elif type(o) is int:
            r = matrix(self.name+'+'+str(o), self.rows, self.columns)
            r.grid = [list(map(lambda x: o + x, l)) for l in self.grid]
            return r

    def __radd__(self,o):
        r = self.__add__(o)
        r.name = str(o)+'+'+self.name
        return r       

    def __mul__(self, o):
        if type(o) is matrix:
            if self.columns != o.rows: return 0
            r = matrix(self.name+'*'+o.name, self.rows, o.columns)
            for i in range(0,self.rows):
                r.grid.append([])
                for j in range(0,o.columns):
                    element = 0.0
                    for k in range(0,o.rows): element += self.grid[i][k]*o.grid[k][j]
                    r.grid[i].append(round(element, 10))
            return r
        elif type(o) is int:
            r = matrix(self.name+'*'+str(o), self.rows, self.columns)
            r.grid = [list(map(lambda x: o*x, l)) for l in self.grid]
            return r
        else:
            print('none type')
            return None

    def __rmul__(self, o):
        r = self.__mul__(o)
        r.name = str(o)+'*'+self.name
        return r

    def __pow__(self, p):
        if type(p) is not int or self.rows != self.columns or p < 1: return 0
        n = self.name+'^'+str(p)
        while p & 1 != 1:
            self = self * self
            p >>= 1
        r = self
        while p > 0:
            p >>= 1
            self = self * self
            if p & 1 == 1:
                r = r * self
        r.name = n
        return r

    def load(self, file):
        if not os.path.exists(file): return 0
        with open(file, "r") as f:
            self.grid = f.read().split('\n')
            self.rows = len(self.grid)
            for i in range(0,self.rows): self.grid[i] = self.grid[i].split()
            self.columns = len(self.grid[0])
            for i in range(0,self.rows):
                for j in range(0,self.columns):
                    self.grid[i][j] = float(self.grid[i][j])
        return 1
