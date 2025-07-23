import platform
import subprocess
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class AppEngine(QObject):
    optimizationComplete = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        
    def get_system_info(self):
        """Безопасный метод получения информации о системе"""
        return {
            "cpu": self._get_cpu_info(),
            "memory": self._get_memory_info()
        }
    
    def _get_cpu_info(self):
    """Полная замена для psutil.cpu_info()"""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        name = winreg.QueryValueEx(key, "ProcessorNameString")
                
            return {
                "name": cpu_name,
                "cores": self._get_cpu_cores(),
                "freq": self._get_cpu_freq()
            }
        except:
            return {
                "name": "Unknown",
                "cores": 1,
                "freq": 0
            }
    
    def _get_windows_cpu_name(self):
        """Альтернативный способ для Windows"""
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
            )
            return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        except:
            return "Unknown CPU"
    
    def _get_cpu_cores(self):
        """Количество ядер"""
        try:
            import psutil
            return psutil.cpu_count(logical=False) or 1
        except:
            return 1
    
    def _get_cpu_freq(self):
        """Частота процессора"""
        try:
            import psutil
            if hasattr(psutil, "cpu_freq"):
                freq = psutil.cpu_freq()
                return freq.max if freq else 0
            return 0
        except:
            return 0
    
    def _get_memory_info(self):
        """Информация о памяти"""
        try:
            import psutil
            mem = psutil.virtual_memory()
            return {
                "total": mem.total // (1024**3),
                "available": mem.available // (1024**3)
            }
        except:
            return {
                "total": 0,
                "available": 0
            }
    
    @pyqtSlot(str)
    def apply_optimization(self, section):
        result = f"{section} optimized"
        self.optimizationComplete.emit(section, result)
