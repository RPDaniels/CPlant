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
        print("refreshAndShowAll")
        self.showAll()

    def showAll(self):
        if len(self.allspecies)==0: # Load for the first time
            print("showAll")
            self.allspecies = sqlcplants.getSpeciesList() #.getAllSpecies()
        self.loadNodeNamesList(self.allspecies, "ghostwhite") ####
        return len(self.allspecies)

    def refreshSpecies(self, species):
        if species == 'All':
            numspecies = self.showAll()
        else:
            numspecies = self.loadCompanions(species)
        return numspecies

    def loadNodeNamesList(self, nodeNamesList, color = "yellowgreen"):
        col = 1
        row = 1
        #print("list of nodes:",nodeNamesList)
        for name in nodeNamesList:
            #print("col:",col)
            #color = "yellowgreen"
            x = col * self.squareside - self.squareside / 2
            y = row * self.squareside - self.squareside / 2
            canvasutils.square(x,y,color,self.squareside,self.canvas)
            canvasutils.pinImage(name, x, y, self.squareside, self.canvas)
            col += 1
            if col == self.maxcolumns + 1:
               col = 1
               row += 1
        return len(nodeNamesList)

    def loadCompanions(self, species):
        set = 'all'
        companions = sqlcplants.getCompanions(species)
        speciesNode = sqlcplants.getNodeByName(species)
        canvasutils.pinImage(species, int(self.squareside/2), int(self.squareside/2), self.squareside, self.canvas)
        col = 1
        row = 1
        #print("companions:",companions)
        for node in companions:
            link = sqlcplants.getLink(speciesNode, node)
            if isAllowed(link.strength,set):
                if link.strength > 0:
                    color = "mediumseagreen"
                else:
                    color = "salmon"
                x = col * self.squareside - self.squareside / 2
                y = row * self.squareside + self.squareside / 2
                canvasutils.square(x,y,color,self.squareside,self.canvas)
                canvasutils.pinImage(node.name, x, y, self.squareside, self.canvas)
                col += 1
                if col == self.maxcolumns:
                    col = 1
                    row += 1
        return len(companions)

def isAllowed(strength ,set): # determines if a node is to be shown depending on the value of "set"
    response = bool(True)
    if set == 'negative' and strength >0:
        response = bool(False)
    if set == 'positive' and strength <0:
        response = bool(False)
    return response

