import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes = []
        self._idMap = {}
        self._graph = nx.Graph()
        pass


    def getRating(self):

        return DAO.getRating()



    def buildGraph(self, rate1, rate2):
        self._graph = nx.Graph()
        #self._graph.clear()
        self._nodes = DAO.getAllNodes(rate1, rate2)

        for n in self._nodes:
            self._idMap[n.id] = n
        self._graph.add_nodes_from(self._nodes)

        archi = DAO.getAllEdges(rate1, rate2)

        for a1, a2 in archi:

            nodo_a = self._idMap[a1]
            nodo_b = self._idMap[a2]

            peso = DAO.getPesoArco(a1, a2)
            peso_int = int(peso[0])
            self._graph.add_edge(nodo_a, nodo_b, weight=peso_int)


    def getNumNodes(self):
        return len(self._nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getTop5(self):
        archi = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]
        return archi

    def getCompConnesse(self):
        comp = list(nx.connected_components(self._graph))
        largest = max(comp, key=len)
        return len(comp) , largest
