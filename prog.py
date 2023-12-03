import Graph, isomorphisms, generator, sys
from copy import deepcopy

def traverse(g: Graph.Graph) -> bool:
    """
    Returns True if the graph is connected and False otherwise
    """
    #Mutually exclusive lists that total V(g)
    grabbed = [0]
    unused = [i for i in range(1, len(g.vertices))]
    #When all vertices are grabbed, stop and return True
    while len(unused) > 0:
        available = []
        for vertex in grabbed:
            for edge in g.vertices[vertex]:
                if edge not in grabbed:
                    available.append(edge)
        available = list(set(available))
        if len(available) == 0:
            return False
        grabbed.append(available[0])
        unused.remove(available[0])
    return True

def filt(biClass: list[Graph.Graph]) -> list[Graph.Graph]:
    classReprs = {}
    nbiClass = []
    for graph in biClass:
        if traverse(graph):
            nbiClass.append(graph)
            classReprs[graph] = isomorphisms.representative(graph)
    biClass = nbiClass
    rem = []
    print(len(biClass))
    for graph1 in range(len(biClass)-1):
        if graph1 in rem:
            continue
        for graph2 in range(graph1 + 1,len(biClass)):
            if classReprs[biClass[graph1]] == classReprs[biClass[graph2]]:
                rem.append(graph2)
            else:
                pass
    #print(rem)
    nbiClass = []
    for graph in range(len(biClass)):
        if graph not in rem:
            nbiClass.append(biClass[graph])
    #print(classReprs)
    print(len(nbiClass))
    return nbiClass

def deckComp(biClass: list[Graph.Graph]) -> list[Graph.Graph]:
    classDecks = {}
    for graph in biClass:
        classDecks[graph] = [isomorphisms.representative(card) for card in graph.deck()]
    for i in range(len(biClass)):
        for j in range(i+1, len(biClass)):
            a = deepcopy(classDecks[biClass[i]])
            b = deepcopy(classDecks[biClass[j]])
            hylo = True
            for graph1 in range(len(a)):
                for graph2 in range(len(b)):
                    if a[graph1] == b[graph2]:
                        b.pop(graph2)
                        break
                    if graph2 == len(b) - 1:
                        hylo = False
                if not hylo:
                    break
            if hylo:
                raise ValueError(f"Counterexample found:\n{biClass[i].vertices}\n {isomorphisms.terminal(biClass[i],isomorphisms.quotient(biClass[i],isomorphisms.initPartition(biClass[i])))},\n {biClass[j].vertices}\n {isomorphisms.terminal(biClass[i],isomorphisms.quotient(biClass[j],isomorphisms.initPartition(biClass[j])))} \n {[len(v) for v in biClass[i].vertices]}")
    return biClass

def main():
    vertices = int(sys.argv[1])
    sys.stdout = open(sys.argv[2], "w")

    possibilities = generator.genSpecs(vertices)

    for deg1 in range(2, vertices):
        if not deg1 % 2:

            if not vertices % 2:
                start = 2
            else:
                start = 1

            for numDeg1 in range(start, vertices, 2):
                biClass = generator.genBiClass(vertices, numDeg1, deg1, deg1 - 1, possibilities)
                biClass = filt(biClass)
                biClass = deckComp(biClass)
                print([deg1]*numDeg1 + [deg1-1]*(vertices-numDeg1))
                print()
                for graph in biClass:
                    graph.print()

        else:
            for numDeg1 in range(2, vertices, 2):
                biClass = generator.genBiClass(vertices, numDeg1, deg1, deg1 - 1, possibilities)
                biClass = filt(biClass)
                biClass = deckComp(biClass)
                print([deg1]*numDeg1 + [deg1-1]*(vertices-numDeg1))
                print()
                for graph in biClass:
                    graph.print()
    
    sys.stdout.close()

if __name__ == "__main__":
    main()