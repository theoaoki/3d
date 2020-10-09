#Global Variables
X = 0
Y = 1

class Line (object):
    def __init__(self, point1, point2):
        '''sets up a line by defining the endpoints'''
        self.points = []
        if point1[X] <= point2[X]:
            self.points = [point1, point2]
        else:
            self.points = [point2, point2]
        if point1[X] != point2[X]:
            self.slope = float(point2[Y] - point1[Y]) / (point2[X] - point1[X])
            self.b = point1[Y] - self.slope * point1[X]
        else:
            self.slope = None
            self.b = None
            if point2[Y] < point1[Y]:
                self.points[0] = point2
                self.points[1] = point1

class Vector (object):
    def __init__(self, base, parameters):
        '''sets up a vector for use with parameterization'''
        self.base = base
        self.parameters = parameters

    def getParameter(self, index):
        '''returns the parameter at the given index'''
        return self.parameters[index]

    def getBase(self, index):
        '''returns the base at the given index'''
        return self.base[index]
        

def intersect(line1, line2):
    '''returns true if the lines have a unique intersection'''
    if line1.slope != None and line2.slope == None:
        hold = line2
        line2 = line1
        line1 = hold
    if line1.slope == None and line2.slope == None:
        return False
    elif line1.slope == None:
        x = line1.points[0][X]
        if x > line2.points[0][X] and x < line2.points[1][X]:
            y = line2.slope * x + line2.b
            if y > line1.points[0][Y] and y < line1.points[1][Y]:
                return True
    elif line1.slope == 0 and line2.slope == 0:
        return False
    else:
        x = (line2.b - line1.b) / (line1.slope - line2.slope)
        if x > line1.points[0][X] and x < line1.points[1][X] and x > line2.points[0][X] and x < line2.points[1][X]:
            return True
        else:
            return False

