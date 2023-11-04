import sys
import logging
from PyQt5 import QtWidgets, QtCore

from trebuchet import run_design


class TrebuchetApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.design_path = None
        self.browser = 'firefox'

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Virtual Trebuchet Automator")
        self.setGeometry(100, 100, 400, 200)

        self.file_drop = DropSection()
        self.last_uploaded = QtWidgets.QLabel("File Uploaded: ")
        self.run_button = QtWidgets.QPushButton("Run")
        self.results_button = QtWidgets.QPushButton("Download Results")
        self.results_button.setEnabled(False)
        self.footer = QtWidgets.QLabel("Please Upload A Design File Above")
        self.footer.setStyleSheet("font-size: 10px;")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.file_drop)
        layout.addWidget(self.last_uploaded)
        layout.addWidget(self.run_button)
        layout.addWidget(self.results_button)
        layout.addWidget(self.footer)

        self.setLayout(layout)

        self.run_button.clicked.connect(self.run_function)
        self.results_button.clicked.connect(self.download_results)

    def run_function(self):
        try:
            self.footer.setText("Running Design...")
            run_design(self.file_drop.design_path, self.browser)
        except KeyError:
            self.footer.setText("Error: Design has invalid variable names")
            self.footer.setStyleSheet('color: red;')

    def download_results(self):
        # Simulate downloading results to a file
        file_dialog = QtWidgets.QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt)")
        selected_file = file_dialog[0]
        if selected_file:
            with open(selected_file, 'w') as file:
                file.write(f"Results from {self.iteration_count} iterations")


class DropSection(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: lightgray;")
        self.setAcceptDrops(True)
        self.setupUI()

        self.design_path = None

    def setupUI(self):
        self.upload_label = QtWidgets.QLabel("Drag and drop design file here")
        self.upload_label.setStyleSheet("color: black;")
        self.upload_label.setAlignment(QtCore.Qt.AlignCenter)
        self.upload_label.setContentsMargins(20, 20, 20, 20)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.upload_label)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = event.mimeData().urls()
        file_paths = [url.toLocalFile() for url in files]
        if file_paths:
            for file_path in file_paths:
                print(f"File dropped on section: {file_path}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    trebuchet = TrebuchetApp()
    trebuchet.show()
    sys.exit(app.exec_())
