class Graph:
    def __init__(self, size: int) -> None:
        """
        Graphs are stored as an adjacency list
        """
        self.size = size
        self.vertices = [list() for _ in range(size)]
    
    def addEdge(self, vertex1: int, vertex2: int) -> None:
        if vertex2 not in self.vertices[vertex1]:
            self.vertices[vertex1].append(vertex2)
            self.vertices[vertex2].append(vertex1)
    
    def copy(self):
        """
        Creates a Graph object that's a copy of the original.
        """
        c = Graph(self.size)
        for v1 in range(len(self.vertices)):
            for v2 in self.vertices[v1]:
                c.addEdge(v1, v2)
        return c
    
    def card(self, delete: int):
        """
        Performs a vertex deletion on a copy of the graph and returns the card.
        """
        card = self.copy()
        for vertex in range(len(card.vertices)):
            if delete in card.vertices[vertex]:
                card.vertices[vertex].remove(delete)
            for edge in range(len(card.vertices[vertex])):
                if card.vertices[vertex][edge] > delete:
                    card.vertices[vertex][edge] -= 1
        del card.vertices[delete]
        return card
    
    def deck(self) -> list:
        """
        Returns the list of cards formed by vertex deletions on the graph.
        """
        deck = []
        for vertex in range(len(self.vertices)):
            deck.append(self.card(vertex))
        return deck

    def print(self) -> None:
        for vertex in self.vertices:
            print(str(vertex))
        print()

class Digraph(Graph):
    def addEdge(self, vertex1: int, vertex2: int) -> None:
        self.vertices[vertex1].append(vertex2)

class WeightedDigraph(Graph):
    def addEdge(self, vertex1: int, vertex2: int, weight: int) -> None:
        self.vertices[vertex1].append((vertex2, weight))