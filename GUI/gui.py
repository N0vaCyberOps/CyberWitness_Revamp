# Poprawiona wersja `gui.py` z docstringami
optimized_gui_with_docstring = '''"""
CyberWitness - Interfejs użytkownika.
Aplikacja GUI do obsługi monitoringu ruchu sieciowego.

Autor: N0vaCyberOps Team
"""

import sys
import asyncio
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

# 🔹 Logowanie
logger = logging.getLogger(__name__)

class BackgroundWorker(QThread):
    """Klasa obsługująca długotrwałe zadania w tle."""

    result_signal = pyqtSignal(str)

    def run(self):
        """Uruchamia wątek z pętlą zdarzeń asyncio."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.long_running_task())
        self.result_signal.emit(result)

    async def long_running_task(self):
        """Symuluje długotrwałe zadanie asynchroniczne."""
        await asyncio.sleep(2)
        return "Operacja zakończona!"

class CyberWitnessGUI(QMainWindow):
    """Główna klasa interfejsu użytkownika CyberWitness."""

    def __init__(self):
        """Inicjalizuje okno aplikacji."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Tworzy elementy interfejsu użytkownika."""
        self.setWindowTitle("CyberWitness")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Witaj w CyberWitness!", self)
        self.layout.addWidget(self.label)

        self.button = QPushButton("Uruchom zadanie", self)
        self.button.clicked.connect(self.start_background_task)
        self.layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def start_background_task(self):
        """Uruchamia proces w tle, aby uniknąć zawieszenia GUI."""
        self.worker = BackgroundWorker()
        self.worker.result_signal.connect(self.on_task_finished)
        self.worker.start()

    def on_task_finished(self, result):
        """Aktualizuje interfejs po zakończeniu zadania w tle."""
        self.label.setText(result)

def main():
    """Uruchamia aplikację GUI."""
    app = QApplication(sys.argv)
    window = CyberWitnessGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
'''

# Zapisanie nowej wersji `gui.py`
gui_path = os.path.join(project_path, "GUI/gui.py")
if os.path.exists(gui_path):
    with open(gui_path, "w", encoding="utf-8") as f:
        f.write(optimized_gui_with_docstring)

# ✅ Dodane docstringi w `gui.py`
"✅ `gui.py` zaktualizowany o dokumentację!"
