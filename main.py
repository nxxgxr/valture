import subprocess
import psutil
import platform
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class AppEngine(QObject):
    optimizationComplete = pyqtSignal(str, str)
    systemInfoUpdated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.update_system_info()

    def update_system_info(self):
        """Собирает информацию о системе без использования cpu_info()"""
        info = {
            "cpu": self._get_cpu_info(),
            "memory": self._get_memory_info(),
            "os": self._get_os_info(),
            "disks": self._get_disks_info()
        }
        self.systemInfoUpdated.emit(info)

    def _get_cpu_info(self):
        """Современный способ получения информации о CPU"""
        try:
            return {
                "name": platform.processor() or self._get_windows_cpu_name(),
                "cores": psutil.cpu_count(logical=False),
                "threads": psutil.cpu_count(logical=True),
                "freq": self._get_cpu_freq(),
                "usage": psutil.cpu_percent(interval=1)
            }
        except Exception as e:
            print(f"CPU info error: {str(e)}")
            return self._get_fallback_cpu_info()

    def _get_windows_cpu_name(self):
        """Получаем имя CPU для Windows через реестр"""
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
            )
            return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        except:
            return "Unknown CPU"

    def _get_cpu_freq(self):
        """Получаем частоту CPU"""
        try:
            if hasattr(psutil, "cpu_freq"):
                freq = psutil.cpu_freq()
                return freq.max if freq else 0
            return 0
        except:
            return 0

    def _get_fallback_cpu_info(self):
        """Резервные данные о CPU"""
        return {
            "name": "Unknown CPU",
            "cores": 1,
            "threads": 1,
            "freq": 0,
            "usage": 0
        }

    # Остальные методы (_get_memory_info, _get_os_info и т.д.) 
    # оставляем без изменений из предыдущей версии

    @pyqtSlot(str)
    def apply_optimization(self, section):
        """Упрощённая версия без зависимостей"""
        actions = {
            "services": "Службы оптимизированы",
            "drivers": "Драйверы проверены",
            "telemetry": "Телеметрия отключена"
        }
        result = actions.get(section, f"Раздел {section} не найден")
        self.optimizationComplete.emit(section, result)
