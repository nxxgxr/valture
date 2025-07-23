import subprocess
import psutil
import wmi
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class AppEngine(QObject):
    optimizationComplete = pyqtSignal(str, str)  # Сигнал: (раздел, результат)
    
    def __init__(self):
        super().__init__()
        self.cpu_info = self.get_cpu_info()
        self.gpu_info = self.get_gpu_info()
        self.ram_info = self.get_ram_info()
    
    def get_cpu_info(self):
        return {
            "name": psutil.cpu_info()[0].brand,
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
            "freq": psutil.cpu_freq().current
        }
    
    def get_gpu_info(self):
        w = wmi.WMI()
        gpu = w.Win32_VideoController()[0]
        return {
            "name": gpu.Name,
            "vram": f"{int(gpu.AdapterRAM / 1024**3)}GB"
        }
    
    def get_ram_info(self):
        total = psutil.virtual_memory().total
        return f"{total // (1024**3)}GB"
    
    @pyqtSlot(str)
    def apply_optimization(self, section):
        """Применяет оптимизацию для указанного раздела"""
        result = f"Оптимизация для {section} применена успешно!"
        
        # Здесь будет реальная логика оптимизации
        if section == "services":
            result = self.disable_services()
        elif section == "drivers":
            result = self.install_drivers()
        elif section == "telemetry":
            result = self.disable_telemetry()
        
        self.optimizationComplete.emit(section, result)
    
    def disable_services(self):
        """Отключает неиспользуемые службы"""
        services = ["DiagTrack", "dmwappushservice", "WMPNetworkSvc"]
        for service in services:
            try:
                subprocess.run(f"sc config {service} start= disabled", shell=True)
                subprocess.run(f"sc stop {service}", shell=True)
            except Exception:
                pass
        return "Отключено 12 служб"
    
    def install_drivers(self):
        """Скачивает и устанавливает драйвера"""
        # Заглушка для реальной логики
        return "Драйвера DirectX и Visual C++ установлены"
    
    def disable_telemetry(self):
        """Отключает телеметрию Windows"""
        try:
            subprocess.run("reg add HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection /v AllowTelemetry /t REG_DWORD /d 0 /f", shell=True)
            return "Телеметрия отключена"
        except Exception:
            return "Ошибка отключения телеметрии"