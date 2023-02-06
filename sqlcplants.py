#import sqlite3
from sqlite3 import connect

def select(query):
   conn = connect('CPlants.db')
   cursor = conn.execute(query)
   mylist = []
   for record in cursor:
      mylist.append(record)
   conn.close()
   return mylist

def insert(query):
   conn = connect('CPlants.db')
   conn.execute(query)
   conn.commit()
   conn.close()

class link:
   def __init__(self, row):  # Constructor
      self.id = row[0]
      self.primary = row[1]
      self.companion = row[2]
      self.strength = row[3]
      self.type = row[4]
      self.description = row[5]


class node:
   def __init__(self, row):  # Constructor
      self.id = row[0]
      self.name = row[1]
      self.name_lat = row[2]
      self.name_es = row[3]
      self.parent = row[4]
      self.type = row[5]
   '''
   def getname(self):
      return self.name

   def getPrimaryName(self):
      query = "SELECT ND_NAME from NODE WHERE ND_ID="+ str(self.primary)+" ORDER BY ND_NAME"
      records = select(query)
      return records[0][0]

   def getCompanionName(self):
      query = "SELECT ND_NAME from NODE WHERE ND_ID="+ str(self.companion) +" ORDER BY ND_NAME"
      records = select(query)
      return records[0][0]
   '''
############# NODES ################################

def getAllNodes():
   query = "SELECT ND_ID, ND_NAME, ND_NAME_LAT, ND_NAME_ES, ND_PARENT, ND_TYPE from NODE"
   records = select(query)
   nodelist = []
   for row in records:
      #print(row[0], row[1], row[2], row[3], row[4], row[5])
      nodelist.append(node(row))
   #for n in nodelist:
      #print(n.id, n.getname())
   return nodelist

def getnodecount():
   query = "SELECT COUNT() FROM NODE"
   records = select(query)
   count = records[0][0]
   return count

def getmaxnode():
   query = "SELECT MAX(ND_ID) FROM NODE"
   records = select(query)
   max = records[0][0]
   return max

def savenode(row):
   query_saveNode = "INSERT INTO NODE (ND_PARENT, ND_TYPE, ND_NAME, ND_NAME_LAT, ND_NAME_ES) VALUES " \
                 "('" + row[0] + "','" + row[1] + "','" + row[2] + "','" + row[3] + "','" + row[4] + "')"
   insert(query_saveNode)

def deletenode(name):
   node = getNodeByName(name)
   query_deleteNodeLinks = "DELETE FROM LINK WHERE LK_PRIM = "+ str(node.id) +" OR LK_COMPANION = " + str(node.id)
   insert(query_deleteNodeLinks)

   query_deleteNode = "DELETE FROM NODE WHERE ND_NAME = '" + name +"'"
   insert(query_deleteNode)


def getSpeciesList():
   query = "SELECT ND_NAME from NODE ORDER BY ND_NAME"
   records = select(query)
   namelist = []
   for row in records:
      namelist.append(row[0])
   return namelist

def getAllSpecies():
   query_getAllSpecies = "SELECT ND_ID, ND_NAME, ND_NAME_LAT, ND_NAME_ES,ND_PARENT, ND_TYPE " \
                               "FROM NODE ORDER BY ND_NAME"
   records = select(query_getAllSpecies)
   nodelist = []
   for row in records:
        nodelist.append(node(row))
   return nodelist

def getNodeByName(name):
   query_getNodeByName = "SELECT ND_ID, ND_NAME, ND_NAME_LAT, ND_NAME_ES, ND_PARENT, ND_TYPE " \
                         "FROM NODE WHERE ND_NAME = '" + name + "' ORDER BY ND_NAME"
   records = select(query_getNodeByName)
   if len(records)>0:
      myNode = node(records[0])
   else:
      myNode = node(["0","","","","","",""])
   return myNode

