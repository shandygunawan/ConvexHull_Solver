"""========================
          IMPORTS
========================"""
from termcolor import colored
import math
import matplotlib.pyplot as pyplot
import random
import time

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

def quick_hull(Points, po, pn):
    # get the left points of a given line(po-pn)
    left_points = get_left_points(po,pn,Points)

    # get the farthest point of the left side of a given line
    pmax = search_farthest_point(po,pn,left_points)

    # If there is no more point, pn is a Hull points
    if(pmax == None):
        return [pn]

    # Recursively search the left and right side of the triangle
    upper_points = quick_hull(left_points, po, pmax)
    lower_points = quick_hull(left_points, pmax, pn)
    return (upper_points+lower_points)

"""========================
           MISC
========================"""
def init_points(list, n):
    for i in range(n):
        x = random.randint(1,100)
        y = random.randint(1,100)
        list.append((x,y))

def printListOfPoint(list, type):
    print("="*22 + "="*len(type))
    print("    List of {} Points    ".format(type))
    print("="*22 + "="*len(type))
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

    # THE COLOR HIGHLIGHTS ONLY WORKS FOR LINUX TERMINAL AND PYCHARM CONSOLE
    print(colored("=====================", "blue"))
    print(colored(" CONVEX HULL SOLVER  ", "red"))
    print(colored("=====================", "blue"))

    # Enter the number of points
    PointCount = int(input("Enter the number of points : "))

    if PointCount <= 1 :
        print("")
        print(colored("There is no Convex Hull for <= 1 point", "red"))
    else:
        # Randomize x and y for each points and append to list
        init_points(Points,PointCount)

        # sort points in list ascending based on attribute x,y
        Points.sort(key=lambda point: (point[0], point[1]))

        # Start time
        start_timer = time.clock()

        # search convex hull with quick hull
        # use line's orientation to scan left and right points
        upper_points = quick_hull(Points, Points[0], Points[-1]) # upper convex hull
        lower_points = quick_hull(Points, Points[-1], Points[0]) # lower convex hull
        HullPoints = upper_points + lower_points

        # Stop timer
        stop_timer = time.clock()

        # calculate the time for quick hull execution
        diff_time = stop_timer - start_timer

        # print Hull points' coordinate to screen
        print("")
        printListOfPoint(HullPoints, "Hull")
        print("The Convex Hull is found by {} milisecond(s)".format(str(round(diff_time*1000,5))))

        # draw convex hull to the screen
        draw_convex(HullPoints, Points)