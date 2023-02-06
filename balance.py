from functools import reduce
from operator import mul
import sqlcplants
import tkinter as tk
import math

# .find_all() #Returns a list of the object ID numbers for all objects on the canvas, from lowest to highest.
# .find_withtag(tagOrId) #Returns a list of the object IDs of the object or objects specified by tagOrId.
# .move(tagOrId, xAmount, yAmount) #Moves the items specified by tagOrId by adding xAmount to their x coordinates and yAmount to their y coordinates.

def moveIcons(linkList,canvas): # Returns a list of lists. Each element contains primary, companion and strength of a link
    #movementsList = []
    #while True:
    #for k in range (15):
        count = 0
        for i in range(len(linkList)):
            primary = linkList[i].primary
            companion = linkList[i].companion
            strenght = linkList[i].strength
            names1 = sqlcplants.getNodeNamesFromIds([primary])
            names2 = sqlcplants.getNodeNamesFromIds([companion])
            name1 = names1[0].replace(" ", "_")
            name2 = names2[0].replace(" ", "_")
            #print("names:",names1,names2)
            x, y = getCoordsOfIcon(name1,canvas)
            x1, y1 = getCoordsOfIcon(name2,canvas)
            xAmount, yAmount = getDeltaMove(x, y, x1, y1, strenght, 3)
            if isNotMovableX(x,canvas):
                xAmount = 0
            if isNotMovableY(y,canvas):
                yAmount = 0
            #print("Moving",names1,xAmount,yAmount)
            canvas.move(name1, xAmount, yAmount)
            canvas.update_idletasks()
            count = count + abs(xAmount) + abs(yAmount)
        #print("count:",count)
        if count < 1:
            print("Terminado")
            global moving
            moving = False

    #return movementsList



def isNotMovableX(x,canvas):
    notMovable = False
    if x<50 or x>canvas.winfo_width()-50:
        notMovable = True
    return notMovable

def isNotMovableY(y,canvas):
    notMovable = False
    if y<50 or y>canvas.winfo_height()/3:
        notMovable = True
    return notMovable

def getCoordsOfIcon(name,canvas):
    #print("getCoordsOfIcon:",name)
    objectCoords = canvas.coords(name)
    #print("objectCoords:", objectCoords)
    if len(objectCoords)>0:
        x = objectCoords[0]
        y = objectCoords[1]
    else:
        x = 0
        y = 0
    return x, y

def getDistance(x,y,x1,y1):
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance

def getDeltaMove(x,y,x1,y1,strenght, speed):
    d = getDistance(x,y,x1,y1)
    #print("d:",d)
    if d > 0:
        xAmount = (x1-x)*strenght*speed/d
        yAmount = (y1-y)*strenght*speed/d
    else:
        xAmount = 0
        yAmount = 0
    return xAmount, yAmount

'''
def moveIconsByLinks(movementsList):
    for i in range(len(movementsList)):
        name = movementsList[i][0]
        x = movementsList[i][2]
        y = movementsList[i][3]
        x1 = movementsList[i][4]
        y1 = movementsList[i][5]
        strength = movementsList[i][6]
        xAmount, yAmount = getDeltaMove(x, y, x1, y1, strenght, speed)
        canvas.move(tagOrId, xAmount, yAmount)
'''