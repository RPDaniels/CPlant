from math import sqrt
#import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Label, CENTER

#https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html

def moveImage(name, xAmount, yAmount, mycanvas):
    xmin = 50
    xmax = mycanvas.winfo_width() - 100
    ymin = 50
    ymax = 410 #mycanvas.winfo_width()/3
    tagname = name.replace(' ', '_')
    x = 0
    y = 0
    if len(mycanvas.find_withtag(tagname))!=0:
        objectCoords = mycanvas.coords(tagname)
        x0 = int(objectCoords[0])
        y0 = int(objectCoords[1])

        xcand = x0 + xAmount
        ycand = y0 + yAmount
        if xcand > xmin and xcand < xmax:
            x = xAmount
        else:
            x = 0
        if ycand > ymin and ycand < ymax:
            y = yAmount
        else:
            y = 0
        mycanvas.move(tagname, x, y)
    return x,y

def pinImage(name, x, y, side, mycanvas, role="node"):
    # print(name)
    tagname = name.replace(' ','_')
    '''
    if len(mycanvas.find_withtag(tagname))!=0:
        objectCoords = mycanvas.coords(tagname)
        x0 = objectCoords[0]
        y0 = objectCoords[1]
        print("delete Image", x0, y0, tagname, name)
        mycanvas.delete(tagname)
    '''
    try:
        photo2 = Image.open("./image/" + name + ".png")
    except:
        photo2 = Image.open("./image/Frame_icon.png")
    photo2 = photo2.resize((int(side / 2), int(side / 2)), Image.ANTIALIAS)
    imgtk2 = ImageTk.PhotoImage(photo2)

    # Truco sucio para mostrar las imágenes: guardar una referencia
    label = Label(image=imgtk2, background="red")
    label.image = imgtk2  # keep a reference!
    label.pack_forget()

    #print("pinImage",x,y,tagname,name)
    if role=="link":
        tagname = tagname + "_link"
    imgX = mycanvas.create_image(int(x), int(y), anchor=CENTER, image=imgtk2, tag=(tagname,"icon"))

    # print(canvas.coords(name))
    chunks = name.split(' ')
    yline = y
    fontsize = int(side /10)
    myFont = 'Helvetica ' + str(fontsize)
    for line in chunks:
        mycanvas.create_text(x, yline + fontsize *4, text=line, fill="black", font=(myFont), tags=tagname)
        yline = yline + fontsize * 2
    #print("mycanvas", tagname, mycanvas.find_withtag(tagname))

    return imgX

def getImage(name):
    try:
        photo2 = Image.open("./image/" + name + ".png")
    except:
        photo2 = Image.open("./image/Frame_icon.png")
    photo2 = photo2.resize((int(50), int(50)), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(photo2)
    return image

def getImageLabel(mycanvas, imageId):
    tags = mycanvas.gettags(imageId)
    #print("id:", imageId)
    #print("tags:", tags)
    val = ''
    if len(tags) > 1:
        val = tags[0].replace("_"," ")
    #print("Image Label:",val)
    return val

def square(x, y,color,squareside,canvas):
    width = int(squareside / 2) - 1
    height = squareside / 2 - 1
    yoffset = int (squareside / 5)
    canvas.create_rectangle(x - width, y-height + yoffset, x + width, y + height + yoffset, fill=color)

def rect(x, y,squareside,widthside, canvas):
    yoffset = int(squareside / 5)
    canvas.create_rectangle(x, y+yoffset, x+widthside, y+yoffset + squareside)

def getCoordsOfIcon(canvas,name):
    # print("getCoordsOfIcon:",name)
    name = name.replace(" ", "_")
    objectCoords = canvas.coords(name)
    # print("objectCoords:", objectCoords)
    if len(objectCoords) > 0:
        x = objectCoords[0]
        y = objectCoords[1]
    else:
        #print("getCoordsOfIcon:",name)
        x = 0
        y = 0
    return int(x), int(y)

def getDistance(x0,y0,x1,y1):
    distance = sqrt((x1 - x0)**2 + (y1 - y0)**2)
    return distance

def getDeltaMove(x, y, x1, y1, strenght, speed):
    d = getDistance(x, y, x1, y1)
    if d > 0:
        xAmount = (x1 - x) * strenght * speed / d
        yAmount = (y1 - y) * strenght * speed / d
    else:
        xAmount = 0
        yAmount = 0
    return int(xAmount), int(yAmount)

def limitCoordinates(x,y,mycanvas): #bloquea las coordenadas si llegan al límite del marco
    xmin = 50
    xmax = mycanvas.winfo_width() - 100
    ymin = 50
    ymax = 410
    if x < xmin: x = xmin
    if y < ymin: y = ymin
    if x > xmax: x = xmax
    if y > ymax: y = ymax
    return x,y

def getSplittedList(txt,maxwidth):
    list = []
    lastwhite = 0
    start = 0
    while start < len(txt):
        limit = min(len(txt),int(start+maxwidth))
        for i in range(start,limit):
            if txt[i]==" ":
                lastwhite = i
        if lastwhite == start or i == len(txt)-1:
            lastwhite = limit
        if txt[start]==" ":
            start = start+1
        part = txt[start:lastwhite]
        list.append(part)
        start = lastwhite
    return list

#texto = "En un lugar de la mancha de cuyo nombre no quiero acordarme vivia un hidalgo de los de rocin flaco y galgo corredor"
#texto = "Unknown advantage"
#lista = getSplittedList(texto,25)
#print("--------------------------")
#print("Lista:",lista)