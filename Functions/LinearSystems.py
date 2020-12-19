import sys
from sympy import *
import numpy as np
import json

class output_data:
    Error=""
    Result=""
    Axe1name="axe1"
    Axe2name="axe2"
    Values=[] #list of named_series .venv\scripts\activate

    def __init__(self):
        self.Error = ""
        self.Result = ""
        self.Axe1name=""
        self.Axe2name=""
        self.Values = []

    def to_json(self):
        s = '{"Error":"'+str(self.Error).replace('\n', '\\n')+'", "Axe1Name": "'+self.Axe1name+'", "Axe2Name": "'+self.Axe2name+'", "Result":"'+str(self.Result).replace('\n', '\\n')+'", "Values":['
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


def function(func, out):
    try:
        syst = "".join(func.split())
        syped_eq = sympify_system(syst)
        solution = solve(syped_eq)

        if len(solution) == 0:
            out.Result = "No solution"
            return

        out.Result = solution

        if len(solution) > 2:
            return

        if len(solution) == 1:
            ser = lindependent_series(solution, syped_eq)
            out.Values.append(ser)
            return

        solution_series = independent_series(solution, syped_eq, out)

        out.Values.append(solution_series[0])
        out.Values.append(solution_series[1])
    except:
        out.Error = "Bad Input!"
    return

def sympify_system(system):
    equations = system.split(";")
    syped_eq = []
    for i in range(0, len(equations)):
        temp = equations[i].split("=")
        syped_eq.append(sympify("Eq("+temp[0]+", "+temp[1]+")"))
    return syped_eq

def lindependent_series(solution, sypified_syst):
    x = list(solution.items())[0][0]
    sol = solve(sypified_syst[0], x)
    yValues = np.arange(-10, 10.01, 10)
    y = symbols("y")
    g = lambdify(y, sol[0], "numpy")
    xValues = g(yValues)
    series = named_series("Straight", xValues.tolist(), yValues.tolist())
    return series

def independent_series(solution, sypified_syst, out):
    x = list(solution.items())[0][0]
    y = list(solution.items())[1][0]

    out.Axe1name=str(x)
    out.Axe2name=str(y)

    y_sol_one = solve(sypified_syst[0], y)
    y_sol_two = solve(sypified_syst[1], y)
    x_sol_one = solve(sypified_syst[0], x)
    x_sol_two = solve(sypified_syst[1], x)

    xValues = np.arange(solution.get(x).evalf()-10, solution.get(x).evalf()+10.01, 20)
    sameXValues = (solution.get(x).evalf(), solution.get(x).evalf())

    yValues = (solution.get(y).evalf()-10, solution.get(y).evalf()+10)
    sameYValues = (solution.get(y).evalf(), solution.get(y).evalf())

    ser1 = []
    ser2 = []

    if (len(y_sol_one) == 0 and (len(y_sol_two) > 0 and len(x_sol_two) > 0)):   
        g = lambdify(x, solve(sypified_syst[1], y)[0], "numpy")
        zValues = g(xValues)
        ser1 = named_series("1st straight", sameXValues, yValues)
        ser2 = named_series("2nd straight", xValues, zValues.tolist())
    elif (len(y_sol_one) > 0 and len(x_sol_one) > 0) and len(y_sol_two) == 0:
        f = lambdify(x, solve(sypified_syst[0], y)[0], "numpy")
        zValues = f(xValues)
        ser1 = named_series("1st straight", xValues, zValues.tolist())
        ser2 = named_series("2nd straight", sameXValues, yValues)
    elif len(x_sol_one) == 0 and ((len(y_sol_two) > 0 and len(x_sol_two) > 0)):
        f = lambdify(x, solve(sypified_syst[1], y)[0], "numpy")
        zValues = f(xValues)
        ser1 = named_series("1st straight", xValues, sameYValues)
        ser2 = named_series("2nd straight", xValues, zValues.tolist())
    elif (len(y_sol_one) > 0 and len(x_sol_one) > 0) and len(x_sol_two) == 0:
        g = lambdify(x, solve(sypified_syst[0], y)[0], "numpy")
        zValues = g(xValues)
        ser1 = named_series("1st straight", xValues, zValues.tolist())
        ser2 = named_series("2nd straight", xValues, sameYValues) 
    elif (len(y_sol_one) > 0 and len(x_sol_two) > 0) and (len(x_sol_one) == 0 and len(y_sol_two) == 0):
        ser1 = named_series("1st straight", (solution.get(x).evalf()-10, solution.get(x).evalf()+10), sameYValues)
        ser2 = named_series("2nd straight", sameXValues, yValues)
    elif (len(y_sol_two) > 0 and len(x_sol_one) > 0) and (len(x_sol_two) == 0 and len(y_sol_one) == 0):
        ser1 = named_series("1st straight", sameXValues, yValues)
        ser2 = named_series("2nd straight", (solution.get(x).evalf()-10,solution.get(x).evalf()+10), sameYValues)
    else:
        f = lambdify(x, solve(sypified_syst[0], y)[0], "numpy")
        g = lambdify(x, solve(sypified_syst[1], y)[0], "numpy")
        iValues = f(xValues)
        zValues = g(xValues)
        ser1 = named_series("1st straight", xValues, iValues.tolist())
        ser2 = named_series("2nd straight", xValues, zValues.tolist())
    return (ser1, ser2)

def info():
    return """
    Find solution to a linear system
    If system rank is 2 also draws graph 

    Examples: 
    'x + 2*y = 10; 3*x + 2*y + z = 23; y + 2*z = 13'  
    '2*x + 3*y = 5; 3*x + 2*y = 3'
    """

mode = sys.argv[1]
# mode = 'v'

output = output_data()
if (mode == 'info'):
    output.Result=info()
else:
    data = ' '.join(sys.argv[2:])
    # data = '2*x + y = 5; 2*x + y = 5'
    # data = '2*x + 3*y = 5; 3*x + 2*y = 3'
    # data = 'x = 2'
    function(data, output)

l = output.to_json()
print(l)
# print(json.loads(l))