import logging
import time

import psutil

from src.plugins.base import BasePlugin

# Setup logger for the plugin
logger = logging.getLogger(__name__)


class SystemMonitorPlugin(BasePlugin):
    """
    SystemMonitorPlugin: Monitors hardware health (CPU, RAM, Temperature).

    This allows the AI Agent to be aware of its physical constraints.
    """

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)
        self.name = "system_monitor"
        # Check if we are in a limited environment (e.g., Docker or MacOS)
        # to decide if we should use mock data for temperature
        self.mock_mode = config.get("mock_mode", False) if config else False

    def get_data(self) -> dict:
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
                "timestamp": time.time(),
            }
            return data
        except (
            AttributeError,  # For unavailable sensors
            psutil.Error,    # For psutil-specific issues like AccessDenied
        ) as e:
            # Catch specific expected exceptions to prevent masking bugs
            logger.error("Failed to collect system metrics: %s", e)
            return {"status": "error", "message": str(e)}

    def _get_temp(self) -> float | None:
        """
        Retrieves CPU temperature safely.

        Note: Temperature sensors might not be available on all platforms.
        """
        if self.mock_mode:
            return 45.0

        try:
            temps = psutil.sensors_temperatures()
            for name in ["cpu_thermal", "coretemp", "soc_thermal"]:
                if name in temps:
                    return temps[name][0].current
            return None
        except (
            AttributeError,  # sensors_temperatures not implemented
            KeyError,        # Thermal name not found
            psutil.Error,    # General psutil errors including AccessDenied
        ):
            logger.warning("Temperature sensors not supported or accessible.")
            return None
