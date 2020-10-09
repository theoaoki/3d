import Point, Matrix

class Plane (object):
    '''wrapper for a collection of points'''
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.points = []
        self.pointPositions = []

    def addPoint(self, point):
        '''adds a point to the plane'''
        self.points.append(point)
        self.pointPositions.append(0)

    def updatePoints(self, translation, rotation, center):
        '''updates the positions of the points on the screen'''
        for i in range(0, len(self.points)):
            originalPosition = self.points[i].getPosition()
            self.points[i].setPosition(self.x + originalPosition[0], self.y + originalPosition[1], self.z + originalPosition[2])
            
            self.pointPositions[i] = self.points[i].getPositionOnScreen(translation, rotation, center)
            self.points[i].setPosition(originalPosition[0], originalPosition[1], originalPosition[2])

    def getPoints(self):
        '''returns the points of the plane'''
        return self.points

    def getCoordinates(self):
        '''returns the center point of the plane'''
        return [self.x, self.y, self.z]

    def getPointPositionsOnScreen(self):
        '''returns the positions of the points on the screen'''
        return self.pointPositions

    def rotate(self, rotation):
        '''rotates the plane by the specified angle, where rotation is a list of rotations [Z,X,Y]'''
        R1 = Matrix.createRotationMatrix(rotation[0], 2)
        R2 = Matrix.multiply(Matrix.createRotationMatrix(rotation[1], 0), R1)
        R3 = Matrix.multiply(Matrix.createRotationMatrix(rotation[2], 1), R2)
        for i in range(0, len(self.points)):
            self.points[i].applyMatrix(R3)

    def getDepth(self, index):
        '''returns the y-value of the point at the given index'''
        return self.points[index].getDepth()


class Square(Plane):
    '''a square Plane object'''
    def __init__(self, x, y, z, width):
        '''defines the points in the plane'''
        Plane.__init__(self, x, y, z)
        self.addPoint(Point.Point(-width/2, 0, width/2))
        self.addPoint(Point.Point(width/2,0,width/2))
        self.addPoint(Point.Point(width/2,0,-width/2))
        self.addPoint(Point.Point(-width/2,0,-width/2))
        
        
        
