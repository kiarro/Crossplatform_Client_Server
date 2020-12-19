import sys
from sympy import *
import numpy as np
import json

class output_data:
    Error=""
    Result=""
    Values=[] #list of named_series

    def __init__(self):
        self.Error = ""
        self.Result = ""
        self.Values = []

    def to_json(self):
        s = '{"Error":"'+str(self.Error).replace('\n', '\\n')+'", "Result":"'+str(self.Result).replace('\n', '\\n')+'", "Values":['
        s += ','.join(list(map(named_series.to_json, self.Values)))
        s += "]}"
        return s;

class named_series:
    Name=""
    Series=[]

    def __init__(self, name, xs, ys):
        self.Name = name
        if (len(xs)!=len(ys)): raise Exception('values', 'different length')
        self.Series = []
        for i in range(len(xs)):
            self.Series.append(point(xs[i], ys[i]))

    def to_json(self):
        s = '{"Name":"'+self.Name+'", "Series":['+','.join(list(map(point.to_json, self.Series)))+']}'
        return s

class point:
    X = 0.0
    Y = 0.0

    def __init__(self, x, y):
        self.X=x
        self.Y=y

    def to_json(self):
        s = '{"X":'+str(self.X)+', "Y":'+str(self.Y)+'}'
        return s

    def __repr__(self):
        return self.to_json()


def function(input, out):
    x=symbols("x")
    expr = sympify(input)
    # print(expr)
    out.Result = expr
    xValues = np.arange(10)
    f = lambdify(x, expr, "numpy")
    g = lambdify(x, diff(expr), "numpy")
    yValues = f(xValues)
    zValues = g(xValues)
    # print([xValues, yValues])
    # print([xValues, zValues])
    ser1 = named_series("normal", xValues.tolist(), yValues.tolist())
    ser2 = named_series("diff", xValues.tolist(), zValues.tolist())
    # print(ser1.Series)
    # print(ser1.to_json())
    # print(ser2.to_json())
    out.Values.append(ser1)
    out.Values.append(ser2)
    return

def info():
    return """
    Find differential

    Create two plots. 
    """

mode = sys.argv[1]
# mode = 'v'

output = output_data()
if (mode == 'info'):
    output.Result=info()
else:
    data = ' '.join(sys.argv[2:])
    # data = 'sin(x)'
    function(data, output)

l = output.to_json()
print(l)
# print(json.loads(l))
    
