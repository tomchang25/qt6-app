from PyQt6 import QtCore, QtGui, QtWidgets
from src.color import Color
from src.vertical_tab import TabWidget


class ProjectTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.projectSubmitSignal = QtCore.pyqtSignal(str)

        self.media_filename = None

        self.init_ui()

    def init_ui(self):
        self.filenameText = QtWidgets.QLineEdit()
        self.filenameText.setReadOnly(True)

        self.loadMediaButton = QtWidgets.QPushButton("Open File")
        self.loadMediaButton.clicked.connect(self.on_loadMediaButton_clicked)

        self.vocalExtractorCheckbox = QtWidgets.QCheckBox()
        self.vocalExtractorCheckbox.setText("Vocal Extractor")

        self.importMediaButton = QtWidgets.QPushButton("Import")
        self.importMediaButton.clicked.connect(self.on_importMediaButton_clicked)

        self.label2 = QtWidgets.QLabel("BBB")
        self.input2 = QtWidgets.QLineEdit()
        self.label3 = QtWidgets.QLabel("CCC")
        self.input3 = QtWidgets.QPlainTextEdit()

        tabLayout = QtWidgets.QGridLayout()
        tabLayout.addWidget(self.filenameText, 0, 0, 1, 5)
        tabLayout.addWidget(self.loadMediaButton, 0, 5, 1, 1)

        tabLayout.addWidget(self.vocalExtractorCheckbox, 1, 2, 1, 3)
        tabLayout.addWidget(self.importMediaButton, 1, 5, 1, 1)

        tabLayout.addWidget(self.label3, 2, 0, 1, 1)
        tabLayout.addWidget(self.input3, 2, 1, 1, 5)

        buttonLayout = QtWidgets.QHBoxLayout()
        saveButton = QtWidgets.QPushButton("Save")
        cancelButton = QtWidgets.QPushButton("Clear")
        buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(cancelButton)

        tabLayout.addLayout(buttonLayout, 3, 5, QtCore.Qt.AlignmentFlag.AlignRight)

        self.setLayout(tabLayout)

    @QtCore.pyqtSlot()
    def on_loadMediaButton_clicked(self):
        mediaFileDialog = QtWidgets.QFileDialog(
            self,
            "Select one or more files to open",
        )
        mediaFileDialog.setNameFilters(
            [
                "All Files (*)",
                "Media Files (*.mp4 *.avi *.mp3 *.wav)",
                "Video Files (*.mp4 *.avi)",
                "Audio Files (*.mp3 *.wav)",
            ]
        )
        mediaFileDialog.selectNameFilter("Media Files (*.mp4 *.avi *.mp3 *.wav)")

        if mediaFileDialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.media_filename = mediaFileDialog.selectedFiles()[0]
            self.filenameText.setText(self.media_filename)
        else:
            self.media_filename = None

    @QtCore.pyqtSlot()
    def on_importMediaButton_clicked(self):
        if self.media_filename is None:
            return

        self.importMediaButton.setEnabled(False)

        # TODO:Use ffmpeg extract to mp3 and check vocal_extractor then use demucs
        self.vocalExtractorCheckbox

        QtCore.QTimer.singleShot(5000, lambda: self.importMediaButton.setEnabled(True))


class TranscribeTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Add widgets and functionality for the Transcribe tab
        # ...


class TranslateTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Add widgets and functionality for the Translate tab
        # ...


class Template(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.subtitle_changed = QtCore.pyqtSignal(str)

        self.setWindowTitle("app")
        self.resize(640, 480)

        self.init_ui()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        tab_widget = TabWidget()

        # Create the Transcribe and Translate tabs
        self.project_tab = ProjectTab()
        self.transcribe_tab = TranscribeTab()
        self.translate_tab = TranslateTab()

        # Connect the subtitle_changed signal in the Transcribe tab to the subtitle_changed signal in the MainWindow
        # self.transcribe_tab.subtitle_changed.connect(self.subtitle_changed)

        # Connect the subtitle_changed signal in the MainWindow to the update_subtitle slot in the Translate tab
        # self.subtitle_changed.connect(self.translate_tab.update_subtitle)

        # Add the tabs to the tab widget
        tab_widget.addTab(self.project_tab, QtGui.QIcon("files/project.png"), "Project")
        tab_widget.addTab(self.transcribe_tab, QtGui.QIcon("files/transcribe.png"), "Transcribe")
        tab_widget.addTab(self.translate_tab, QtGui.QIcon("files/translate.png"), "Translate")

        # Add the tab widget to the main layout
        main_layout.addWidget(tab_widget)

        # Set the main layout of the window
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle("Oxygen")
    window = Template()
    window.show()
    sys.exit(app.exec())
