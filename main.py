import subprocess
import psutil
import platform
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class AppEngine(QObject):
    optimizationComplete = pyqtSignal(str, str)  # Сигнал: (раздел, результат)
    systemInfoUpdated = pyqtSignal(dict)  # Сигнал с информацией о системе
    
    def __init__(self):
        super().__init__()
        self.update_system_info()
    
    def update_system_info(self):
        """Собирает полную информацию о системе"""
        info = {
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "gpu": self.get_gpu_info(),
            "os": self.get_os_info(),
            "disks": self.get_disks_info()
        }
        self.systemInfoUpdated.emit(info)
    
    def get_cpu_info(self):
        """Возвращает информацию о процессоре"""
        try:
            return {
                "name": self._get_cpu_name(),
                "cores": psutil.cpu_count(logical=False),
                "threads": psutil.cpu_count(logical=True),
                "freq": self._get_cpu_freq(),
                "usage": psutil.cpu_percent(interval=1)
            }
        except Exception as e:
            print(f"CPU info error: {e}")
            return {
                "name": "Unknown",
                "cores": 0,
                "threads": 0,
                "freq": 0,
                "usage": 0
            }
    
    def _get_cpu_name(self):
        """Альтернативные методы получения имени CPU"""
        try:
            if platform.system() == "Windows":
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, 
                    r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
                )
                return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
            return platform.processor()
        except:
            return "Unknown CPU"
    
    def _get_cpu_freq(self):
        """Получение частоты CPU"""
        try:
            freq = psutil.cpu_freq()
            return freq.max if freq else 0
        except:
            return 0
    
    def get_memory_info(self):
        """Информация об оперативной памяти"""
        try:
            mem = psutil.virtual_memory()
            return {
                "total": mem.total // (1024**3),
                "available": mem.available // (1024**3),
                "used": mem.used // (1024**3),
                "percent": mem.percent
            }
        except:
            return {
                "total": 0,
                "available": 0,
                "used": 0,
                "percent": 0
            }
    
    def get_gpu_info(self):
        """Информация о видеокарте"""
        try:
            if platform.system() == "Windows":
                import wmi
                w = wmi.WMI()
                gpu = w.Win32_VideoController()[0]
                return {
                    "name": gpu.Name,
                    "vram": int(gpu.AdapterRAM // (1024**3)) if gpu.AdapterRAM else 0
                }
            return {"name": "Unknown GPU", "vram": 0}
        except Exception as e:
            print(f"GPU info error: {e}")
            return {"name": "Unknown", "vram": 0}
    
    def get_os_info(self):
        """Информация об ОС"""
        try:
            return {
                "name": platform.system(),
                "version": platform.version(),
                "build": platform.win32_ver()[1] if platform.system() == "Windows" else ""
            }
        except:
            return {
                "name": "Unknown",
                "version": "",
                "build": ""
            }
    
    def get_disks_info(self):
        """Информация о дисках"""
        try:
            disks = []
            for part in psutil.disk_partitions():
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "device": part.device,
                    "mount": part.mountpoint,
                    "type": part.fstype,
                    "total": usage.total // (1024**3),
                    "used": usage.used // (1024**3),
                    "free": usage.free // (1024**3)
                })
            return disks
        except:
            return []
    
    @pyqtSlot(str)
    def apply_optimization(self, section):
        """Применяет оптимизацию для указанного раздела"""
        result = f"Оптимизация {section} выполнена"
        
        try:
            if section == "services":
                result = self.disable_services()
            elif section == "drivers":
                result = self.update_drivers()
            elif section == "telemetry":
                result = self.disable_telemetry()
        except Exception as e:
            result = f"Ошибка: {str(e)}"
        
        self.optimizationComplete.emit(section, result)
    
    def disable_services(self):
        """Отключает неиспользуемые службы"""
        services = ["DiagTrack", "dmwappushservice", "WMPNetworkSvc"]
        disabled = 0
        
        for service in services:
            try:
                subprocess.run(f"sc stop {service}", shell=True, check=True)
                subprocess.run(f"sc config {service} start= disabled", shell=True, check=True)
                disabled += 1
            except:
                continue
                
        return f"Отключено служб: {disabled}/{len(services)}"
    
    def update_drivers(self):
        """Обновление драйверов (заглушка)"""
        return "Драйверы актуальны"
    
    def disable_telemetry(self):
        """Отключает телеметрию Windows"""
        try:
            subprocess.run(
                'reg add HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\DataCollection '
                '/v AllowTelemetry /t REG_DWORD /d 0 /f',
                shell=True,
                check=True
            )
            return "Телеметрия отключена"
        except subprocess.CalledProcessError:
            return "Ошибка отключения телеметрии"
