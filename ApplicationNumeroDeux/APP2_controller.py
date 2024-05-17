import sys
from PyQt6.QtWidgets import QApplication , QFileDialog
from PyQt6.QtGui import QAction
from APP2_model import ListModel
from APP2_vue import MainView, PopupInfo, PopupNewList

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.toolbar.addAction(self.create_action('Choisir un magasin', self.open_list, 'Ctrl+O'))
        self.view.toolbar.addAction(self.create_action('Nouvelle liste', self.new_list, 'Ctrl+L'))
        self.view.toolbar.addAction(self.create_action('Ouvrir une liste', self.open_list, 'Ctrl+P'))
        self.view.toolbar.addAction(self.create_action('Sauvegarder une liste', self.save_list, 'Ctrl+A'))
        self.view.toolbar.addAction(self.create_action('A propos', self.show_info, 'Ctrl+I'))

        self.model.list_updated.connect(self.update_view)

    def create_action(self, name, method, shortcut=None):
        action = QAction(name, self.view)
        action.triggered.connect(method)
        if shortcut:
            action.setShortcut(shortcut)
        return action

    def open_list(self):
        filename, _ = QFileDialog.getOpenFileName(self.view, "Choisir un fichier liste :", filter="JSON (*.json)")
        if filename:
            self.model.open_list(filename)

    def new_list(self):
        self.popup = PopupNewList()
        self.popup.buttons.accepted.connect(self.create_list)
        self.popup.buttons.rejected.connect(self.popup.close)
        self.popup.show()

    def create_list(self):
        nom = self.popup.nom_input.text()
        date = self.popup.date_input.text()
        self.model.create_list(nom, date)
        self.popup.close()

    def save_list(self):
        items = [item.strip() for item in self.view.user_input.toPlainText().split(",")]
        self.model.add_items(items)
        self.model.save_list(self.model.data['listname'] + ".json")

    def show_info(self):
        self.popup = PopupInfo()
        self.popup.show()

    def update_view(self):
        self.view.update_view(self.model.data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = ListModel()
    view = MainView()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec())
