import sys
import asyncio
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.uic import loadUi
from auth import AuthModel
from controller import AuthController
from cyber_witness.main import CyberWitness

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CyberWitnessGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("cyber_witness.ui", self)  # Ładowanie pliku .ui z Qt Designer
        self.auth_model = AuthModel()
        self.auth_controller = AuthController(self.auth_model)
        self.cw = CyberWitness()
        self.role = None
        self.alerts = []
        self.setup_ui()

    def setup_ui(self):
        # Ustawienie ciemnej kolorystyki
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;"
                          "QPushButton { background-color: #007BFF; color: white; padding: 5px; }"
                          "QLineEdit { background-color: #4A4A4A; color: white; padding: 5px; }"
                          "QTableWidget { background-color: #3E3E3E; color: white; }"
                          "QTabWidget::pane { border: 1px solid #D3D3D3; }")

        # Inicjalizacja wykresu
        chart = QChart()
        self.traffic_series = QLineSeries()
        chart.addSeries(self.traffic_series)
        self.trafficChart.setChart(chart)

        # Ukrycie zakładek przed zalogowaniem
        self.mainTabs.setVisible(False)

        # Połączenie sygnałów
        self.auth_controller.login_success.connect(self.on_login_success)
        self.auth_controller.login_failed.connect(self.on_login_failed)
        self.loginButton.clicked.connect(self.attempt_login)
        self.startSnifferButton.clicked.connect(self.start_sniffer)
        self.stopSnifferButton.clicked.connect(self.stop_sniffer)
        self.exportReportsButton.clicked.connect(self.export_reports)
        self.addUserButton.clicked.connect(self.add_user)
        self.saveConfigButton.clicked.connect(self.save_config)

    def attempt_login(self):
        self.auth_controller.login(self.usernameInput.text(), self.passwordInput.text())

    def on_login_success(self, role):
        self.role = role
        self.loginWidget.setVisible(False)
        self.mainTabs.setVisible(True)

        # Dynamiczne ukrywanie zakładek na podstawie roli
        if self.role == "Technik":
            self.mainTabs.removeTab(self.mainTabs.indexOf(self.snifferTab))
            self.mainTabs.removeTab(self.mainTabs.indexOf(self.usersTab))
            self.mainTabs.removeTab(self.mainTabs.indexOf(self.configTab))
            self.mainTabs.removeTab(self.mainTabs.indexOf(self.kibanaTab))
        elif self.role == "Pentester":
            self.mainTabs.removeTab(self.mainTabs.indexOf(self.usersTab))
            self.mainTabs.removeTab(self.mainTabs.indexOf(self.configTab))
            self.mainTabs.removeTab(self.mainTabs.indexOf(self.kibanaTab))

        self.start_timer()

    def on_login_failed(self, message):
        logger.error(message)

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_traffic)
        self.timer.start(1000)

    def update_traffic(self):
        # Placeholder dla integracji z CyberWitness
        self.traffic_series.append(self.traffic_series.count(), self.traffic_series.count())
        # Symulacja alertów
        self.alerts.append({"timestamp": "12:00", "severity": "LOW", "description": "Suspicious UA"})
        self.update_alerts()

    def update_alerts(self):
        self.alertsTable.setRowCount(0)
        for alert in self.alerts:
            if self.role == "Technik" and alert["severity"] == "HIGH":
                continue
            row = self.alertsTable.rowCount()
            self.alertsTable.insertRow(row)
            self.alertsTable.setItem(row, 0, QTableWidgetItem(alert["timestamp"]))
            self.alertsTable.setItem(row, 1, QTableWidgetItem(alert["severity"]))
            self.alertsTable.setItem(row, 2, QTableWidgetItem(alert["description"]))

    def start_sniffer(self):
        asyncio.create_task(self.cw.monitor.start())

    def stop_sniffer(self):
        asyncio.create_task(self.cw.monitor.stop())

    def export_reports(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Reports", "", "CSV Files (*.csv)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write("Timestamp,Severity,Description\n")
                for alert in self.alerts:
                    f.write(f"{alert['timestamp']},{alert['severity']},{alert['description']}\n")

    def add_user(self):
        username = "new_user"
        password = "password"
        role = "Technik"
        self.auth_model.add_user(username, password, role)
        row = self.usersTable.rowCount()
        self.usersTable.insertRow(row)
        self.usersTable.setItem(row, 0, QTableWidgetItem(username))
        self.usersTable.setItem(row, 1, QTableWidgetItem(role))
        self.usersTable.setItem(row, 2, QTableWidgetItem("Edit/Delete"))

    def save_config(self):
        logger.info(f"Saving config: Threshold={self.thresholdInput.text()}, Filter={self.filterInput.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CyberWitnessGUI()
    window.show()
    sys.exit(app.exec_())