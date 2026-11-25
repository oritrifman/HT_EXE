from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class AboutWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About - Heat Transfer")
        self.setGeometry(820, 100, 420, 480)

        title_label = QLabel("Heat Transfer Simulation", self)
        title_label.setGeometry(0, 20, 420, 35)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: rgb(200, 60, 40);")

        self.image_label = QLabel(self)
        self.image_label.setGeometry(60, 70, 300, 180)
        pixmap = QPixmap("images/about.png")
        self.image_label.setPixmap(pixmap.scaled(300, 180, Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid rgb(200, 60, 40); border-radius: 8px;")

        info_label = QLabel("Simulation of heat conduction between two bodies.\n\n"
                            "Written by: Ori Trifman", self)
        info_label.setGeometry(30, 275, 360, 80)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 14px;")

        github_label = QLabel('<a style="color: rgb(0, 102, 204);" href="https://github.com/oritrifman/HT_EXE.git">Project on GitHub</a>', self)
        github_label.setGeometry(0, 370, 420, 30)
        github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        github_label.setOpenExternalLinks(True)
        github_label.setStyleSheet("font-size: 15px;")

        linkedin_label = QLabel('<a style="color: rgb(0, 102, 204);" href="https://www.linkedin.com/in/ori-trifman-7333b2233">My LinkedIn</a>', self)
        linkedin_label.setGeometry(0, 410, 420, 30)
        linkedin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        linkedin_label.setOpenExternalLinks(True)
        linkedin_label.setStyleSheet("font-size: 15px;")