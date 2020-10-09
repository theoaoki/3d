import Matrix, math

OPTICAL_DISTANCE = 500
PIXELS_PER_METER = 1 #bring this in somehow

def getHypotenuse(a, b):
    '''returns the hypotenuse determined by a right angled triangle with sides a and b'''
    return math.sqrt(a**2 + b**2)

def getRelativeLength(absoluteLength, distance, opticalDistance):
    '''returns the distance as seen by the eye of a length at a certain distance'''
    if distance == 0:
        return -10000 #this causes weird graphics
    return absoluteLength * opticalDistance / distance

class Point (object) :
    '''wrapper for a vector in three-space'''
    def __init__(self, x, y, z):
        '''sets coordinates for the point'''
        self.x = x
        self.y = y
        self.z = z
        self.vector = Matrix.Matrix(3, 1, x, y, z)

    def setPosition(self, x, y, z):
        '''sets coordinates for the point'''
        self.x = x
        self.y = y
        self.z = z

    def applyMatrix(self, matrix):
        '''applies a matrix to the point'''
        self.vector.setValue(self.x, 0, 0)
        self.vector.setValue(self.y, 1, 0)
        self.vector.setValue(self.z, 2, 0)
        self.vector = Matrix.multiply(matrix, self.vector)
        self.x = self.vector.getValue(0, 0)
        self.y = self.vector.getValue(1, 0)
        self.z = self.vector.getValue(2, 0)
        

    def getPosition(self):
        '''returns the coordinates for the point'''
        return [self.x, self.y, self.z]

    def updatePosition(self, translation, rotation, center):
        '''changes the vector of the point in three-space to reflect the translation and rotation specified, returns the vector as a list'''
        self.vector.setValue(self.x - translation[0] - center[0], 0, 0)
        self.vector.setValue(self.y - translation[1], 1, 0)
        self.vector.setValue(self.z - translation[2] - center[1], 2, 0)
        mat = Matrix.createRotationMatrix(-rotation[0], 2)
        self.vector = Matrix.multiply(mat, self.vector)
        self.vector.setValue(self.vector.getValue(0,0) + center[0], 0, 0)
        self.vector.setValue(self.vector.getValue(2,0) + center[1], 2, 0)
        return [self.vector.getValue(0,0), self.vector.getValue(1,0), self.vector.getValue(2,0)]

    def getPositionOnScreen(self, translation, rotation, center): #change function name
        '''returns the point on the screen based on the translation and rotation of the viewer from the origin'''
        self.vector.setValue(self.x - translation[0] - center[0], 0, 0)
        self.vector.setValue(self.y - translation[1], 1, 0)
        self.vector.setValue(self.z - translation[2] - center[1], 2, 0)
        mat = Matrix.multiply(Matrix.createRotationMatrix(-rotation[1], 0), Matrix.createRotationMatrix(-rotation[0], 2))
        self.vector = Matrix.multiply(mat, self.vector)
        if self.vector.getValue(1, 0) < 0:
            return [-1, -1]
        else:
            #self.vector.setValue(getRelativeLength(self.vector.getValue(2,0) - center[1], getHypotenuse(self.vector.getValue(1,0), self.vector.getValue(0,0) - center[0]), OPTICAL_DISTANCE) + center[1], 2, 0)
            self.vector.setValue(getRelativeLength(self.vector.getValue(2,0), self.vector.getValue(1,0), OPTICAL_DISTANCE) + center[1], 2, 0)
            self.vector.setValue(getRelativeLength(self.vector.getValue(0,0), self.vector.getValue(1,0), OPTICAL_DISTANCE) + center[0], 0, 0)
            return [int(self.vector.getValue(0,0)), int(self.vector.getValue(2,0))]

        
    def getDepth(self):
        '''returns the y-value of the vector'''
        return self.vector.getValue(1,0)
    

    
