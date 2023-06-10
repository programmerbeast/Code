from PySide6.QtWidgets import QApplication, QMainWindow, QProgressBar, QLabel


class ProgressBarWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Progress Bar")

        # Create a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(30, 40, 200, 25)

        # Create a label to display the progress value
        self.progress_label = QLabel(self)
        self.progress_label.setGeometry(30, 40, 200, 25)

        self.progress_label2 = QLabel("Downloading reviews, please wait", self)
        self.progress_label2.setGeometry(0, 0, 200, 25)

        self.show()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"{value}%")
        QApplication.processEvents()
