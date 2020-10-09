import sys, math
class Matrix (object):
    '''matrix object'''
    def __init__(self, rows, columns, x=None, y=None, z=None):
        '''sets up the size of the matrix, filled with 0s'''
        self.matrix = []
        self.rows = rows
        self.columns = columns
        for i in range(0, rows):
            row = []
            for j in range(0, columns):
                row.append(0)
            self.matrix.append(row)

        if (x != None and rows >= 1):
            self.matrix[0][0] = x
            if (y != None and rows >= 2):
                self.matrix[1][0] = y
                if (z != None and rows == 3):
                    self.matrix[2][0] = z
            
    
    def setValue(self, value, row, column):
        '''changes the value at the specified index of the matrix'''
        self.matrix[row][column] = value

    def getValue(self, row, column):
        '''returns the value at the specified index of the matrix'''
        return self.matrix[row][column]

    def getRows(self):
        '''returns the amount of rows in the matrix'''
        return self.rows

    def getColumns(self):
        '''returns the amount of columns in the matrix'''
        return self.columns

    def display(self):
        '''displays the matrix'''
        sys.stdout.write("[\n")
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                sys.stdout.write(str(self.matrix[i][j]))
                if j != self.columns - 1:
                    sys.stdout.write(", ")
            sys.stdout.write("\n")
        sys.stdout.write("]\n")


#global variables
X = 0
Y = 1
Z = 2
PI = 3.14159265

def createRotationMatrix(angle, axis):
    '''returns a matrix object that describes a rotation around the specified axis'''
    mat = Matrix(3,3)
    angle = angle * PI / 180
    cosAngle = int (math.cos(angle) * 1000) / 1000.0
    sinAngle = int (math.sin(angle) * 1000) / 1000.0
    if axis == Z:
        mat.setValue(1, 2, 2)
        mat.setValue(sinAngle, 1, 0)
        mat.setValue(cosAngle, 0, 0)
        mat.setValue(-sinAngle, 0, 1)
        mat.setValue(cosAngle, 1, 1)

    elif axis == X:
        mat.setValue(1, 0, 0)
        mat.setValue(cosAngle, 2, 2)
        mat.setValue(sinAngle, 1, 2)
        mat.setValue(-sinAngle, 2, 1)
        mat.setValue(cosAngle, 1, 1)

    elif axis == Y:
        mat.setValue(1, 1, 1)
        mat.setValue(sinAngle, 2, 0)
        mat.setValue(cosAngle, 0, 0)
        mat.setValue(-sinAngle, 0, 2)
        mat.setValue(cosAngle, 2, 2)

    else:
        sys.stdout.write("Error")
        
    return mat
        
def multiply(matrix1, matrix2):
    '''returns the product of matrix multiplication'''
    if matrix1.getColumns() != matrix2.getRows():
        sys.stdout.write("Error: matrix multiplication not permitted between matrix arguments specified\n")
        return Matrix(0,0)
    else:
        product = Matrix(matrix1.getRows(), matrix2.getColumns())
        for i in range(0, product.getRows()):
            for j in range(0, product.getColumns()):
                cell = 0
                for k in range(0, matrix1.getColumns()):
                    cell += matrix1.getValue(i, k) * matrix2.getValue(k, j)
                product.setValue(cell, i, j)

        return product


