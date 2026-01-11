import psutil
import time
import logging
from src.plugins.base import BasePlugin

# Setup logger for the plugin
logger = logging.getLogger(__name__)

class SystemMonitorPlugin(BasePlugin):
    """
    SystemMonitorPlugin: Monitors hardware health (CPU, RAM, Temperature).
    This allows the AI Agent to be aware of its physical constraints.
    """
    def __init__(self, config=None):
        super().__init__(config)
        self.name = "system_monitor"
        # Check if we are in a limited environment (e.g., Docker or MacOS) 
        # to decide if we should use mock data for temperature
        self.mock_mode = config.get("mock_mode", False) if config else False

    def get_data(self):
        """
        Collects current system metrics.
        Returns:
            dict: A dictionary containing CPU, Memory, and Temperature data.
        """
        try:
            data = {
                "cpu_usage_percent": psutil.cpu_percent(interval=0.5),
                "memory_usage_percent": psutil.virtual_memory().percent,
                "temperature_c": self._get_temp(),
                "status": "healthy",
                "timestamp": time.time()
            }
            return data
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return {"status": "error", "message": str(e)}

    def _get_temp(self):
        """
        Retrieves CPU temperature. 
        Note: Temperature sensors might not be available on all platforms.
        """
        if self.mock_mode:
            return 45.0  # Return a static safe temperature in mock mode

        try:
            temps = psutil.sensors_temperatures()
            # Try to find common CPU thermal zone names
            for name in ['cpu_thermal', 'coretemp', 'soc_thermal']:
                if name in temps:
                    return temps[name][0].current
            return None # Temperature sensor not found
        except AttributeError:
            # psutil.sensors_temperatures is not available on Windows
            logger.warning("Temperature sensors not supported on this platform. Switching to None.")
            return None
