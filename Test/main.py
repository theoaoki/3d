import pygame, time, Point, math, Plane, Line

#constants

PI = 3.14159265
TRANSLATE_SPEED = 0.75 #pixels(?) per frame
ROTATE_SPEED = 3 #angles per frame

#constants ended

pygame.init()
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
center = [width / 2, height / 2]
black = [0, 0, 0]
white = [255, 255, 255]
gray = [125,125,125]
lightGray = [200,200,200]
darkGray = [50,50,50]
done = False
FPS = 30 #frames per second
screenTime = int(1.0 / FPS * 1000) #in milliseconds

position = [0, 0, 0]
rotation = [0, 0]

def translate(x, y, angle):
        '''returns the change in position based on the angle of rotation of the body'''
        angle = angle * PI / 180
        cosAngle = int (math.cos(angle) * 1000) / 1000.0
        sinAngle = int (math.sin(angle) * 1000) / 1000.0
        changeInPosition = [0, 0]
        changeInPosition[0] = cosAngle*x - sinAngle*y
        changeInPosition[1] = cosAngle*y + sinAngle*x
        return changeInPosition

def sign(num):
        if num < 0:
                return -1
        else:
                return 1

def drawPoint(point):
        '''draws the point on the screen'''
        pygame.draw.circle(screen, black, point.getPositionOnScreen(position, rotation, center), 5)

def drawPlane(plane, color):
        '''draws the plane on the screen'''
        pygame.draw.polygon(screen, color, plane.getPointPositionsOnScreen())

def order(plane1, plane2):
        '''returns True if plane1 should be in front of plane2'''
        front = True
        pointList1 = plane1.getPointPositionsOnScreen()
        pointList2 = plane2.getPointPositionsOnScreen()
        rawPointList = plane1.getPoints()
        pointList = []
        planeCoordinates = plane1.getCoordinates()
        for i in range(0, len(rawPointList)):
                pointList.append([])
                for j in range(0, 3):
                        pointList[i].append(rawPointList[i].getPosition()[j] + planeCoordinates[j])
        lineList = []
        #creating lines between the points of plane2
        for i in range(0, len(pointList2)):
                if i == len(pointList2) - 1:
                        lineList.append(Line.Line(pointList2[i], pointList2[0]))
                else:
                        lineList.append(Line.Line(pointList2[i], pointList2[i + 1]))
        #cycling through all of plane1 points, seeing if any are behind plane2
        for i in range(0, len(pointList1)):
                count = 0
                ray = Line.Line([0, pointList1[i][1]], pointList1[i])
                vectorToEye = Line.Vector([center[0], 0, center[1]], [pointList[i][0] - center[0], pointList[i][1], pointList[i][2] - center[1]])
                for j in range(0, len(lineList)):
                        if Line.intersect(ray, lineList[j]):
                                count += 1

                

                if count % 2 == 1 and plane1.getDepth(i) > getIntersection(plane2, vectorToEye)[1]: 
                        front = False
                        break
        return front

def getIntersection(plane, vector):
        '''returns the POI of the plane and the vector'''
        points = plane.getPoints()
        planeCoordinates = plane.getCoordinates()
        tempVectors = []
        for i in range(0, 2):
                translation = []
                for j in range(0, 3):
                        translation.append(planeCoordinates[j] + position[j])
                tempVectors.append([points[i+1].updatePosition(translation, rotation, center)[0] - points[i].updatePosition(translation, rotation, center)[0], points[i+1].updatePosition(translation, rotation, center)[1] - points[i].updatePosition(translation, rotation, center)[1], points[i+1].updatePosition(translation, rotation, center)[2] - points[i].updatePosition(translation, rotation, center)[2]])
        n = []
        n.append(tempVectors[0][1] * tempVectors[1][2] - tempVectors[0][2] * tempVectors[1][1])
        n.append(tempVectors[0][2] * tempVectors[1][0] - tempVectors[0][0] * tempVectors[1][2])
        n.append(tempVectors[0][0] * tempVectors[1][1] - tempVectors[0][1] * tempVectors[1][0])
        
        d = n[0] * (points[0].getPosition()[0] + planeCoordinates[0]) + n[1] * (points[0].getPosition()[1] + planeCoordinates[1]) + n[2] * (points[0].getPosition()[2] + planeCoordinates[2])

        if n[0] * vector.getParameter(0) + n[1] * vector.getParameter(1) + n[2] * vector.getParameter(2) == 0:
                t = 5
        else:
                t = (d - n[0] * vector.getBase(0) - n[1] * vector.getBase(1) - n[2] * vector.getBase(2)) / float(n[0] * vector.getParameter(0) + n[1] * vector.getParameter(1) + n[2] * vector.getParameter(2))
        return [vector.getBase(0) + t * vector.getParameter(0), vector.getBase(1) + t * vector.getParameter(1), vector.getBase(2) + t * vector.getParameter(2)]
        
                                          
