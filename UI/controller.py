import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):

        voto1 = self._model.getRating()
        voto2 = self._model.getRating()

        for v in voto1:
            self._view._ddrating1.options.append(ft.dropdown.Option(v))
        for v in voto2:
            self._view._ddrating2.options.append(ft.dropdown.Option(v))

        self._view._page.update()

    def handleCreaGrafo(self, e):
        voto1 = self._view._ddrating1.value
        voto2 = self._view._ddrating2.value

        self._model.buildGraph(voto1, voto2)

        if voto1 is None or voto2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare dei voti"))
            self._view._page.update()
            return
        if voto1 > voto2:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append("Il voto1 deve essere minore del voto2", color="red")
            self._view._page.update()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumEdges()}"))
        self._view._page.update()

        top5 = self._model.getTop5()
        self._view.txt_result.controls.append(ft.Text("Top 5 archi"))

        for u, v, peso in top5:

            self._view.txt_result.controls.append(ft.Text(f"{u.name} -> {v.name} : {peso["weight"]}"))
            self._view._page.update()

        numero, largest = self._model.getCompConnesse()

        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numero} componenti connesse"))
        self._view.txt_result.controls.append(ft.Text(f"La più grande è lunga {len(largest)}"))
        for l in largest:
            self._view.txt_result.controls.append(ft.Text(str(l)))
            self._view._page.update()





    def handleCammino(self, e):
        pass