from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSlider, QDoubleSpinBox
from PySide6.QtCore import Qt , QTimer
from about_window import AboutWindow
from graph_window import GraphWindow
from Body import Body



class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = AboutWindow()
        self.graph_window = GraphWindow(self)
        self.dt = 0.1
        self.time = 0
        self.time_list = []
        self.left_temp_list = []
        self.right_temp_list = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_method)

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer Simulation")
        self.setGeometry(100, 100, 700, 450)

        # ----- title -----
        title_label = QLabel("Heat Transfer Between Two Bodies", self)
        title_label.setGeometry(0, 15, 700, 30)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: rgb(40, 40, 60);")

        # ----- left body: slider + color square -----
        self.left_temp_slider = QSlider(Qt.Orientation.Vertical, self)
        self.left_temp_slider.setGeometry(40, 70, 30, 200)
        self.left_temp_slider.setRange(0, 200)
        self.left_temp_slider.setValue(200)
        self.left_temp_slider.valueChanged.connect(self.left_temperature_changed)

        self.left_body_label = QLabel(self)
        self.left_body_label.setGeometry(90, 70, 150, 200)
        self.left_body_label.setStyleSheet("background-color: rgb(255, 0, 0); border: 2px solid rgb(60, 60, 60); border-radius: 10px;")

        # ----- the bar between the bodies -----
        bridge_label = QLabel(self)
        bridge_label.setGeometry(240, 160, 220, 40)
        bridge_label.setStyleSheet("background-color: rgb(170, 170, 170);")

        # ----- right body: color square + slider -----
        self.right_body_label = QLabel(self)
        self.right_body_label.setGeometry(460, 70, 150, 200)
        self.right_body_label.setStyleSheet("background-color: rgb(0, 0, 0); border: 2px solid rgb(60, 60, 60); border-radius: 10px;")

        self.right_temp_slider = QSlider(Qt.Orientation.Vertical, self)
        self.right_temp_slider.setGeometry(630, 70, 30, 200)
        self.right_temp_slider.setRange(0, 200)
        self.right_temp_slider.setValue(0)
        self.right_temp_slider.valueChanged.connect(self.right_temperature_changed)
        
        # ----- conductivity (above the bar) -----
        conductivity_label = QLabel("Conductivity", self)
        conductivity_label.setGeometry(290, 85, 120, 20)
        conductivity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.conductivity_spin = QDoubleSpinBox(self)
        self.conductivity_spin.setGeometry(290, 110, 120, 30)
        self.conductivity_spin.setRange(0.01, 100)
        self.conductivity_spin.setValue(1.0)
        self.conductivity_spin.setSuffix(" W/°C")

        # ----- left body data -----
        left_temp_text = QLabel("Temp.", self)
        left_temp_text.setGeometry(20, 295, 70, 30)

        self.left_temp_display = QLabel("200.0 °C", self)
        self.left_temp_display.setGeometry(100, 295, 140, 30)
        self.left_temp_display.setStyleSheet("background-color: white; color: black; border: 1px solid gray; padding-left: 5px;")

        left_mass_text = QLabel("Mass", self)
        left_mass_text.setGeometry(20, 340, 70, 30)

        self.left_mass_spin = QDoubleSpinBox(self)
        self.left_mass_spin.setGeometry(100, 340, 140, 30)
        self.left_mass_spin.setRange(0.01, 1000)
        self.left_mass_spin.setValue(10)
        self.left_mass_spin.setSuffix(" kg")

        left_heat_capacity_text = QLabel("H. Cap.", self)
        left_heat_capacity_text.setGeometry(20, 385, 70, 30)

        self.left_heat_capacity_spin = QDoubleSpinBox(self)
        self.left_heat_capacity_spin.setGeometry(100, 385, 140, 30)
        self.left_heat_capacity_spin.setRange(0.01, 10000)
        self.left_heat_capacity_spin.setValue(0.4)
        self.left_heat_capacity_spin.setSuffix(" J/kg°C")

        # ----- right body data -----
        self.right_temp_display = QLabel("0.0 °C", self)
        self.right_temp_display.setGeometry(460, 295, 140, 30)
        self.right_temp_display.setStyleSheet("background-color: white; color: black; border: 1px solid gray; padding-left: 5px;")

        right_temp_text = QLabel("Temp.", self)
        right_temp_text.setGeometry(610, 295, 70, 30)

        self.right_mass_spin = QDoubleSpinBox(self)
        self.right_mass_spin.setGeometry(460, 340, 140, 30)
        self.right_mass_spin.setRange(0.01, 1000)
        self.right_mass_spin.setValue(10)
        self.right_mass_spin.setSuffix(" kg")

        right_mass_text = QLabel("Mass", self)
        right_mass_text.setGeometry(610, 340, 70, 30)

        self.right_heat_capacity_spin = QDoubleSpinBox(self)
        self.right_heat_capacity_spin.setGeometry(460, 385, 140, 30)
        self.right_heat_capacity_spin.setRange(0.01, 10000)
        self.right_heat_capacity_spin.setValue(0.4)
        self.right_heat_capacity_spin.setSuffix(" J/kg°C")

        right_heat_capacity_text = QLabel("H. Cap.", self)
        right_heat_capacity_text.setGeometry(610, 385, 70, 30)

        # ----- buttons (middle) -----
        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(300, 295, 100, 35)
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.start_stop)

        self.graphs_button = QPushButton("Graphs", self)
        self.graphs_button.setGeometry(300, 340, 100, 35)
        self.graphs_button.clicked.connect(self.graphs_clicked)

        self.about_button = QPushButton("About", self)
        self.about_button.setGeometry(300, 385, 100, 35)
        self.about_button.clicked.connect(self.about_clicked)

    def about_clicked(self):
        self.about_window.show()

    def left_temperature_changed(self, value):
        self.left_temp_display.setText(f"{value:.1f} °C")
        red = int(value / 200 * 255)
        self.left_body_label.setStyleSheet(f"background-color: rgb({red}, 0, 0); border: 2px solid rgb(60, 60, 60); border-radius: 10px;")

    def right_temperature_changed(self, value):
        self.right_temp_display.setText(f"{value:.1f} °C")
        red = int(value / 200 * 255)
        self.right_body_label.setStyleSheet(f"background-color: rgb({red}, 0, 0); border: 2px solid rgb(60, 60, 60); border-radius: 10px;")

    def start_stop(self, checked):
        if checked:
            self.left_body = Body(self.left_mass_spin.value(), self.left_heat_capacity_spin.value(),
                                self.left_temp_slider.value())
            self.right_body = Body(self.right_mass_spin.value(), self.right_heat_capacity_spin.value(),
                                self.right_temp_slider.value())
            self.time = 0
            self.time_list = [0]
            self.left_temp_list = [self.left_body.temperature]
            self.right_temp_list = [self.right_body.temperature]
            self.start_button.setText("Stop")
            self.timer.start(100)
        else:
            self.timer.stop()
            self.start_button.setText("Start")

        for widget in [self.left_temp_slider, self.right_temp_slider, self.left_mass_spin, self.right_mass_spin,
                    self.left_heat_capacity_spin, self.right_heat_capacity_spin, self.conductivity_spin]:
            widget.setEnabled(not checked)

    def timer_method(self):
        heat_current = self.conductivity_spin.value() * (self.right_body.temperature - self.left_body.temperature)
        heat = heat_current * self.dt
        left_temperature = self.left_body.add_heat(heat)
        right_temperature = self.right_body.add_heat(-heat)

        self.time = self.time + self.dt
        self.time_list.append(self.time)
        self.left_temp_list.append(left_temperature)
        self.right_temp_list.append(right_temperature)

        self.left_temp_slider.setValue(int(left_temperature))
        self.right_temp_slider.setValue(int(right_temperature))
        self.left_temperature_changed(left_temperature)
        self.right_temperature_changed(right_temperature)

    def graphs_clicked(self):
        self.graph_window.show()

    def closeEvent(self, event):
        self.about_window.close()
        self.graph_window.close()


if __name__ == "__main__":
    app = QApplication()
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = HeatTransfer()
    window.show()
    app.exec()