def getNodeNamesFromIds(idlist,order=True):
   lista = str(idlist[0])
   for i in range(len(idlist)):
     lista = lista + ","+ str(idlist[i])
   query = "SELECT ND_NAME FROM NODE WHERE ND_ID IN ("+ lista +")"
   if order:
      query = query + " ORDER BY ND_NAME"
   records = select(query)
   namelist = []
   for row in records:
        namelist.append(row[0])
   return namelist

################# LINK #############################################
def getLink(node1,node2):
   primary = node1.id
   companion = node2.id
   myLink = getLinkByIds(primary, companion)
   return myLink

def getLinkByIds(primary,companion):
   query = "SELECT LK_ID, LK_PRIM, LK_COMPANION,LK_STRENGTH,LK_TYPE,LT_DESCRIPTION FROM LINK, LINK_TYPES" \
           " WHERE LK_PRIM = " + str(primary) + " AND LK_COMPANION = " + str(companion) + " AND LK_TYPE = LT_ID"
   records = select(query)
   if len(records)>0:
      myLink = link(records[0])
   else: myLink = link([0,"","","","",""])
   return myLink

def deleteLinkByNodeNames(primaryName, companionName):
   primary_node = getNodeByName(primaryName)
   companion_node = getNodeByName(companionName)
   query = "DELETE FROM LINK WHERE LK_PRIM = "+ str(primary_node.id)+" AND LK_COMPANION = " + str(companion_node.id)
   insert(query)

def getLinkMatrix():
   query = "SELECT LK_PRIM, LK_COMPANION, LK_STRENGTH FROM LINK"
   records = select(query)
   matrix = []
   for row in records:
      matrix.append([row[0], row[1], row[2]])
   #print(matrix)
   return matrix

def savelink(row):
   primary_name = row[0]
   companion_name = row[1]
   strength = int(row[2])
   description = row[3]
   query_get_linktypeid = "SELECT LT_ID FROM LINK_TYPES WHERE LT_DESCRIPTION = '"+description+"'"
   records = select(query_get_linktypeid)

   if len(records)> 0: # Link type already exists
      linktypeid = records[0][0]
   else: # Create link type
      if strength > 0: linkRating = "Good"
      else: linkRating = "Bad"
      query_saveLinkType = "INSERT INTO LINK_TYPES (LT_TYPE,LT_DESCRIPTION) VALUES " \
                           "('" + linkRating + "','" + description + "')"
      insert(query_saveLinkType)
      records = select(query_get_linktypeid)
      linktypeid = records[0][0]

   primary_node = getNodeByName(primary_name)
   companion_node = getNodeByName(companion_name)

   myLink = getLink(primary_node,companion_node)
   print("myLink:",myLink)
   print("myLinkid:", myLink.id)
   if myLink.id !=0: # Link exists, we have to update it
      query_updateLink = "UPDATE LINK SET LK_STRENGTH = "+str(strength)+", LK_TYPE="+ str(linktypeid)+\
                           " WHERE LK_PRIM = "+str(primary_node.id)+\
                           " AND LK_COMPANION = "+ str(companion_node.id)
      print(query_updateLink)
      insert(query_updateLink)
   else: # Link does not exist, let's create it
      query_saveLink = "INSERT INTO LINK (LK_PRIM, LK_COMPANION, LK_STRENGTH, LK_TYPE) VALUES " \
                    "('" + str(primary_node.id) + "','" + str(companion_node.id) + "','" + str(strength) \
                       + "','" + str(linktypeid) + "')"
      print(query_saveLink)
      insert(query_saveLink)

############# LINK TYPES #############################################
def getLinkTypesDescriptions():
   query = "SELECT LT_DESCRIPTION from LINK_TYPES ORDER BY LT_DESCRIPTION"
   records = select(query)
   namelist = []
   for row in records:
      namelist.append(row[0])
   return namelist

############## ECOSYSTEMS #############################################3
def getEcosystemIdByName(ecoName):
   query_getEcosystemId = "SELECT ES_ID FROM ECOSYSTEM WHERE ES_NAME = '" + ecoName + "'"
   records = select(query_getEcosystemId)
   if len(records) == 0:
      ecoId = ''
   else:
      ecoId = str(records[0][0])
   return ecoId

