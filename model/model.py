import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()  # grafo semplice
        self._idMapArtisti = {}

    def getCamminoMassimo(self, artista_partenza):
        self._best_path=[]
        self._minDistGiorni=100*365

        parziale=[artista_partenza]
        self._ricorsione(parziale, -1)
        return self._best_path

    def _ricorsione(self, parziale, peso_precedente):
        # 1. Caso terminale e aggiornamento della soluzione migliore
        # Se il cammino parziale attuale è più lungo di quello salvato finora, lo memorizziamo
        if len(parziale) > len(self._best_path):
            self._best_path = list(parziale)

        # Recuperiamo l'ultimo nodo inserito nel cammino, da cui dobbiamo continuare l'esplorazione
        u = parziale[-1]

        # 2. Esplorazione dei vicini (nodi adiacenti in uscita)
        for v in self._graph.neighbors(u):
            # Recuperiamo il peso dell'arco che va da u a v
            peso_arco = self._graph[u][v]["weight"]

            # CONDIZIONI FONDAMENTALI:
            # 1. Il peso dell'arco deve essere STRETTAMENTE CRESCENTE rispetto al precedente
            # 2. Il nodo 'v' non deve essere già stato visitato (cammino semplice -> no cicli)
            if peso_arco > peso_precedente and v not in parziale:
                # Passo accia: proviamo ad aggiungere il nodo al cammino
                parziale.append(v)

                # Chiamata ricorsiva: il peso di questo arco diventa il 'peso_precedente' per il prossimo passo
                self._ricorsione(parziale, peso_arco)

                # Backtracking: rimuoviamo il nodo per esplorare altre strade possibili
                parziale.pop()



    def buildGraph(self, genere):
        # svuoto il grafo
        self._graph.clear()

        self._artisti = DAO.getAllNodes(genere)

        for a in self._artisti:
            self._idMapArtisti[a.ArtistId] = a

        # aggiungo i nodi al grafo
        self._graph.add_nodes_from(self._artisti)

        edges = DAO.getAllEdges(  genere, self._idMapArtisti)
        #for e in edges:
           #self._graph.add_edge(e.a1, e.a2)

        #for n in self._generi:
            #self.mappaArtisti[n.ArtistId] = n
        #self._archi = DAO.getEdges(genere)
        self._pop = DAO.getPop(genere)
        # Iteriamo direttamente sugli oggetti Arco restituiti dal DAO
        for edge in edges:
            u = edge.a1  # Questo è l'oggetto Artista 1
            v = edge.a2  # Questo è l'oggetto Artista 2

            # Recuperiamo la popolarità usando gli ID numerici degli artisti
            up = self._pop.get(u.ArtistId, 0)
            vp = self._pop.get(v.ArtistId, 0)

            # Calcoliamo il peso totale
            peso_arco = up + vp

            # Gestione del verso basata sulla popolarità
            if up < vp:
                # Nota: u e v sono già oggetti Artista, li passiamo direttamente a NetworkX!
                self._graph.add_edge(u, v, weight=peso_arco)
            elif up > vp:
                self._graph.add_edge(v, u, weight=peso_arco)
            else:
                self._graph.add_edge(u, v, weight=peso_arco)
                self._graph.add_edge(v, u, weight=peso_arco)
        #CASO GESTITO CON LE TUPLE
        #for u, v in edges:
            #   up = self._pop[u.ArtistId] #A
             #  vp = self._pop[v.ArtistId] #B
              # if up < vp:
                  # self._graph.add_edge(self._idMapArtisti[u], self._idMapArtisti[v], weight=up + vp)
              # elif up > vp:
                   #self._graph.add_edge(self._idMapArtisti[v], self._idMapArtisti[u], weight=up + vp)
               #else:
                  # self._graph.add_edge(self._idMapArtisti[u], self._idMapArtisti[v], weight=up + vp)
                   #self._graph.add_edge(self._idMapArtisti[v], self._idMapArtisti[u], weight=up + vp)

    def getAllNodes(self):
        return list(self._graph.nodes())

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllGeneri(self):
        self._generi=DAO.getAllGeneri()
        return self._generi

    def getTop5Archi(self):
        return sorted(self._graph.edges(data=True),
                      key=lambda x: x[2]["weight"], reverse=True)[:5]

    def getArtistaPiuInfluente(self):
        miglior_artista = None
        max_influenza=-float('inf')
        for n in self._graph.nodes:
            # .out_degree(n, weight='weight') fa la somma automatica dei pesi di tutti gli archi in uscita da n
            peso_uscenti = self._graph.out_degree(n, weight='weight')

            # .in_degree(n, weight='weight') fa la somma automatica dei pesi di tutti gli archi in entrata a n
            peso_entranti = self._graph.in_degree(n, weight='weight')

            # 1. Calcoliamo la somma dei pesi degli archi USCENTI
           # peso_uscenti = 0
            #for u, v, data in self._graph.out_edges(n, data=True):
               # peso_uscenti += data.get("weight", 0)

            # 2. Calcoliamo la somma dei pesi degli archi ENTRANTI
           # peso_entranti = 0
           # for u, v, data in self._graph.in_edges(n, data=True):
           #     peso_entranti += data.get("weight", 0)

            # 3. L'influenza è la differenza tra i due pesi
            influenza = peso_uscenti - peso_entranti

            # Se questa influenza è maggiore di quella massima trovata finora, aggiorniamo il record
            if influenza > max_influenza:
                max_influenza = influenza
                miglior_artista = n

            # Restituiamo l'oggetto Artista migliore e il valore della sua influenza
        return miglior_artista, max_influenza