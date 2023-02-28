import sqlcplants
from numpy import zeros, arange, insert

def getRecommendationsList(l,itemIdList, type="positive"):
    # Gets a list of species names recommended for a itemIdList (ecosystem)
    matrix = sqlcplants.getLinkMatrix() # Get all links from db
    numnodos = sqlcplants.getmaxnode()
    # empty matrix of zeroes including first row and first column for indexes:
    matriz_relaciones = zeros((numnodos+1, numnodos+1))
    matriz_relaciones[:,0] = arange(0,numnodos+1) # First column contains the ids of all nodes
    matriz_relaciones[0,:] = arange(0,numnodos+1) # First column contains the ids of all possible candidates
    for i in matrix: # Builds the full matrix of relationships
        #print("x,y,val:",i[0],i[1],i[2])
        if i[0]<=numnodos and i[1]<=numnodos:
            matriz_relaciones[i[0],i[1]] = i[2]  #sets a relationship in matrix
    # seleccionar las filas de los items del ecosistema
    itemIdList.insert(0,0) # Include first list with the ids
    new_matrix = matriz_relaciones[itemIdList,:].copy() # matriz con todas las relaciones posibles de ese ecosistema con todo lo demás

    if type == "positive":
        # List of columns where at least a value is negative (harmful to a species in our ecosystem):
        cols_to_remove = (new_matrix[1:,1:] < 0).any(axis=0)
        cols_to_remove = insert(cols_to_remove, 0, False)  # We keep the first column that contains the indexes

        # List of columns where all values are zero (not related to our ecosystem):
        cols_to_remove_zero = (new_matrix[1:,:] == 0).all(axis=0)

        # We select all columns that haven't negatives or all zeroes
        recommendations_matrix = new_matrix[:,~(cols_to_remove | cols_to_remove_zero)].copy()
    else:
        # List of columns where all values are positive or neutral:
        cols_to_remove = (new_matrix[1:, 1:] >= 0).all(axis=0)
        cols_to_remove = insert(cols_to_remove, 0, False)  # We keep the first column that contains the indexes
        # We select all columns that contain a value harmful to a species in our ecosystem
        recommendations_matrix = new_matrix[:, ~(cols_to_remove)].copy()

    recommendations_list =  recommendations_matrix[0, :].copy()
    idlist = recommendations_list[1:] # remove first element that contains the id
    cleanList = list(set(idlist) - set(itemIdList)) #remove species already contained in the ecosystem
    lista = []
    nameList = []
    for elemento in cleanList:
        lista.append(int(elemento))
    if len(lista)>0:
        nameList = sqlcplants.getNodeNamesFromIds(l,lista)
    return nameList

def getEcosystemCompanionsHash(l,itemIdList):
    positiveList = getRecommendationsList(l,itemIdList, type="positive")
    negativeList = getRecommendationsList(l,itemIdList, type="negative")
    inList = sqlcplants.getNodeNamesFromIds(l,itemIdList)
    res = dict()
    for elem in positiveList:
        res[elem] = "positive"
    for elem in negativeList:
        res[elem] = "negative"
    for elem in inList:
        res[elem] = "in"
    #print("res:",res)
    return res








