import sqlcplants
import canvasutils

class Compcanvas:

    def __init__(self, mycanvas):
        self.canvas = mycanvas
        self.squareside = 100
        self.maxcolumns = 10 #int((self.canvas.winfo_screenwidth() / 2) / self.squareside) +1
        self.allspecies = []

    def refreshAndShowAll(self):
        self.allspecies = sqlcplants.getSpeciesList() #.getAllSpecies()
        self.showAll()

    def showAll(self, relations={}):
        if len(self.allspecies)==0: # Load for the first time
            self.allspecies = sqlcplants.getSpeciesList() #.getAllSpecies()
        self.loadNodeNamesList(self.allspecies, "ghostwhite", relations) ####
        return len(self.allspecies)

    def refreshSpecies(self, species, relations={}):
        if species == 'All':
            numspecies = self.showAll(relations)
        else:
            numspecies = self.loadCompanions(species)
        return numspecies

    def loadNodeNamesList(self, nodeNamesList, color = "yellowgreen", relations={}):
        col = 1
        row = 1
        defaultColor = color
        #print("list of nodes:",nodeNamesList)
        for name in nodeNamesList:
            x = col * self.squareside - self.squareside / 2
            y = row * self.squareside - self.squareside / 2
            if name in relations:
                if relations[name] == "positive":
                    color = "yellowgreen"
                elif  relations[name] == "negative":
                    color = "indianred" #indianred
                else:
                    color = "teal"
            else:
                color = defaultColor
            canvasutils.square(x,y,color,self.squareside,self.canvas)
            canvasutils.pinImage(name, x, y, self.squareside, self.canvas)
            col += 1
            if col == self.maxcolumns + 1:
               col = 1
               row += 1
        return len(nodeNamesList)

    def loadCompanions(self, species):
        myrow = self.displayRelatedNodesOf(species, direction="is affected by", row=0)
        self.displayRelatedNodesOf(species, direction="affects", row=myrow+1)

    def displayRelatedNodesOf(self, species, direction="affects", row=1):
        if direction == "affects": # The species affects other nodes
            nodeList = sqlcplants.getAffectedBy(species)
        else: # The species is affected by the companions
            nodeList = sqlcplants.getCompanions(species)
        speciesNode = sqlcplants.getNodeByName(species)

        canvasutils.pinImage(species, int(self.squareside/2), int(row * self.squareside + self.squareside / 2), self.squareside, self.canvas)
        fontsize = int(self.squareside / 10)
        myFont = 'Helvetica ' + str(fontsize)
        self.canvas.create_text(int(self.squareside * 2), int(self.squareside * (row+0.5)), text=direction+":",
                                fill="black", font =myFont)
        col = 1
        row = row + 1
        for node in nodeList:
            if direction == "affects":
                link = sqlcplants.getLink(node,speciesNode) #second affects first
            else:
                link = sqlcplants.getLink(speciesNode, node)
            if isAllowed(link.strength,set):
                if int(link.strength) > 0:
                    color = "mediumseagreen"
                else:
                    color = "indianred"
                x = col * self.squareside - self.squareside / 2
                y = row * self.squareside + self.squareside / 2
                canvasutils.square(x,y,color,self.squareside,self.canvas)
                canvasutils.pinImage(node.name, x, y, self.squareside, self.canvas)
                col += 1
                if col == self.maxcolumns + 1:
                    col = 1
                    row += 1
        return row #len(nodeList)


def isAllowed(strength ,set): # determines if a node is to be shown depending on the value of "set"
    response = bool(True)
    if set == 'negative' and strength >0:
        response = bool(False)
    if set == 'positive' and strength <0:
        response = bool(False)
    return response

