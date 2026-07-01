import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists = []
        self._bestGroup = []
        self._maxTracks = 0

    def buildGraph(self):
        self._graph.clear()
        self._artists = DAO.getAllArtists()

        self._graph.add_nodes_from(self._artists)

        artistPlaylists = DAO.getArtistPlaylistPairs()
        for artist in self._artists:
            artist.Playlists = set(artistPlaylists.get(artist.ArtistId, set()))

        for i in range(len(self._artists)):
            for j in range(i + 1, len(self._artists)):
                a1 = self._artists[i]
                a2 = self._artists[j]
                common = a1.Playlists & a2.Playlists
                if common:
                    peso = len(common)
                    self._graph.add_edge(a1, a2, weight=peso)

    def getArtistWithMaxDegree(self):
        if len(self._graph.nodes) == 0:
            return None, 0
        max_degree = -1
        best_artist = None
        for node, degree in self._graph.degree():
            if degree > max_degree:
                max_degree = degree
                best_artist = node
        return best_artist, max_degree

    def getArtistWithMaxWeightSum(self):
        if len(self._graph.nodes) == 0:
            return None, 0
        max_sum = -1
        best_artist = None
        for node in self._graph.nodes:
            weight_sum = sum(
                self._graph[node][neighbor]['weight']
                for neighbor in self._graph.neighbors(node)
            )
            if weight_sum > max_sum:
                max_sum = weight_sum
                best_artist = node
        return best_artist, max_sum

    def getTop10Edges(self):
        if len(self._graph.edges) == 0:
            return []
        edges_with_weights = [
            (u, v, self._graph[u][v]['weight'])
            for u, v in self._graph.edges
        ]
        edges_sorted = sorted(
            edges_with_weights,
            key=lambda x: (-x[2], x[0].Name, x[1].Name)
        )
        return edges_sorted[:10]

    def getBestGroup(self, starting_artist, N):
        self._bestGroup = []
        self._maxTracks = 0
        parziale = [starting_artist]
        self._ricorsione(parziale, N)
        return self._bestGroup, self._maxTracks

    def _ricorsione(self, parziale, N):
        if len(parziale) == N:
            total = self._getTotalTracks(parziale)
            if total > self._maxTracks:
                self._maxTracks = total
                self._bestGroup = copy.deepcopy(parziale)
            return

        for candidate in self._graph.nodes:
            if candidate in parziale:
                #skip questo candidato se già inserito in parziale
                continue

            # verifico se il candidato è adiacente ad almeno un elemento di parziale,
            # altrimenti skip il resto del codice perchè non è un candidato valido
            adjacent = any(
                self._graph.has_edge(candidate, existing)
                for existing in parziale
            )
            if not adjacent:
                continue

            # verifico che questo candidato non sia connesso a nessun elemento di parziale con un
            # arco di peso 1
            blocked = any(
                self._graph.has_edge(candidate, existing) and
                self._graph[candidate][existing]['weight'] == 1
                for existing in parziale
            )
            if blocked:
                continue

            parziale.append(candidate)
            self._ricorsione(parziale, N)
            parziale.pop()

    def _getTotalTracks(self, artists):
        return sum(len(a.Tracks) for a in artists)

    def getAllArtists(self):
        return self._graph.nodes

    def getNumAlbumsForArtist(self, artistID):
        return DAO.getNumAlbumsForArtist(artistID)

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)
