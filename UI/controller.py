import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):

        generi = self._model.getAllGeneri()

        for g in generi:
            g_str= str(g)
            #self._view._ddGenre.options.append( g_str)
            self._view._ddGenre.options.append(ft.dropdown.Option(key=g_str, text=g_str))

        self._view.update_page()

    def fillDDArtisti(self):
        self._view._ddArtist.options.clear()
        artisti = self._model.getAllNodes()

        for g in artisti:
            g_str= str(g)
            #self._view._ddGenre.options.append( g_str)
            self._view._ddArtist.options.append(ft.dropdown.Option(key=g_str, text=g_str))

        self._view.update_page()


    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._view._ddGenre.value)
        Nnodes, Nedges = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grapfo correttamente creato. "
                                                      f"Il grafo contiene {Nnodes} nodi e {Nedges} archi"))

   # def handleDettagli(self, e):
        top5 = self._model.getTop5Archi()
       # self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore: "))

        for arco in top5:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))

        artista_top, influenza_top = self._model.getArtistaPiuInfluente()
       # self._view.txt_result.controls.clear()
        if artista_top:
            self._view.txt_result.controls.append(
                ft.Text(f"L'artista più influente è: {artista_top.Name} (Influenza: {influenza_top})")
            )
        self.fillDDArtisti()

    def  handleCammino(self,e):
        id_artista = self._view._ddArtist.value

        if not id_artista:
            self._view.create_alert("Per favore, seleziona un artista di partenza!")
            return
        # Recuperiamo l'oggetto Artista corrispondente usando la idMap salvata nel model
        artista_partenza = self._model._idMapArtisti[int(id_artista)]

        # 2. Calcoliamo il cammino massimo
        cammino = self._model.getCamminoMassimo(artista_partenza)
        self._view.txt_result.controls.append(
            ft.Text(f"\nCammino massimo trovato (Lunghezza: {len(cammino) - 1} archi):"))

        for i in range(len(cammino)):
            if i == 0:
                self._view.txt_result.controls.append(ft.Text(f"Partenza: {cammino[i].Name}"))
            else:
                # Recuperiamo il peso dell'arco tra il nodo precedente e quello attuale
                u = cammino[i - 1]
                v = cammino[i]
                peso = self._model._graph[u][v]["weight"]
                self._view.txt_result.controls.append(ft.Text(f" --> {v.Name} (peso arco: {peso})"))
        self._view.update_page()