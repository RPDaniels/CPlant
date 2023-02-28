import math
from tkinter import messagebox
from tkinter import simpledialog

from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, Label, Tk, Entry, Button, Canvas, Frame, BOTTOM, LEFT, RIGHT, TOP, CENTER
import sqlcplants
import canvasutils

class Ecocanvas:
    def __init__(self,lang, mycanvas):
        self.canvas = mycanvas
        self.squareside = 100
        self.radius = 100
        self.l = lang

    def set(self,ecosystem,ecosystemLinks):
        self.ecosystem = ecosystem
        self.ecosystemLinks = ecosystemLinks

    def addCompanionToEcosystem(self,companionName):
        # Get node based on name
        mynode = sqlcplants.getNodeByName(companionName)
        # Get position in ecosystem based on NodeId
        pos = self.getPositionInEcosystem(mynode.id)
        if pos == len(self.ecosystem):  # Verificar primero si no está
            self.ecosystem.append(mynode) # Mejora: meter el nodo en su orden
            self.ecosystemLinks = sqlcplants.getEcosystemLinksBynodeList(self.ecosystem)
        return self.ecosystem, self.ecosystemLinks

    def removeCompanionFromEcosystem(self,companionName):
        if companionName != 'All' and companionName != '':
            # Get node based on name
            mynode = sqlcplants.getNodeByName(companionName)
            # Get position in ecosystem based on NodeId
            pos = self.getPositionInEcosystem(mynode.id)
            if pos < len(self.ecosystem):  # Verificar primero si está
                self.ecosystem.pop(pos)
                self.ecosystemLinks = sqlcplants.getEcosystemLinksBynodeList(self.ecosystem)
        return self.ecosystem, self.ecosystemLinks

    def drawEcosystemCircle(self):
        i = 0
        for node in self.ecosystem:
            x, y = self.getItemCoordinatesInCircle(i) # Gets position in the circle
            canvasutils.pinImage(self.l,node.name, x, y, self.squareside, self.canvas)
            i += 1
        for link in self.ecosystemLinks:
            self.drawLink(link)
        self.drawLinkReport()

    def getLinkData(self,link, data): # gets all data necessary to update a link and its icons in the screen
        primary = link.primary
        companion = link.companion
        strenght = link.strength
        namep = data[primary]["name"]
        namec = data[companion]["name"]
        xp = data[primary]["x"]
        yp = data[primary]["y"]
        xc = data[companion]["x"]
        yc = data[companion]["y"]
        return namec, xc, yc, namep, xp, yp, strenght

    def getIconHash(self): # Gets a dictionary of all icons in eco screen with its coordinates
        data = {}
        for node in self.ecosystem: # Gets current coords from canvas
            id = node.id
            name = node.name
            x,y = canvasutils.getCoordsOfIcon(self.canvas,name)
            data[id]={"name": name, "x": x, "y": y}
        return data

    def drawMovingEcosystem(self):  # Moves 1 frame the ecosystem, attracting or repelling linked icons
        iconDictionary = self.getIconHash()
        for link in self.ecosystemLinks: # Update images
            namec, xc, yc, namep, xp, yp, strenght = self.getLinkData(link, iconDictionary)
            xcAmount, ycAmount = canvasutils.getDeltaMove(xc, yc, xp, yp, strenght, 3) # Companion goes to primary
            #print("--", namec, xcAmount, ycAmount, namep)

            xcAmount, ycAmount = canvasutils.moveImage(namec, xcAmount, ycAmount, self.canvas) #companion goes to primary
            iconDictionary[link.companion]["x"] = xc + xcAmount
            iconDictionary[link.companion]["y"] = yc + ycAmount

            xcAmount, ycAmount  = canvasutils.moveImage(namep, -xcAmount, -ycAmount, self.canvas)  # primary goes to companion
            iconDictionary[link.primary]["x"] = xp + xcAmount
            iconDictionary[link.primary]["y"] = yp + ycAmount

            self.refreshLinks(iconDictionary)

    def refreshLinks(self, iconDictionary): # Updates the links in screen
        self.canvas.delete("link")
        for link in self.ecosystemLinks: #Update links
            namec, xlc, ylc, namep, xlp, ylp, strenght = self.getLinkData(link, iconDictionary)
            if link.strength > 0:
                color = "green"
            else:
                color = "red"
            self.canvas.create_line(xlc, ylc, xlp, ylp, fill=color, width=2, smooth=1, arrow="last", arrowshape="8 10 10",
                                    tag=(link.description,"link"))
            self.canvas.update_idletasks()

    def drawLink(self,link): # Draws an arrow link in screen
        #print(link.getPrimaryName() + " -> " + link.getCompanionName())
        pos1 = self.getPositionInEcosystem(link.companion)
        pos2 = self.getPositionInEcosystem(link.primary)
        x0, y0 = self.getItemCoordinatesInCircle(pos1)
        x1, y1 = self.getItemCoordinatesInCircle(pos2)
        if link.strength > 0:
            color = "green"
        else:
            color = "red"
        self.canvas.create_line(x0, y0, x1, y1, fill=color, width=2, smooth=1, arrow="last", arrowshape="8 10 10",
                           tag=(link.description,"link"))

    def getEcoDrawingHeight(self):
        y = (self.radius + self.squareside) * 2
        return y

    def drawLinkReport(self):   # Shows the list of icons couples ant the description of their relationship
        data = self.getIconHash()
        side = 100
        descriptionwidth = 300
        x = side / 2 + 1
        y = (self.radius + self.squareside)*2
        fontsize = int(side / 10)
        myFont = 'Helvetica ' + str(fontsize)
        tagname = "datos"
        xoffset = 0
        for link in self.ecosystemLinks:
            primary = link.primary #-> get name by id -> ge
            companion = link.companion
            strenght = link.strength
            description = link.description
            name1 = data[primary]["name"]
            name2 = data[companion]["name"]
            if strenght>0: color = "mediumseagreen"
            else: color = "indianred"
            canvasutils.square(x+xoffset, y, "white", side, self.canvas)
            canvasutils.pinImage(self.l,name1, x+xoffset, y, side, self.canvas, role="link")
            canvasutils.square(x + side+xoffset, y, color, side, self.canvas)
            canvasutils.pinImage(self.l,name2, x+side+xoffset, y, side, self.canvas, role="link")
            canvasutils.rect(x+side*1.5+xoffset+1, y-side/2+2, side-2, side*2-1, self.canvas)
            #self.canvas.create_rectangle(x+side*2+xoffset, y, x+side*2+xoffset + descriptionwidth, y + side)
            descriptionList = canvasutils.getSplittedList(description,30)
            for k in range(len(descriptionList)):
                self.canvas.create_text(x+side*1.5+xoffset+10, y-side/4+k*side/5, text=descriptionList[k], fill="black", font=(myFont), tags=tagname, anchor ="nw")
            if xoffset ==0:
                xoffset = 410 #canvas.width / 2
            else:
                xoffset = 0
                y += side

    def getPositionInEcosystem(self, nodeid): # Given an ecosystem (list of nodes), get the node in position nodeid
        i = 0
        for node in self.ecosystem:
            if node.id == nodeid:
                break
            i += 1
        return i

    def getItemCoordinatesInCircle(self,positionInEcosystem): # Get x,y coordinates in eco circle for a position
        numnodes = len(self.ecosystem)
        self.radius = 100 + 6 * numnodes
        angle = math.radians(360 / numnodes) * positionInEcosystem
        xcenterecosystem = self.canvas.winfo_screenwidth() / 4
        ycenterecosystem = 150
        x = xcenterecosystem + math.cos(angle) * self.radius
        y = ycenterecosystem + math.sin(angle) * self.radius + 6 * numnodes
        return x, y

    def loadEcosystemByName(self, name): # Gets the nodes and links from the DB and updates these variables
        self.ecosystem = sqlcplants.getEcosystemNodes(name)
        self.ecosystemLinks = sqlcplants.getEcosystemLinks(name)
        return self.ecosystem, self.ecosystemLinks

    def saveEcosystem(self,defaultname): # Saves current ecosystem into the database
        ecoName = simpledialog.askstring(self.l.get("Save ecosystem"), self.l.get("Enter an ecosystem name to save:"), initialvalue=defaultname)
        if ecoName != None:
            sqlcplants.saveEcosystem(ecoName,self.ecosystem)
        return ecoName

    def deleteEcosystem(self,ecoName): # Deletes ecosystem from the database
        confirmation = messagebox.askyesno(self.l.get("Delete ecosystem"),self.l.get("You are going to delete ecosystem")+" "+ecoName)
        if confirmation:
            sqlcplants.removeEcosystem(ecoName)
            self.ecosystem = []
            self.ecosystemLinks = []
        return self.ecosystem, self.ecosystemLinks

    def getecosystemcombolist(self): #Gets a list of names of the ecosystems stored in database
        ecosystemList = sqlcplants.getEcosystemsList()
        ecosystemList.insert(0, self.l.get("(Select a ecosystem)"))
        return tuple(ecosystemList)




