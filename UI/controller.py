import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._artistaValue = None

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        try:
            self._model.buildGraph()

            self._view._txt_result.controls.append(
                ft.Text("Grafo correttamente creato.")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero nodi: {self._model.getNumNodi()}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero archi: {self._model.getNumEdges()}")
            )
            self.fillDDArtisti()

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        try:
            best_degree, max_degree = self._model.getArtistWithMaxDegree()
            if best_degree:
                self._view._txt_result.controls.append(
                    ft.Text(f"Artista con grado maggiore: {best_degree} (grado: {max_degree})")
                )

            best_weight, max_weight = self._model.getArtistWithMaxWeightSum()
            if best_weight:
                self._view._txt_result.controls.append(
                    ft.Text(f"Artista con somma pesi incidenti massima: {best_weight} (somma: {max_weight})")
                )

            top10 = self._model.getTop10Edges()
            if top10:
                self._view._txt_result.controls.append(
                    ft.Text("Top 10 archi con peso maggiore:")
                )
                for i, (u, v, weight) in enumerate(top10, 1):
                    self._view._txt_result.controls.append(
                        ft.Text(f"{i}. {u} -- {v} (peso: {weight})")
                    )
            else:
                self._view._txt_result.controls.append(
                    ft.Text("Nessun arco trovato.")
                )

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella stampa delle info: {ex}")

    def handleSelezione(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        if self._artistaValue is None:
            self._view.create_alert("Selezionare un artista dal menu a tendina.")
            return

        try:
            N = int(self._view._txtInN.value)
        except (ValueError, TypeError):
            self._view.create_alert("Inserisci un valore numerico valido per N.")
            return

        if N <= 0:
            self._view.create_alert("N deve essere un intero positivo.")
            return

        try:
            best_group, total_tracks = self._model.getBestGroup(self._artistaValue, N)

            if not best_group:
                self._view._txt_result.controls.append(
                    ft.Text("Nessun gruppo trovato.")
                )
                self._view.update_page()
                return

            sorted_group = sorted(best_group, key=lambda a: a.Name)

            self._view._txt_result.controls.append(
                ft.Text("Lista degli artisti selezionati:")
            )
            self._view._txt_result.controls.append(ft.Text(""))

            for artist in sorted_group:
                num_albums = self._model.getNumAlbumsForArtist(artist.ArtistId)
                num_tracks = len(artist.Tracks)
                num_playlists = len(artist.Playlists)
                self._view._txt_result.controls.append(
                    ft.Text(
                        f"  - {artist}: album: {num_albums}, "
                        f"brani: {num_tracks}, playlist: {num_playlists}"
                    )
                )

            self._view._txt_result.controls.append(ft.Text(""))
            self._view._txt_result.controls.append(
                ft.Text(f"Numero totale di artisti selezionati: {len(best_group)}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero complessivo di brani: {total_tracks}")
            )

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella ricerca del gruppo: {ex}")

    def fillDDArtisti(self):
        self._view._ddArtista.options.clear()
        all_artists = self._model.getAllArtists()

        artistsDDOptions = list(
            map(
                lambda x: ft.dropdown.Option(data=x, key=str(x), on_click=self._choiceArtista),
                all_artists
            )
        )
        self._view._ddArtista.options = artistsDDOptions
        self._view.update_page()

    def _choiceArtista(self, e):
        self._artistaValue = e.control.data
