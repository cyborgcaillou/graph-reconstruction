import sys
from Graph import Graph

def bitCount(n: int) -> int:
    """
    Uses bit manipulation to return the number of 1-bits in the binary
    form of n
    """
    n = ((0xaaaaaaaa & n) >> 1) + (0x55555555 & n)
    n = ((0xcccccccc & n) >> 2) + (0x33333333 & n)
    n = ((0xf0f0f0f0 & n) >> 4) + (0x0f0f0f0f & n)
    n = ((0xff00ff00 & n) >> 8) + (0x00ff00ff & n)
    n = ((0xffff0000 & n) >> 16) + (0x0000ffff & n)
    return n

def genSpecs(vertices: int) -> list[list[int]]:
    """
    Sorts all integers in the range [0, 2^vertices - 1] into buckets based
    on their bitcounts
    """
    specs = [list() for _ in range(vertices+1)]
    for i in range(2**vertices):
        specs[bitCount(i)].append(i)
    return specs

def genValid(vertices: int, degrees: list[int], possibilities: list[list[int]]) -> list[list[int]]:
    """
    Uses the number of vertices and the degree sequence to create all the 
    valid descriptions of graphs within the given class. The descriptions
    are based on the upper triangle of an adjacency matrix and are the 
    decimal conversions of those binary strings.
    """
    valid = [[]]
    #Base case
    if vertices == 2:
        #2 valid forms
        if degrees[0] == 1 and degrees[1] == 1:
            return [[1]]
        elif degrees[0] == 0 and degrees[1] == 0:
            return [[0]]
        #invalid cases
        else:
            return [[]]
    
    #Recursive case
    else:
        #Pulls all integers s.t. the bitcount matches the degree of the 
        #first vertex remaining
        pool = possibilities[degrees[0]]

        #iteration over these
        for num in pool:
            #preventing integers above our max size
            if num > pow(2, vertices - 1) - 1:
                break
            #determining how to change the current remaining degree sequence
            modDegrees = [degrees[i] - (num >> (vertices - i - 1))%2 for i in range(1, vertices)]
            #passing over invalid cases
            if -1 in modDegrees:
                pass
            #remaining cases
            else:
                lower = genValid(vertices - 1, modDegrees, possibilities)
                #more filtering (no valid cases for the remaining vertices)
                if lower == [[]]:
                    pass
                else:
                    #cleaning up
                    if valid[0] == []:
                        valid.pop(0)
                    #adding the current number to the front of all arrays
                    #generated from the remaining degree sequence and
                    #and appending these to the current valid cases
                    for validVec in lower:
                        validVec.insert(0, num)
                        valid.append(validVec)

        #pushing the valid cases back up the chain or out to the rest of
        #the program
        return valid
    
def individual(vertices: int, description: list[int]) -> Graph:
    """
    Generating a graph from its description list
    """
    indiv = Graph(vertices)
    for i in range(len(description)):
        for j in range(i + 1, len(description) + 1):
            if ((description[i] >> (vertices - j - 1))%2 == 1):
                indiv.addEdge(i, j)
    return indiv

#Might split into a bidegreed deg seq generator and a fcn that generates
#the class having a specific sequence. Also planning on adding in 
#isomorphism checking once the module for that has been built.
def genBiClass(vertices: int, numDeg1: int, deg1: int, deg2: int, possibilities: list[list[int]]) -> list[Graph]:
    """
    The only part of the program specific to bidegreed graphs.
    Generates all valid graphs with the specified deg sequence.
    """
    biClass = []
    degrees = [deg1 for i in range(numDeg1)] + [deg2 for i in range(vertices - numDeg1)]
    valid = genValid(vertices, degrees, possibilities)
    for validVec in valid:
        biClass.append(individual(vertices, validVec))
    return biClass

#This is probably mostly gonna go in the wrapper
def main():
    vertices = int(sys.argv[1])
    sys.stdout = open(sys.argv[2], "w")

    possibilities = genSpecs(vertices)

    for deg1 in range(2, vertices):
        if not deg1 % 2:

            if not vertices % 2:
                start = 2
            else:
                start = 1

            for numDeg1 in range(start, vertices, 2):
                biClass = genBiClass(vertices, numDeg1, deg1, deg1 - 1, possibilities)
                for graph in biClass:
                    graph.print()

        else:
            for numDeg1 in range(2, vertices, 2):
                biClass = genBiClass(vertices, numDeg1, deg1, deg1 - 1, possibilities)
                for graph in biClass:
                    graph.print()
    
    sys.stdout.close()

if __name__ == "__main__":
    main()

#Unit tests
def test_bitCount():
    assert bitCount(0) == 0
    assert bitCount(1) == 1
    assert bitCount(1564687) == 11
    assert bitCount(4578) == 6

def test_genSpecs():
    assert genSpecs(1) == [[0], [1]]
    assert genSpecs(2) == [[0], [1, 2], [3]]
    assert genSpecs(4) == [[0], [1, 2, 4, 8], [3, 5, 6, 9, 10, 12], [7, 11, 13, 14], [15]]

def test_genValid():
    assert genValid(2, [1, 1], genSpecs(2)) == [[1]]
    assert genValid(2, [1, 0], genSpecs(2)) == [[]]
    assert genValid(3, [1, 1, 1], genSpecs(3)) == [[]]
    assert genValid(3, [1, 1, 2], genSpecs(3)) == [[1, 1]]
    assert genValid(3, [1, 2, 1], genSpecs(3)) == [[2, 1]]
    assert genValid(4, [1, 1, 1, 1], genSpecs(4)) == [[1, 2, 0], [2, 1, 0], [4, 0, 1]]

def test_individual():
    assert individual(4, [1, 2, 0]).vertices == [[3], [2], [1], [0]]
    assert individual(4, [4, 0, 1]).vertices == [[1], [0], [3], [2]]
    assert individual(4, [7, 3, 1]).vertices == [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]

def test_genBiClass():
    assert [graph.vertices for graph in genBiClass(4, 2, 2, 1, genSpecs(4))] == [[[1, 3], [0, 2], [1], [0]], [[1, 2], [0, 3], [0], [1]]]  
    assert [graph.vertices for graph in genBiClass(4, 2, 3, 2, genSpecs(4))] == [[[1, 2, 3], [0, 2, 3], [0, 1], [0, 1]]]