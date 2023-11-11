import sys
import os
import logging
from PyQt5 import QtWidgets, QtCore
from pandas import DataFrame

from trebuchet import run_design, load_design, validate_design


class TrebuchetApp(QtWidgets.QWidget):
    supported_browsers = {'Firefox', 'Chrome'}

    def __init__(self):
        super().__init__()
        self.design = None
        self.data_out = None
        self.browser = 'firefox'
        self.design_runner = None

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Virtual Trebuchet Automator")
        self.setGeometry(100, 100, 400, 200)

        self.file_drop = DropSection()
        self.file_drop.file_drop_completed.connect(self.on_file_dropped)
        self.file_upload_label = QtWidgets.QLabel("File Uploaded: ")
        self.run_button = QtWidgets.QPushButton("Run")
        self.run_button.setEnabled(False)
        self.browser_label = QtWidgets.QLabel("Select Browser:")
        self.browser_combo = QtWidgets.QComboBox()
        self.browser_combo.addItems(self.supported_browsers)
        self.browser_combo.setCurrentText('Firefox')
        self.download_button = QtWidgets.QPushButton("Download Results")
        self.download_button.setEnabled(False)
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.footer = QtWidgets.QLabel("Upload A Design File Above")
        self.footer.setStyleSheet("font-size: 10px;")

        run_browser_layout = QtWidgets.QHBoxLayout()
        run_browser_layout.addWidget(self.run_button)
        run_browser_layout.addWidget(self.browser_label)
        run_browser_layout.addWidget(self.browser_combo)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(run_browser_layout)
        layout.addWidget(self.file_drop)
        layout.addWidget(self.file_upload_label)
        layout.addWidget(self.download_button)
        layout.addWidget(line)
        layout.addWidget(self.footer)

        self.setLayout(layout)

        self.run_button.clicked.connect(self.click_run)
        self.download_button.clicked.connect(self.click_download)

    def click_run(self):
        self.browser = self.browser_combo.currentText().lower()
        self.footer.setText("Running Design...")
        self.footer.setStyleSheet('color: white; font-size: 10px;')
        self.download_button.setEnabled(False)

        self.design_runner = DesignRunner(self.design, self.browser)
        self.design_runner.design_completed.connect(self.on_design_completed)
        self.design_runner.start()

    def click_download(self):
        default_filename = os.path.basename(self.file_drop.design_path)
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save to Excel", default_filename,
                                                          "Excel Files (*.xlsx);;All Files (*)")[0]
        if not file_path:
            return
        
        self.data_out.to_excel(file_path, index=False)
        self.footer.setText('Download Complete')

    def on_file_dropped(self):
        try:
            self.design = load_design(self.file_drop.design_path)
            is_valid, error = validate_design(self.design)
            if not is_valid:
                self.footer.setText(f'{error}')
                self.footer.setStyleSheet('color: red; font-size: 10px;')
                self.run_button.setEnabled(False)
                self.run_button.setStyleSheet('')
                self.file_upload_label.setText("File Uploaded: ")
            else:
                self.file_upload_label.setText(f"File Uploaded: {os.path.basename(self.file_drop.design_path)}")
                self.run_button.setEnabled(True)
                self.run_button.setStyleSheet('background-color: #65C1FF;')
                self.footer.setText("Upload Successful")
                self.footer.setStyleSheet('color: white; font-size: 10px;')
        except ValueError:
            self.design = None
            self.footer.setText(f'Invalid format. Please upload an Excel file')
            self.footer.setStyleSheet('color: red; font-size: 10px;')
            self.run_button.setEnabled(False)
            self.run_button.setStyleSheet('')
            self.file_upload_label.setText("File Uploaded: ")

    def on_design_completed(self, data_out: DataFrame):
        if data_out is not None:
            self.download_button.setEnabled(True)
            self.footer.setText("Design Complete")
            self.data_out = data_out
        else:
            self.footer.setText("An error occurred during the run, please see log file")
            self.footer.setStyleSheet('color: red; font-size: 10px;')


class DropSection(QtWidgets.QWidget):
    file_drop_completed = QtCore.pyqtSignal()
    valid_ext = ('xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt')

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
        if self.design_path.lower().endswith(self.valid_ext):
            self.file_drop_completed.emit()


class DesignRunner(QtCore.QThread):
    design_completed = QtCore.pyqtSignal(object)

    def __init__(self, design, browser):
        super().__init__()
        self.design = design
        self.browser = browser

    def run(self):
        try:
            result = run_design(self.design, self.browser)
            self.design_completed.emit(result)
        except Exception as e:
            logging.exception(f"An error occurred in DesignRunner: {str(e)}")
            self.design_completed.emit(None)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    trebuchet = TrebuchetApp()
    trebuchet.show()
    sys.exit(app.exec_())
