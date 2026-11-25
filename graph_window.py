from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QComboBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import os

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
        self.draw_button.clicked.connect(self.draw_clicked)
        self.clear_button.clicked.connect(self.clear_clicked)
        self.export_button.clicked.connect(self.export_clicked)

    def style_axes(self):
        self.ax.set_title("Body Temperature over Time", fontsize=13, color=(0.2, 0.2, 0.3))
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, linestyle="--", alpha=0.4)
        for spine in ["top", "right"]:
            self.ax.spines[spine].set_visible(False)
        self.canvas.draw()

    def draw_clicked(self):
        if self.body_combo.currentIndex() == 0:
            temperatures = self.main_window.left_temp_list
            color = "red"
        else:
            temperatures = self.main_window.right_temp_list
            color = "blue"
        self.ax.plot(self.main_window.time_list, temperatures, color=color, linewidth=2,
                     label=self.body_combo.currentText())
        self.ax.legend()
        self.canvas.draw()

    def clear_clicked(self):
        self.ax.clear()
        self.style_axes()

    def export_clicked(self):
        file_name = "heat_transfer_results.csv"
        try:
            with open(file_name, "w") as f:
                f.write("Time (s),Body 1 temperature (C),Body 2 temperature (C)\n")
                for i in range(len(self.main_window.time_list)):
                    f.write(f"{self.main_window.time_list[i]:.2f},"
                            f"{self.main_window.left_temp_list[i]:.3f},"
                            f"{self.main_window.right_temp_list[i]:.3f}\n")
            if os.name == "nt":
                os.startfile(file_name)
            else:
                print(f"File saved: {file_name}")
        except PermissionError:
            print("Close the CSV file in Excel and try again")