def getEcosystemsList():
   query = "SELECT ES_NAME from ECOSYSTEM ORDER BY ES_NAME"
   records = select(query)
   namelist = []
   for row in records:
      namelist.append(row[0])
   return namelist

def getEcosystemNodes(ecoName):
   query_getEcosystemNodes = "SELECT ND_ID, ND_NAME, ND_NAME_LAT, ND_NAME_ES, ND_PARENT, ND_TYPE FROM NODE " \
                             "WHERE ND_ID IN " + "(SELECT EN_NODE FROM ECONODES, ECOSYSTEM " \
                             "WHERE " + "ES_NAME='" + ecoName + "' " + "AND EN_ECOSYS = ES_ID)" \
                             "ORDER BY ND_NAME"
   #(query_getEcosystemNodes)
   records = select(query_getEcosystemNodes)
   nodelist = []
   for row in records:
      nodelist.append(node(row))
   return nodelist

def getCompanions(name):
   query_getCompanionsByName = "SELECT ND_ID, ND_NAME, ND_NAME_LAT, ND_NAME_ES,ND_PARENT, ND_TYPE," \
                               " LK_STRENGTH, LT_DESCRIPTION FROM NODE," \
                               " LINK, LINK_TYPES WHERE LK_COMPANION = ND_ID and LK_PRIM IN " \
                               "(SELECT ND_ID FROM NODE WHERE ND_NAME = '" \
                               + name + "') " + "AND LT_ID = LK_TYPE " \
                               "ORDER BY ND_NAME"
   records = select(query_getCompanionsByName)
   nodelist = []
   for row in records:
        nodelist.append(node(row))
   return nodelist


def getEcosystemLinks(ecoName):
   nodeIds = getEcosystemNodes(ecoName)
   linklist = getEcosystemLinksBynodeList(nodeIds)
   return linklist

def getEcosystemLinksBynodeList(nodeIds):
   idlist = ""
   for node in nodeIds:
      idlist = str(node.id) + "," + idlist
   idlist = idlist[:-1]
   query = "SELECT LK_ID, LK_PRIM, LK_COMPANION,LK_STRENGTH,LK_TYPE,LT_DESCRIPTION FROM LINK, LINK_TYPES" \
           " WHERE LK_PRIM IN(" + idlist + ")" + "AND LK_COMPANION IN (" + idlist + ") AND LK_TYPE = LT_ID"
   #print(query)
   records = select(query)
   linklist = []
   for row in records:
        linklist.append(link(row))
   return linklist



def saveEcosystem(ecoName, nodeList):
   # Search Id by name
   ecoId = getEcosystemIdByName(ecoName)

   if ecoId =='': # New ecosystem
      query_saveEcosystem1 = "INSERT INTO ECOSYSTEM (ES_NAME) VALUES ('" + ecoName + "')"
      insert(query_saveEcosystem1)
      ecoId = getEcosystemIdByName(ecoName)
   else: # Delete existing nodes, since we are updating them
      query_saveEcosystem2 = "DELETE FROM ECONODES WHERE EN_ECOSYS ='" + ecoId + "'"
      insert(query_saveEcosystem2)
   ##
   for myNode in nodeList:
      nodeId = str(myNode.id)
      query_saveEcosystem3="INSERT INTO ECONODES (EN_ECOSYS, EN_NODE) VALUES (" + ecoId + "," + nodeId + ")"
      insert(query_saveEcosystem3)

def removeEcosystem(ecoName):
   query_getEcosystemId = "SELECT ES_ID FROM ECOSYSTEM WHERE ES_NAME = '" + ecoName + "'"
   records = select(query_getEcosystemId)
   ecoId = str(records[0][0])
   query_removeEcosystem = "DELETE FROM ECONODES WHERE EN_ECOSYS ='" + ecoId + "'"
   insert(query_removeEcosystem)
   query_removeEcosystem2 = "DELETE FROM ECOSYSTEM WHERE ES_ID = " + ecoId
   insert(query_removeEcosystem2)

