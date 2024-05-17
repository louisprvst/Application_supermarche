import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QFileDialog, QWidget, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QDialogButtonBox, QDockWidget, QTextEdit
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

class PopupInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('A propos')
        self.setGeometry(100, 100, 300, 150)
        self.name = QLabel("Application item finder.")
        layout = QVBoxLayout()
        layout.addWidget(self.name)
        self.setLayout(layout)

class PopupNewList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Création de liste')
        self.setGeometry(100, 100, 300, 150)
        self.nom_input = QLineEdit()
        self.date_input = QDateEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Nom de la liste :'))
        layout.addWidget(self.nom_input)
        layout.addWidget(QLabel('Date de vos courses :'))
        layout.addWidget(self.date_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Item Finder")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/'))

        menu_bar = self.menuBar()
        menu_Fichiers = menu_bar.addMenu('&Fichier')
        menu_Listes = menu_bar.addMenu('&Listes')
        menu_help = menu_bar.addMenu('&Aides')

        self.toolbar = QToolBar('Tool Bar')
        self.addToolBar(self.toolbar)

        self.json_display = QTextEdit()
        self.json_display.setPlaceholderText("Veuillez choisir un fichier liste.json ou en créer un ...")
        self.json_display.setReadOnly(True)

        self.user_input = QTextEdit()
        self.user_input.setPlaceholderText("Entrez votre liste ici...")
        self.user_input.setMinimumHeight(700)
        self.user_input.setMaximumHeight(700)

        self.dock_list = QDockWidget('Ma liste :', self)
        self.dock_list.setWidget(self.json_display)
        self.dock_list.setMaximumWidth(200)

        layout = QVBoxLayout()
        layout.addWidget(self.json_display)
        layout.addWidget(QLabel("Entrez vos articles :"))
        layout.addWidget(self.user_input)

        widget = QWidget()
        widget.setLayout(layout)
        self.dock_list.setWidget(widget)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_list)
        self.dock_list.setMinimumWidth(200)

        self.showMaximized()

    def update_view(self, data):
        formatted_data = f"\n Nom : {data['listname']} \n\n Date : {data['listdate']}\n\n Items : {', '.join(data.get('items', []))}"
        self.json_display.setPlainText(formatted_data)
