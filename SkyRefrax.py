from PyQt5 import QtWidgets
import sys
import math
import matplotlib.pyplot as plt

def calculate_n_lambda(wavelength, pressure, temperature, water_vapor):
    K1, K2, K3 = 64.328, 29498.1, 255.4
    term1 = K1 + (K2 / (146 - (1 / wavelength) ** 2)) + (K3 / (41 - (1 / wavelength) ** 2))
    term2 = term1 * (pressure * (1 + (1.049 - 0.0157 * temperature) * 1e-6 * pressure) / (720.883 * (1 + 0.003661 * temperature)))
    term3 = term2 - (0.0624 - (0.000680 / wavelength) / (1 + 0.003661 * temperature)) * water_vapor
    return term3 / 1e6 + 1

def calculate_delta_r(n_lambda, n_5000, angle_rad):
    return 206265 * (n_lambda - n_5000) * math.tan(angle_rad)

def parse_angle(angle_str):
    try:
        parts = angle_str.replace('°', ' ').replace("'", ' ').replace('"', ' ').split()
        return math.radians(float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / 3600)
    except:
        return None

class RefractionCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Refraction Delta Calculator")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.wavelength_input = QtWidgets.QLineEdit()
        self.wavelength_input.setPlaceholderText("Wavelengths (Å), comma-separated")
        layout.addWidget(self.wavelength_input)
        
        self.angles_input = QtWidgets.QLineEdit()
        self.angles_input.setPlaceholderText("Zenith Angles (deg, min, sec), comma-separated")
        layout.addWidget(self.angles_input)
        
        self.pressure_input = QtWidgets.QLineEdit()
        self.pressure_input.setPlaceholderText("Pressure (mmHg)")
        layout.addWidget(self.pressure_input)
        
        self.temperature_input = QtWidgets.QLineEdit()
        self.temperature_input.setPlaceholderText("Temperature (°C)")
        layout.addWidget(self.temperature_input)
        
        self.water_vapor_input = QtWidgets.QLineEdit()
        self.water_vapor_input.setPlaceholderText("Water Vapor (mmHg)")
        layout.addWidget(self.water_vapor_input)
        
        self.calculate_button = QtWidgets.QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)
        
        self.export_button = QtWidgets.QPushButton("Export Table")
        self.export_button.clicked.connect(self.export_table)
        layout.addWidget(self.export_button)
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def calculate(self):
        try:
            self.wavelengths = list(map(float, self.wavelength_input.text().split(',')))
            self.angles = list(map(parse_angle, self.angles_input.text().split(',')))
            pressure = float(self.pressure_input.text())
            temperature = float(self.temperature_input.text())
            water_vapor = float(self.water_vapor_input.text())
            
            if None in self.angles:
                QtWidgets.QMessageBox.critical(self, "Error", "Invalid angle format!")
                return
            
            n_5000 = calculate_n_lambda(5500 * 1e-4, pressure, temperature, water_vapor)
            self.n_lambda = [calculate_n_lambda(wl * 1e-4, pressure, temperature, water_vapor) for wl in self.wavelengths]
            
            self.refraction_deltas = [[calculate_delta_r(nl, n_5000, ang) for nl in self.n_lambda] for ang in self.angles]
            
            self.table.setRowCount(len(self.angles))
            self.table.setColumnCount(len(self.wavelengths))
            self.table.setHorizontalHeaderLabels([f"{wl} Å" for wl in self.wavelengths])
            self.table.setVerticalHeaderLabels([f"{round(1/(math.cos(a)), 2)} ({math.degrees(a):.2f}°)" for a in self.angles])
            
            for i, row in enumerate(self.refraction_deltas):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QtWidgets.QTableWidgetItem(f"{round(value, 2)}"))
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
    
    def export_table(self):
        try:
            if not hasattr(self, 'refraction_deltas'):
                QtWidgets.QMessageBox.critical(self, "Error", "No data available. Calculate first!")
                return
            
            fig, ax = plt.subplots(figsize=(len(self.wavelengths) * 0.8, len(self.angles) * 0.5))
            ax.axis('tight')
            ax.axis('off')
            
            table_data = [[round(value, 2) for value in row] for row in self.refraction_deltas]
            col_labels = [f"{wl} Å" for wl in self.wavelengths]
            row_labels = [f"{round(1/(math.cos(a)), 2)} ({math.degrees(a):.2f}°)" for a in self.angles]
            
            table = ax.table(cellText=table_data, colLabels=col_labels, rowLabels=row_labels, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1.5, 1.5)
            
            options = QtWidgets.QFileDialog.Options()
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Table", "", "PNG Files (*.png);;PDF Files (*.pdf)", options=options)
            
            if file_path:
                plt.savefig(file_path, bbox_inches='tight', dpi=300)
                QtWidgets.QMessageBox.information(self, "Success", f"Table saved to {file_path}")
            plt.close()
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RefractionCalculator()
    window.show()
    sys.exit(app.exec_())
