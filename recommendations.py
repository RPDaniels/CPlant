import sqlcplants
from numpy import zeros, arange

def getRecommendationsList(itemIdList):
    matrix = sqlcplants.getLinkMatrix() # Get all links from db
    numnodos = sqlcplants.getmaxnode()
    print("numnodos:",numnodos)
    matriz_relaciones = zeros((numnodos+1, numnodos+1))

    matriz_relaciones[:,0] = arange(0,numnodos+1) # First column contains the ids of all nodes
    matriz_relaciones[0,:] = arange(0,numnodos+1) # First column contains the ids of all# possible candidates
    for i in matrix:
        #print("x,y,val:",i[0],i[1],i[2])
        if i[0]<=numnodos and i[1]<=numnodos:
            matriz_relaciones[i[0],i[1]] = i[2] # Builds the full matrix of relationships
    #print("matriz_relaciones",matriz_relaciones)
    # seleccionar las filas de los items del ecosistema
    itemIdList.insert(0,0) # Include first list with the ids
    new_matrix = matriz_relaciones[itemIdList,:].copy() # matriz con todas las relaciones posibles de ese ecosistema con todo lo demás

    # Se obtiene una matriz booleana donde se indica si existe algún elemento negativo en cada columna
    cols_to_remove = (new_matrix[1:,:] < 0).any(axis=0)

    # Se obtiene una matriz booleana donde se indica si todos los elementos son cero en cada columna
    cols_to_remove_zero = (new_matrix[1:,:] == 0).all(axis=0)

    # Se seleccionan todas las columnas que no contengan elementos negativos o ceros
    recommendations_matrix = new_matrix[:,~(cols_to_remove | cols_to_remove_zero)].copy()
    recommendations_list =  recommendations_matrix[0, :].copy()
    idlist = recommendations_list[1:] # remove first element that contains the id
    cleanList = list(set(idlist) - set(itemIdList))
    lista = []
    nameList = []
    for elemento in cleanList:
        lista.append(int(elemento))
    if len(lista)>0:
        nameList = sqlcplants.getNodeNamesFromIds(lista)
    return nameList












