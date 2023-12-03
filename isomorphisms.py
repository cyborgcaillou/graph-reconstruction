from Graph import Graph, WeightedDigraph
from copy import deepcopy

def partAdjacencies(g: Graph, part: list[list[int]]) -> list[list[int]]:
    """
    Given a graph and a partition on the vertices returns the
    adjacencies each vertex has with each cell
    """
    #Basically O(n^2) just uses a particular ordering
    #to iterate through the vertices twice 
    cellList = []
    globIter = -1
    for cell in range(len(part)):
        for vert in range(len(part[cell])):
            globIter += 1
            #Zeroes out the adjacencies in the partition list
            cellList.append([0 for i in range(len(part))])
            for cell2 in range(len(part)):
                for vert2 in part[cell2]:
                    #If vert2 is not adjacent to vert1
                    #skip. Else, add 1 to the list associated
                    #with vert1 at the index of that cell
                    try: 
                        g.vertices[part[cell][vert]].index(vert2)
                        cellList[globIter][cell2] += 1
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
    part = [list() for i in range(len(degSeq))]
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
    cellList = {vertex:[] for vertex in range(len(g.vertices))}
    #Refines partition so that each member of a cell
    #is adjacent to the same number of vertices from 
    #each cell, including itself
    refined = False
    while not refined:
        newPart = []
        cellList = partAdjacencies(g, part)
        globIter = 0
        for cell in range(len(part)):
            locIter = -1
            #consistent reordering within cell
            if len(part[cell]) > 1:
                #in progress reordering
                reordering = []
                #adjacency lists to be sorted
                revLookup = []
                for vert in part[cell]:
                    locIter += 1
                    revLookup.append(cellList[globIter + locIter])
                #sorting adjacency lists
                revLookup = sorted(revLookup)
                #reordering original cell by using sorted list of adjacency lists
                for term in revLookup:
                    locIter = -1
                    for vert in part[cell]:
                        locIter += 1
                        if cellList[globIter + locIter] == term and vert not in reordering:
                            reordering.append(vert)
                #removes any duplicates added in the previous step
                part[cell] = reordering
                cellList = partAdjacencies(g, part)
            if len(part[cell]) > 1:
                #Tracks what vertices have been updated within the cell
                updated = []
                locIter = -1
                for vert in part[cell]:
                    locIter += 1
                    if vert not in updated:
                        #Sets the standard for the list comparison and
                        #creates a subpartition 
                        standard = cellList[globIter + locIter]
                        updated.append(vert)
                        subcell = [vert]
                        #Adds any vert in the cell sharing the same list
                        #to the new subpartition 
                        locIter2 = -1
                        for vert2 in part[cell]:
                            locIter2 += 1
                            if vert2 not in updated and cellList[globIter + locIter2] == standard:
                                subcell.append(vert2)
                                updated.append(vert2)
                        newPart.append(subcell)
            else:
                newPart.append(part[cell])
            globIter += len(part[cell])
        #The length is nondecreasing across iterations, and if it's the
        #same, kill the loop 
        if len(newPart) == len(part):
            refined = True
        else:
            part = newPart
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
                    partTest = deepcopy(part)
                    partTest[i].pop(j)
                    partTest.insert(i, [part[i][j]])
                    jthQuotient = partAdjacencies(g,quotient(g, partTest))
                    unique.append(jthQuotient)
                    quotDict[j] = jthQuotient
                uniqueSet = []
                for k in range(len(unique)):
                    if unique[k] not in uniqueSet:
                        uniqueSet.append(unique[k])
                if len(uniqueSet) == 1 and i == len(part)-1:
                    terminate = True
                #If any aquotients are different, repartition
                elif len(uniqueSet) != 1:
                    unique = sorted(uniqueSet)
                    subcells = [list() for i in range(len(unique))]
                    for t in range(len(unique)):
                        for vert in range(len(part[i])):
                            if quotDict[vert] == unique[t]:
                                subcells[t].append(part[i][vert])
                    part.pop(i)
                    for cell in subcells[::-1]:
                        part.insert(i, cell)
                    #starts over with new partition
                    break
            elif len(part[i]) == 1 and i == len(part)-1:
                terminate = True
    #cellList = partAdjacencies(g, part)
    #extract and sort the partition adjacencies so that the finalized
    #list is the same across isomorphisms.
    return part

def final(g: Graph, part: list[list[int]]) -> tuple[list[list[int]], dict[int:list[list[int]]]]:
    """
    An extra labeling on the terminal quotient graph vertices.
    """
    vertQuotients = {}
    #pulls out a vertex of the ith cell and finds the vertex quotient
    #of a vertex in i (remembering that they are all the same),
    #labelling that cell with the vertex quotient
    for cell in range(len(part)):
        if len(part[cell]) > 1:
            newPart = deepcopy(part)
            newPart.insert(cell, [part[cell][0]])
            newPart[cell+1].pop(0)
            vertQuotients[cell] = partAdjacencies(g, quotient(g, newPart))
        else:
            vertQuotients[cell] = partAdjacencies(g, quotient(g, part))
    return (partAdjacencies(g, part), vertQuotients)

def representative(g1: Graph) -> tuple[list[list[int]], dict[int:list[list[int]]]]:
    return final(g1, terminal(g1, quotient(g1, initPartition(g1))))