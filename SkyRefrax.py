from PyQt5 import QtWidgets
import sys
import math
import matplotlib.pyplot as plt

def calcola_n_lambda(lambda_angstrom, pressione, temperatura, vapore_acqueo):
    K1, K2, K3 = 64.328, 29498.1, 255.4
    primo_termine = K1 + (K2 / (146 - (1 / lambda_angstrom) ** 2)) + (K3 / (41 - (1 / lambda_angstrom) ** 2))
    secondo_termine = primo_termine * (pressione * (1 + (1.049 - 0.0157 * temperatura) * 1e-6 * pressione) / (720.883 * (1 + 0.003661 * temperatura)))
    terzo_termine = secondo_termine - (0.0624 - (0.000680 / lambda_angstrom) / (1 + 0.003661 * temperatura)) * vapore_acqueo
    return terzo_termine / (1e+6) + 1

def calcola_delta_r(n_lambda, n_5000, angolo_rad):
    return 206265 * (n_lambda - n_5000) * math.tan(angolo_rad)

def parse_angle(angle_str):
    try:
        parts = angle_str.replace('°', ' ').replace("'", ' ').replace('"', ' ').split()
        return math.radians(float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / 3600)
    except:
        return None

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("rDelta Calculator")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.lambda_input = QtWidgets.QLineEdit()
        self.lambda_input.setPlaceholderText("Wave Lengths")
        layout.addWidget(self.lambda_input)
        
        self.angoli_input = QtWidgets.QLineEdit()
        self.angoli_input.setPlaceholderText("Zenith Angles")
        layout.addWidget(self.angoli_input)
        
        self.pressione_input = QtWidgets.QLineEdit()
        self.pressione_input.setPlaceholderText("Pressure (mmHg)")
        layout.addWidget(self.pressione_input)
        
        self.temperatura_input = QtWidgets.QLineEdit()
        self.temperatura_input.setPlaceholderText("Temperature (°C)")
        layout.addWidget(self.temperatura_input)
        
        self.vapore_input = QtWidgets.QLineEdit()
        self.vapore_input.setPlaceholderText("Water Vapor (mmHg)")
        layout.addWidget(self.vapore_input)
        
        self.calc_button = QtWidgets.QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calcola)
        layout.addWidget(self.calc_button)
        
        self.export_button = QtWidgets.QPushButton("Export Table")
        self.export_button.clicked.connect(self.esporta_tabella)
        layout.addWidget(self.export_button)
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def calcola(self):
        try:
            self.lambda_list = list(map(float, self.lambda_input.text().split(',')))
            self.angoli_list = list(map(parse_angle, self.angoli_input.text().split(',')))
            pressione = float(self.pressione_input.text())
            temperatura = float(self.temperatura_input.text())
            vapore_acqueo = float(self.vapore_input.text())
            
            if None in self.angoli_list:
                QtWidgets.QMessageBox.critical(self, "Error", "Format of angles not valid!")
                return
            
            r_5000 = calcola_n_lambda(5000 * 1e-4, pressione, temperatura, vapore_acqueo)
            self.n_lambda = [calcola_n_lambda(l * 1e-4, pressione, temperatura, vapore_acqueo) for l in self.lambda_list]
            
            self.rDelta_matrix = [[calcola_delta_r(nl, r_5000, ang) for ang in self.angoli_list] for nl in self.n_lambda]
            
            self.table.setRowCount(len(self.lambda_list))
            self.table.setColumnCount(len(self.angoli_list))
            self.table.setHorizontalHeaderLabels([f"{round(1/(math.cos(a)), 2)}" for a in self.angoli_list])
            self.table.setVerticalHeaderLabels([f"{l} Å" for l in self.lambda_list])
            
            for i, row in enumerate(self.rDelta_matrix):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QtWidgets.QTableWidgetItem(f"{round(value, 2)}"))
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
    
    def esporta_tabella(self):
        try:
            if not hasattr(self, 'rDelta_matrix'):
                QtWidgets.QMessageBox.critical(self, "Error", "No data available. Calculate first!")
                return
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.axis('tight')
            ax.axis('off')
            table_data = [[round(value, 2) for value in row] for row in self.rDelta_matrix]
            col_labels = [f"{round(1/(math.cos(a)), 2)}" for a in self.angoli_list]
            row_labels = [f"{l} Å" for l in self.lambda_list]
            
            table = ax.table(cellText=table_data, colLabels=col_labels, rowLabels=row_labels, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.2)
            
            options = QtWidgets.QFileDialog.Options()
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Table", "", "PNG Files (*.png);;PDF Files (*.pdf)", options=options)
            
            if file_path:
                plt.savefig(file_path, bbox_inches='tight')
                QtWidgets.QMessageBox.information(self, "Success", f"Table saved to {file_path}")
            plt.close()
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