def draw(planeList, colourList):
        '''draws the planes in the correct order'''
        for i in range(0, len(planeList)):
                planeList[i].updatePoints(position, rotation, center)
        #ordering
        swap = False
        for i in range(0, len(planeList) - 1):
                for j in range(0, len(planeList) - 1):
                        if not order(planeList[j + 1], planeList[j]):
                                swap = True
                                hold = planeList[j+1]
                                planeList[j + 1] = planeList[j]
                                planeList[j] = hold

                                hold = colourList[j + 1]
                                colourList[j+1] = colourList[j]
                                colourList[j] = hold

                                
                if swap == False:
                        break


        #actually drawing the planes
        for i in range(0, len(planeList)):
                drawPlane(planeList[i], colourList[i])
        
        

#CREATE OBJECTS HERE

#============================================

#the following creates a cube (use to test ordering)
planes = []
planes.append(Plane.Square(center[0], 30, center[1], 10))
planes.append(Plane.Square(center[0], 40, center[1], 10))
planes.append(Plane.Square(center[0] - 5, 35, center[1], 10))
planes.append(Plane.Square(center[0] + 5, 35, center[1], 10))
planes.append(Plane.Square(center[0], 35, center[1] + 5, 10))
planes.append(Plane.Square(center[0], 35, center[1] - 5, 10))

colours = []
colours.append(black)
colours.append(black)
colours.append(lightGray)
colours.append(lightGray)
colours.append(darkGray)
colours.append(darkGray)

planes[2].rotate([90, 0, 0])
planes[3].rotate([90, 0, 0])
planes[4].rotate([0, 90, 0])
planes[5].rotate([0, 90, 0])


#============================================

#object creation done

#key variables

wDown = False
aDown = False
sDown = False
dDown = False
jDown = False
lDown = False
iDown = False
kDown = False

#key variables done

jump = False
jumpI = 0

while not done:
        startTime = int(time.time() * 1000)
        #events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            wDown = True
                
                        if event.key == pygame.K_s:
                            sDown = True
                            
                        if event.key == pygame.K_a:
                            aDown = True
                        if event.key == pygame.K_d:
                            dDown = True

                        if event.key == pygame.K_j:
                            jDown = True
                        if event.key == pygame.K_l:
                            lDown = True
                        if event.key == pygame.K_i:
                            iDown = True
                        if event.key == pygame.K_k:
                            kDown = True
                        if event.key == pygame.K_SPACE and not jump:
                            jump = True
                        if event.key == pygame.K_v:
                            position[2] += 5
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            wDown = False
                
                        if event.key == pygame.K_s:
                            sDown = False
                            
                        if event.key == pygame.K_a:
                            aDown = False
                        if event.key == pygame.K_d:
                            dDown = False

                        if event.key == pygame.K_j:
                            jDown = False
                        if event.key == pygame.K_l:
                            lDown = False
                        if event.key == pygame.K_i:
                            iDown = False
                        if event.key == pygame.K_k:
                            kDown = False
                        if event.key == pygame.K_SPACE:
                            jump = False
                            
        delta = [0, 0]
        if wDown:
            delta1 = translate(0, TRANSLATE_SPEED, rotation[0])
            delta[0] += delta1[0]
            delta[1] += delta1[1]
        if sDown:
            delta1 = translate(0, -TRANSLATE_SPEED, rotation[0])
            delta[0] += delta1[0]
            delta[1] += delta1[1]
        if aDown:
            delta1 = translate(-TRANSLATE_SPEED, 0, rotation[0])
            delta[0] += delta1[0]
            delta[1] += delta1[1]
        if dDown:
            delta1 = translate(TRANSLATE_SPEED, 0, rotation[0])
            delta[0] += delta1[0]
            delta[1] += delta1[1]

        if math.sqrt(delta[0]**2 + delta[1] ** 2) > TRANSLATE_SPEED:
                pass
        
        if jDown:
            rotation[0] += ROTATE_SPEED

        if lDown:
            rotation[0] -= ROTATE_SPEED
        if iDown:
                rotation[1] += ROTATE_SPEED
        if kDown:
                rotation[1] -= ROTATE_SPEED


        if jump:
                position[2] -= 5
                
        
        #events done

        #maintenance
        position[0] += delta[0]
        position[1] += delta[1]
        rotation[0] = rotation[0] % 360
        rotation[1] = rotation[1] % 360

        #maintenance done

        #drawing
        screen.fill(white)

        draw(planes, colours)



        pygame.display.flip()
        #drawing done


        while int(time.time() * 1000) - startTime < screenTime:
                pass

pygame.quit()
