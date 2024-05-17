import json
from PyQt6.QtCore import QObject, pyqtSignal

class ListModel(QObject):
    list_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.data = {}

    def create_list(self, nom, date):
        self.data = {
            'listname': nom,
            'listdate': date,
            'items': []
        }
        self.save_list(f"{nom}.json")

    def open_list(self, filename):
        with open(filename, 'r') as file:
            self.data = json.load(file)
        self.list_updated.emit()

    def save_list(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)

    def add_items(self, items):
        self.data['items'].extend(items)
        self.data['items'] = list(set(self.data['items']))  # Remove duplicates
        self.list_updated.emit()
