def get_cpu_info(self):
    """Получение информации о процессоре с использованием WMI для Windows"""
    try:
        # Получаем имя процессора через WMI (работает только на Windows)
        w = wmi.WMI()
        cpu_name = w.Win32_Processor()[0].Name
        
        # Получаем остальные данные через psutil
        cpu_data = {
            "name": cpu_name,
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
            "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
        }
        return cpu_data
        
    except Exception as e:
        print(f"Ошибка при получении данных CPU: {e}")
        return {
            "name": "Неизвестный процессор",
            "cores": 0,
            "threads": 0,
            "freq": 0
        }
