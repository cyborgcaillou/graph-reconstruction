from Graph import Graph, WeightedDigraph

def partAdjacencies(g: Graph, part: list[list[int]]) -> dict[list[int]:list[int]]:
    """
    Given a graph and a partition on the vertices returns the
    adjacencies each vertex has with each cell
    """
    #Basically O(n^2) just uses a particular ordering
    #to iterate through the vertices twice 
    cellList = {}
    for cell in range(len(part)):
        for vert in part[cell]:
            #Zeroes out the adjacencies in the partition list
            cellList[vert] = [0 for i in len(part)]
            for cell2 in range(len(part)):
                for vert2 in part[cell2]:
                    #If vert2 is not adjacent to vert1
                    #skip. Else, add 1 to the list associated
                    #with vert1 at the index of that cell
                    try: 
                        g.vertices[vert].index(vert2)
                        cellList[vert][cell2] += 1
                    except:
                        pass
    return cellList
    
def initPartition(g: Graph) -> list[list[int]]:
    """
    Creates initial partition based on degree sequence.
    The degree sequence is used because the initial partition 
    must be invariant under automorphism.
    """
    degSeq = []
    for i in range(len(g.vertices)):
        degSeq.append(len(g.vertices[i]))
    degSeq = sorted(set(degSeq), reverse=True)
    #Original version was specific to bidegreed graphs. Generalized
    #it with no small amount of pain and distress 
    part = [list()*len(degSeq)]
    for i in range(len(g.vertices)):
        #Probably should've just used a dict, but the conversions
        #seemed like kind of a pain 
        part[degSeq.index(len(g.vertices[i]))].append(i)
    return part

def quotient(g: Graph, part: list[list[int]]) -> list[list[int]]:
    """
    Creates a partition using an iterative series of refinements, some 
    further refinement of which is the automorphism partition. The end
    result is a partition where every element in every cell bears the
    same relation to every cell.
    """
    #holds the list of adjacencies between verts and cells
    cellList = {vertex:[] for vertex in g.vertices}
    #Refines partition so that each member of a cell
    #is adjacent to the same number of vertices from 
    #each cell, including itself
    refined = False
    while not refined:
        newPart = []
        cellList = partAdjacencies(g, part)
        for cell in range(len(part)):
            #consistent reordering within cell
            reordering = []
            revLookup = []
            for vert in part[cell]:
                revLookup.append(cellList[vert])
            revLookup = sorted(set(revLookup))
            for term in revLookup:
                for vert in part[cell]:
                    if cellList[vert] == term:
                        reordering.append(vert)
            part[cell] = reordering
            #Tracks what vertices have been updated within the cell
            updated = []
            for vert in part[cell]:
                if vert not in updated:
                    #Sets the standard for the list comparison and
                    #creates a subpartition 
                    standard = cellList[vert]
                    updated.append(vert)
                    subcell = []
                    #Adds any vert in the cell sharing the same list
                    #to the new subpartition 
                    for vert2 in part[cell]:
                        if vert2 not in updated and cellList[vert2] == standard:
                            subcell.append(vert2)
                            updated.append(vert2)
                    newPart.append(subcell)
        #The length is nondecreasing across iterations, and if it's the
        #same, kill the loop 
        if len(newPart) == len(part):
            refined = True
        else:
            part = newPart
    #extract and sort the partition adjacencies so that the finalized
    #list is the same across isomorphisms.
    pDict = {}
    pList = []
    for i in range(len(part)):
        standard = cellList[part[i][0]]
        pDict[standard] = part[i]
        pList.append(standard)
    pList = sorted(pList)
    part = []
    for std in pList:
        part.append(pDict[std])
    return part

def terminal(g: Graph, part: list[list[int]]) -> list[list[int]]:
    """
    Further refine the partition to maximize the number of transitive
    subgraphs. If two graphs are isomorphic, they have the same 
    terminal graph. Conjecturely, this is the automorphism partition
    on g.
    """
    #Alg only terminates when it can get through all cells w/out
    #repartitioning 
    terminate = False
    while not terminate:
        #Check all cells
        for i in range(len(part)):
            if len(part[i]) != 1:
                #Only cells with more than 1 vertex are considered
                unique = []
                quotDict = {}
                #Iterate through all vertices of i, creating a new
                #cell containing only the jth cell and making a new
                #quotient based on this new partition. Since this is
                #invariant under automorphism, vertices with different
                #quotients can't be in the same transitive subgraph 
                for j in range(len(part[i])):
                    partTest = part.copy()
                    del partTest[i][j]
                    partTest.insert(i, [part[i][j]])
                    jthQuotient = quotient(g, partTest)
                    unique.append(jthQuotient)
                    quotDict[j] = jthQuotient
                if len(set(unique)) == 1 and i == len(part)-1:
                    terminate = True
                #If any aquotients are different, repartition
                elif len(set(unique)) != 1:
                    unique = sorted(set(unique))
                    subcells = [list()*len(unique)]
                    for t in range(len(unique)):
                        for vert in part[i]:
                            if quotDict[vert] == unique[t]:
                                subcells[t].append(vert)
                    del part[i]
                    for cell in subcells[::-1]:
                        part.insert(i, cell)
                    #starts over with new partition
                    break
            elif len(part[i]) == 1 and i == len(part)-1:
                terminate == True
    cellList = partAdjacencies(g, part)
    #extract and sort the partition adjacencies so that the finalized
    #list is the same across isomorphisms.
    pDict = {}
    pList = []
    for i in range(len(part)):
        standard = cellList[part[i][0]]
        pDict[standard] = part[i]
        pList.append(standard)
    pList = sorted(pList)
    part = []
    for std in pList:
        part.append(pDict[std])
    return part

def representative(g: Graph, part: list[list[int]]) -> tuple(list[list[int]], dict[int:list[list[int]]]):
    """
    An extra labeling on the terminal quotient graph vertices.
    """
    vertQuotients = {}
    #pulls out a vertex of the ith cell and finds the vertex quotient
    #of a vertex in i (remembering that they are all the same),
    #labelling that cell with the vertex quotient
    for cell in range(len(part)):
        newPart = part.copy()
        newPart.insert(cell, part[cell][0])
        del part[cell+1][0]
        vertQuotients[cell] = partAdjacencies(g, quotient(g, newPart))
    return (partAdjacencies(g, part), vertQuotients)

def isomorphic(g1: Graph, g2: Graph) -> bool:
    return representative(g1, terminal(g1, quotient(g1, initPartition(g1)))) == representative(g2, terminal(g2, quotient(g2, initPartition)))
