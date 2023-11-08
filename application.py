import sys
import os
import logging
from PyQt5 import QtWidgets, QtCore

from trebuchet import run_design, load_design, validate_design


class TrebuchetApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.design = None
        self.data_out = None
        self.browser = 'firefox'

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Virtual Trebuchet Automator")
        self.setGeometry(100, 100, 400, 200)

        self.file_drop = DropSection()
        self.file_drop.file_drop_completed.connect(self.on_file_dropped)
        self.file_upload_label = QtWidgets.QLabel("File Uploaded: ")
        self.run_button = QtWidgets.QPushButton("Run")
        self.run_button.setEnabled(False)
        self.download_button = QtWidgets.QPushButton("Download Results")
        self.download_button.setEnabled(False)
        self.footer = QtWidgets.QLabel("Please Upload A Design File Above")
        self.footer.setStyleSheet("font-size: 10px;")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.file_drop)
        layout.addWidget(self.file_upload_label)
        layout.addWidget(self.run_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.footer)

        self.setLayout(layout)

        self.run_button.clicked.connect(self.click_run)
        self.download_button.clicked.connect(self.click_download)

    def click_run(self):
        try:
            self.footer.setText("Running Design...")
            self.footer.setStyleSheet('color: white;')
            self.download_button.setEnabled(False)
            self.data_out = run_design(self.design, self.browser)
            self.download_button.setEnabled(True)
            self.footer.setText("Design Complete")
        except KeyError:
            self.footer.setText("Error: Design has invalid variable names")
            self.footer.setStyleSheet('color: red;')
            self.file_upload_label.setText("File Uploaded: ")

    def click_download(self):
        default_filename = os.path.basename(self.file_drop.design_path)
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save to Excel", default_filename,
                                                          "Excel Files (*.xlsx);;All Files (*)")[0]
        self.data_out.to_excel(file_path, index=False)
        self.footer.setText('Download Complete')

    def on_file_dropped(self):
        try:
            self.design = load_design(self.file_drop.design_path)
            is_valid, error = validate_design(self.design)
            if not is_valid:
                self.footer.setText(f'{error}')
                self.footer.setStyleSheet('color: red;')
                self.run_button.setEnabled(False)
                self.file_upload_label.setText("File Uploaded: ")
            else:
                self.file_upload_label.setText(f"File Uploaded: {os.path.basename(self.file_drop.design_path)}")
                self.run_button.setEnabled(True)
                self.footer.setText("Upload Successful")
                self.footer.setStyleSheet('color: white;')
        except ValueError:
            self.design = None
            self.footer.setText(f'Invalid format. Please upload an Excel file')
            self.footer.setStyleSheet('color: red;')
            self.run_button.setEnabled(False)
            self.file_upload_label.setText("File Uploaded: ")


class DropSection(QtWidgets.QWidget):
    file_drop_completed = QtCore.pyqtSignal()

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
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.design_path = event.mimeData().urls()[0].toLocalFile()
        self.file_drop_completed.emit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    trebuchet = TrebuchetApp()
    trebuchet.show()
    sys.exit(app.exec_())
