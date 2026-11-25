from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDoubleSpinBox, QComboBox
from PySide6.QtCore import Qt, QTimer
from about_window import AboutWindow
from graph_window import GraphWindow
from Body import Body
from candle_slider import CandleSlider

class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = AboutWindow()
        self.graph_window = GraphWindow(self)
        self.materials = {"Custom": None, "Copper": 0.385, "Aluminum": 0.900, "Iron": 0.450,
                          "Gold": 0.129, "Glass": 0.840, "Water": 4.186}
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
        self.setGeometry(100, 100, 700, 530)

        # ----- title -----
        title_label = QLabel("Heat Transfer Between Two Bodies", self)
        title_label.setGeometry(0, 15, 700, 30)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: rgb(255, 200, 90);")

        # ----- left body: slider + color square -----
        self.left_temp_slider = CandleSlider(self)
        self.left_temp_slider.setGeometry(25, 60, 55, 215)
        self.left_temp_slider.setRange(0, 200)
        self.left_temp_slider.setValue(200)
        self.left_temp_slider.valueChanged.connect(self.left_temperature_changed)

        self.left_body_label = QLabel(self)
        self.left_body_label.setGeometry(90, 70, 150, 200)
        self.left_body_label.setStyleSheet("background-color: rgb(255, 0, 0); border: 2px solid rgb(60, 60, 60); border-radius: 10px;")

        # ----- the bar between the bodies -----
        bridge_label = QLabel(self)
        bridge_label.setGeometry(240, 160, 220, 40)
        bridge_label.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(140, 80, 35), stop:0.5 rgb(230, 160, 90), stop:1 rgb(140, 80, 35)); border-radius: 6px;")

        # ----- right body: color square + slider -----
        self.right_body_label = QLabel(self)
        self.right_body_label.setGeometry(460, 70, 150, 200)
        self.right_body_label.setStyleSheet("background-color: rgb(0, 0, 0); border: 2px solid rgb(60, 60, 60); border-radius: 10px;")

        self.right_temp_slider = CandleSlider(self)
        self.right_temp_slider.setGeometry(620, 60, 55, 215)
        self.right_temp_slider.setRange(0, 200)
        self.right_temp_slider.setValue(0)
        self.right_temp_slider.valueChanged.connect(self.right_temperature_changed)
        
        # ----- conductivity (above the bar) -----
        conductivity_label = QLabel("Conductivity", self)
        conductivity_label.setGeometry(290, 85, 120, 20)
        conductivity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.conductivity_spin = QDoubleSpinBox(self)
        self.conductivity_spin.setGeometry(275, 110, 150, 30)
        self.conductivity_spin.setRange(0.01, 100)
        self.conductivity_spin.setValue(1.0)
        self.conductivity_spin.setSuffix(" kW/°C")

        # ----- left body data -----
        left_temp_text = QLabel("Temp.", self)
        left_temp_text.setGeometry(20, 295, 70, 30)

        self.left_temp_display = QLabel("200.0 °C", self)
        self.left_temp_display.setGeometry(100, 295, 140, 30)
        self.left_temp_display.setStyleSheet("background-color: rgb(255, 243, 220); color: rgb(50, 25, 10); border: 1px solid rgb(215, 150, 45); border-radius: 5px; padding-left: 5px; font-weight: bold;")

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
        self.left_heat_capacity_spin.setRange(0.01, 100)
        self.left_heat_capacity_spin.setDecimals(3)
        self.left_heat_capacity_spin.setValue(0.385)
        self.left_heat_capacity_spin.setSuffix(" kJ/kg°C")

        # ----- right body data -----
        self.right_temp_display = QLabel("0.0 °C", self)
        self.right_temp_display.setGeometry(460, 295, 140, 30)
        self.right_temp_display.setStyleSheet("background-color: rgb(255, 243, 220); color: rgb(50, 25, 10); border: 1px solid rgb(215, 150, 45); border-radius: 5px; padding-left: 5px; font-weight: bold;")

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
        self.right_heat_capacity_spin.setRange(0.01, 100)
        self.right_heat_capacity_spin.setDecimals(3)
        self.right_heat_capacity_spin.setValue(0.385)
        self.right_heat_capacity_spin.setSuffix(" kJ/kg°C")

        right_heat_capacity_text = QLabel("H. Cap.", self)
        right_heat_capacity_text.setGeometry(610, 385, 70, 30)

        # ----- material selection -----
        left_material_text = QLabel("Material", self)
        left_material_text.setGeometry(20, 430, 70, 30)

        self.left_material_combo = QComboBox(self)
        self.left_material_combo.setGeometry(100, 430, 140, 30)
        self.left_material_combo.addItems(list(self.materials))
        self.left_material_combo.setCurrentText("Copper")
        self.left_material_combo.currentTextChanged.connect(self.left_material_changed)
        self.left_heat_capacity_spin.valueChanged.connect(self.left_heat_capacity_changed)

        self.right_material_combo = QComboBox(self)
        self.right_material_combo.setGeometry(460, 430, 140, 30)
        self.right_material_combo.addItems(list(self.materials))
        self.right_material_combo.setCurrentText("Copper")
        self.right_material_combo.currentTextChanged.connect(self.right_material_changed)
        self.right_heat_capacity_spin.valueChanged.connect(self.right_heat_capacity_changed)

        right_material_text = QLabel("Material", self)
        right_material_text.setGeometry(610, 430, 70, 30)

        # ----- heaters -----
        left_heater_text = QLabel("Heater", self)
        left_heater_text.setGeometry(20, 475, 70, 30)

        self.left_heater_spin = QDoubleSpinBox(self)
        self.left_heater_spin.setGeometry(100, 475, 140, 30)
        self.left_heater_spin.setRange(0, 10)
        self.left_heater_spin.setValue(0)
        self.left_heater_spin.setSuffix(" kW")

        self.right_heater_spin = QDoubleSpinBox(self)
        self.right_heater_spin.setGeometry(460, 475, 140, 30)
        self.right_heater_spin.setRange(0, 10)
        self.right_heater_spin.setValue(0)
        self.right_heater_spin.setSuffix(" kW")

        right_heater_text = QLabel("Heater", self)
        right_heater_text.setGeometry(610, 475, 70, 30)

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
        red = min(int(value / 200 * 255), 255)
        self.left_body_label.setStyleSheet(f"background-color: rgb({red}, 0, 0); border: 2px solid rgb(60, 60, 60); border-radius: 10px;")

    def right_temperature_changed(self, value):
        self.right_temp_display.setText(f"{value:.1f} °C")
        red = min(int(value / 200 * 255), 255)
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
                    self.left_heat_capacity_spin, self.right_heat_capacity_spin, self.conductivity_spin,
                       self.left_material_combo, self.right_material_combo]:
            widget.setEnabled(not checked)

    def timer_method(self):
        heat_current = self.conductivity_spin.value() * (self.right_body.temperature - self.left_body.temperature)
        heat = heat_current * self.dt
        left_heater_heat = self.left_heater_spin.value() * self.dt
        right_heater_heat = self.right_heater_spin.value() * self.dt
        left_temperature = self.left_body.add_heat(heat + left_heater_heat)
        right_temperature = self.right_body.add_heat(-heat + right_heater_heat)

        self.time = self.time + self.dt
        self.time_list.append(self.time)
        self.left_temp_list.append(left_temperature)
        self.right_temp_list.append(right_temperature)

        self.left_temp_slider.setValue(int(left_temperature))
        self.right_temp_slider.setValue(int(right_temperature))
        self.left_temperature_changed(left_temperature)
        self.right_temperature_changed(right_temperature)

        heaters_off = self.left_heater_spin.value() == 0 and self.right_heater_spin.value() == 0
        if heaters_off and abs(left_temperature - right_temperature) < 0.01:
            self.start_button.setChecked(False)
            self.start_stop(False)

    def left_material_changed(self, material):
        if self.materials[material] is not None:
            self.left_heat_capacity_spin.setValue(self.materials[material])

    def right_material_changed(self, material):
        if self.materials[material] is not None:
            self.right_heat_capacity_spin.setValue(self.materials[material])

    def left_heat_capacity_changed(self, value):
        if self.materials[self.left_material_combo.currentText()] != value:
            self.left_material_combo.setCurrentText("Custom")

    def right_heat_capacity_changed(self, value):
        if self.materials[self.right_material_combo.currentText()] != value:
            self.right_material_combo.setCurrentText("Custom")

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