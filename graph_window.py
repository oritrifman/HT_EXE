from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QComboBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class GraphWindow(QWidget):

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graph - Heat Transfer")
        self.setGeometry(820, 100, 720, 470)

        # ----- the graph (matplotlib inside the window) -----
        self.figure = Figure(facecolor=(0.94, 0.95, 0.96))
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(10, 10, 520, 450)
        self.style_axes()

        # ----- controls on the right -----
        body_text = QLabel("Body to plot:", self)
        body_text.setGeometry(550, 30, 150, 25)

        self.body_combo = QComboBox(self)
        self.body_combo.setGeometry(550, 60, 150, 30)
        self.body_combo.addItems(["Body 1 (left)", "Body 2 (right)"])

        self.draw_button = QPushButton("Draw", self)
        self.draw_button.setGeometry(550, 110, 150, 35)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(550, 155, 150, 35)

        self.export_button = QPushButton("Export to CSV", self)
        self.export_button.setGeometry(550, 200, 150, 35)

    def style_axes(self):
        self.ax.set_title("Body Temperature over Time", fontsize=13, color=(0.2, 0.2, 0.3))
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, linestyle="--", alpha=0.4)
        for spine in ["top", "right"]:
            self.ax.spines[spine].set_visible(False)
        self.canvas.draw()