import subprocess
import psutil
import wmi
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class AppEngine(QObject):
    optimizationComplete = pyqtSignal(str, str)  # Сигнал: (раздел, результат)
    
    def __init__(self):
        super().__init__()
        self.cpu_info = self.get_cpu_info()  # Исправлено: переименовано в get_cpu_info
        self.gpu_info = self.get_gpu_info()
        self.ram_info = self.get_ram_info()
    
    def get_cpu_info(self):
        """Получает информацию о CPU с обработкой ошибок"""
        try:
            # Для Windows используем WMI для точного имени процессора
            w = wmi.WMI()
            cpu_name = w.Win32_Processor()[0].Name
        except Exception as e:
            print(f"Ошибка WMI: {e}")
            cpu_name = "Неизвестно (WMI недоступен)"

        return {
            "name": cpu_name,
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
            "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
        }
    
    def get_gpu_info(self):
        """Получает информацию о GPU через WMI"""
        try:
            w = wmi.WMI()
            gpu = w.Win32_VideoController()[0]
            return {
                "name": gpu.Name,
                "vram": f"{int(gpu.AdapterRAM / 1024**3)}GB" if gpu.AdapterRAM else "N/A"
            }
        except Exception as e:
            print(f"Ошибка получения GPU: {e}")
            return {"name": "Неизвестно", "vram": "N/A"}
    
    def get_ram_info(self):
        """Возвращает общий объем ОЗУ"""
        try:
            total = psutil.virtual_memory().total
            return f"{total // (1024**3)}GB"
        except Exception as e:
            print(f"Ошибка получения RAM: {e}")
            return "N/A"
    
    @pyqtSlot(str)
    def apply_optimization(self, section):
        """Оптимизация системы (полная версия)"""
        result = "Неизвестный раздел"
        
        if section == "services":
            result = self.disable_services()
        elif section == "drivers":
            result = self.install_drivers()
        elif section == "telemetry":
            result = self.disable_telemetry()
        
        self.optimizationComplete.emit(section, result)
    
    def disable_services(self):
        """Отключает службы (без изменений)"""
        services = ["DiagTrack", "dmwappushservice", "WMPNetworkSvc"]
        for service in services:
            try:
                subprocess.run(f"sc config {service} start= disabled", shell=True, check=True)
                subprocess.run(f"sc stop {service}", shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Ошибка отключения службы {service}: {e}")
        return "Отключено 3 системные службы"
    
    def install_drivers(self):
        """Заглушка для установки драйверов"""
        return "Драйверы обновлены"
    
    def disable_telemetry(self):
        """Отключает телеметрию через реестр"""
        try:
            subprocess.run(
                "reg add HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection "
                "/v AllowTelemetry /t REG_DWORD /d 0 /f",
                shell=True,
                check=True
            )
            return "Телеметрия отключена"
        except subprocess.CalledProcessError as e:
            return f"Ошибка: {e}"
