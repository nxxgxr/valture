import sys
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from app_engine import AppEngine

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Регистрация Python-логики в QML
    app_engine = AppEngine()
    engine.rootContext().setContextProperty("appEngine", app_engine)
    
    # Загрузка главного QML-файла
    engine.load("ui/main.qml")
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    # Установка глобальных свойств
    root = engine.rootObjects()[0]
    root.setProperty("appVersion", "1.0 Pro")
    
    sys.exit(app.exec())