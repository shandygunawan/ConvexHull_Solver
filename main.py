"""========================
          IMPORTS
========================"""
import math
import matplotlib.pyplot as pyplot
import random

"""========================
          GLOBAL
========================"""
# Global Variable
Points = [] # list to store points
HullPoints = [] # list to store hull points

"""========================
           SOLVE
========================"""

# used to determine if a point is on the left/right of a line
# det > 0 -> left of line
# det < 0 -> right of line
def determinant_sarrus(p1,p2,p3):
    x1 = p1[0]
    x2 = p2[0]
    x3 = p3[0]
    y1 = p1[1]
    y2 = p2[1]
    y3 = p3[1]
    return( (x1*y2) + (x3*y1) + (x2*y3) - (x3*y2) - (x2*y1) - (x1*y3) )

# return the value of a, b, and c from ax+by+c = 0
def line_equation(p1,p2):
    return (p2[1]-p1[1]),(p1[0]-p2[0]),((p2[0])*(p1[1]) - (p1[0])*(p2[1]))

# return the distance of a given point to a line
def distance_point_line(P,a,b,c):
    try:
        return ( (abs((a*P[0]) + (b*P[1]) + c))/(math.sqrt( (a*a) + (b*b) )) )
    except:
        return 0

# return the degree of a point to a line using vector operation
# a.b = |a| |b| cos(theta)
def degree_vector(p1,p2,p3):
    v1 = (p3[0]-p1[0], p3[1]-p1[1])
    v2 = (p3[0]-p2[0], p3[1]-p2[1])
    dot = (v1[0]*v2[0]) + (v1[1]*v2[1])
    cardinal_v1 = math.sqrt( (v1[0]*v1[0]) + (v1[1]*v1[1]) )
    cardinal_v2 = math.sqrt( (v2[0]*v2[0]) + (v2[1]*v2[1]) )
    try:
        return math.degrees(math.acos(dot/(cardinal_v1*cardinal_v2)))
    except:
        return 0

# search the farthest point from a given side(left/right) to a line
def search_farthest_point(po,pn,list):
    # determine the line equation
    a,b,c = line_equation(po,pn)
    distanceMax = 0
    pmax = None

    for point in list:
        if(distance_point_line(point,a,b,c) > distanceMax):
            distanceMax = distance_point_line(point,a,b,c)
            pmax = point

    return pmax

# get the points located left of a given line
def get_left_points(po,pn,list):
    left_points = []
    for point in list:
        if(determinant_sarrus(po,pn,point) > 0):
            left_points.append(point)

    return left_points

# get the points located right of a given line
def get_right_points(po,pn,list):
    right_points = []
    for point in list:
        if (determinant_sarrus(po, pn, point) < 0):
            right_points.append(point)

    return right_points


def quick_hull(Points, po, pn):
    left_points = get_left_points(po,pn,Points)
    pmax = search_farthest_point(po,pn,left_points)
    if(pmax == None):
        return [pn]
    ListHull = quick_hull(left_points, po, pmax)
    ListHull = ListHull + quick_hull(left_points, pmax, pn)
    return ListHull

"""========================
           PRINT
========================"""
def printListOfPoint(list):
    print("===========================")
    print("    List of Hull Points    ")
    print("===========================")
    for i in range(len(list)):
        print("{:5} | {:1} : {:2}".format(i+1, "X",list[i][0]))
        print("{:5} | {:1} : {:2}".format(" ","Y",list[i][1]))
        print("-"*15)

# draw the convex hull to the screen
def draw_convex(listHull, listPoints):

    # Tuples unpacking
    x1,y1 = zip(*listHull)
    x2,y2 = zip(*listPoints)

    # random colors for ordinary points
    color = ['m','g','b', 'y', 'k']

    pyplot.scatter(x2,y2, c=color) # Scatter ordinary points in blue
    pyplot.scatter(x1,y1, c='r') # Scatter Hull points in red

    # Make lines between hull points
    for i in range(len(listHull)):
        if(i+1 == len(listHull)): # edge case (end of list, make line back to the first element)
            x1, x2 = listHull[i][0], listHull[0][0]
            y1, y2 = listHull[i][1], listHull[0][1]
            pyplot.plot([x1, x2], [y1, y2], 'r')
        else:
            x1, x2 = listHull[i][0], listHull[i+1][0]
            y1, y2 = listHull[i][1], listHull[i+1][1]
            pyplot.plot([x1,x2],[y1,y2], 'r')

    # show coordinates
    pyplot.grid(color='tab:gray', linestyle='--', linewidth=1) # add grid to coordinates
    pyplot.show()

"""========================
          MAIN
========================"""
if __name__ == "__main__":

    # Enter the number of points
    PointCount = int(input("Enter the number of points : "))

    # Randomize x and y for each points and append to list
    for i in range(PointCount):
        x = random.randint(1,100)
        y = random.randint(1,100)
        entry = (x,y)
        Points.append(entry)

    # sort points in list ascending based on attribute x,y
    Points.sort(key=lambda point: (point[0], point[1]))

    # search convex hull with quick hull
    HullPoints = quick_hull(Points, Points[0], Points[-1]) # upper convex hull
    HullPoints = HullPoints + quick_hull(Points, Points[-1], Points[0]) # lower convex hull

    # print Hull points' coordinate to screen
    printListOfPoint(HullPoints)
    print("")

    # draw convex hull to the screen
    draw_convex(HullPoints, Points)