# utils/performance_monitor.py
import time
import threading
import psutil  # Make sure to install: pip install psutil
from utils.logging import log_info, log_error

class PerformanceMonitor:
    """Monitors CPU and memory usage."""

    def __init__(self, interval=5):
        """
        Initializes the PerformanceMonitor.

        Args:
            interval (int): Time interval in seconds between checks.
        """
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None

    def _monitor(self):
        """Monitors CPU and memory usage in a loop."""
        while not self._stop_event.is_set():
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory()

            log_info(f"CPU Usage: {cpu_percent}% | Memory Usage: {memory_usage.percent}% (Used: {memory_usage.used / (1024**3):.2f} GB / Total: {memory_usage.total / (1024**3):.2f} GB)")

            time.sleep(self.interval)


    def start(self):
        """Starts the monitoring thread."""
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()  # Ensure the event is cleared
            self._thread = threading.Thread(target=self._monitor, daemon=True)
            self._thread.start()
            log_info("Performance monitor started.")
        else:
            log_info("Performance monitor is already running.")


    def stop(self):
        """Stops the monitoring thread."""
        if self._thread is not None and self._thread.is_alive():
            self._stop_event.set()  # Signal the thread to stop
            self._thread.join()  # Wait for the thread to finish
            log_info("Performance monitor stopped.")
        else:
            log_info("Performance monitor is not running.")

    def tick(self):
        """ Placeholder to comply with previous code."""
        pass