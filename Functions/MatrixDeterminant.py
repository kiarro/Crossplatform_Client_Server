import sys
import numpy
import json

class output_data:
    Error=""
    Result=""
    Values=[] #list of named_series

    def to_json(self):
        s = '{"Error":"'+str(self.Error).replace('\n', '\\n')+'", "Result":"'+str(self.Result).replace('\n', '\\n')+'", "Values":'+str(self.Values)+"}"
        return s;

class named_series:
    Name=""
    Series=[]

class point:
    X = 0.0
    Y = 0.0




def function(s):
    matrix = numpy.matrix(s)
    res = numpy.linalg.det(matrix)
    return str(round(res, 5))

def info():
    return """
    Count matrix determinant. Matrix must be square form.
    
    Input: string represent matrix
    Example: \'[1 3.2 66; 10.11 2.4 4; 13.409 18.009 9]\'

    Output: one number
    """

mode = sys.argv[1]
# mode = 'v'
output = output_data()
if (mode == 'info'):
    output.Result=info()
else:
    data = ' '.join(sys.argv[2:])
    # data='[1 2; 2 0]'
    output.Result=function(data)

print(output.to_json())
