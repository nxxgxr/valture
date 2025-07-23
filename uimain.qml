import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15

ApplicationWindow {
    id: mainWindow
    width: 1280
    height: 800
    minimumWidth: 1024
    minimumHeight: 768
    visible: true
    title: "BoosterX Pro"
    color: "#1E1E2E"
    
    // Фон с параллакс-эффектом
    Image {
        source: "assets/background.jpg"
        anchors.fill: parent
        opacity: 0.15
        layer.enabled: true
        layer.effect: HueSaturation {
            saturation: -0.8
        }
        
        transform: [
            Scale {
                origin.x: mainWindow.width/2
                origin.y: mainWindow.height/2
                xScale: 1.1
                yScale: 1.1
            },
            Translate {
                x: (mouseArea.mouseX - mainWindow.width/2) / 20
                y: (mouseArea.mouseY - mainWindow.height/2) / 20
            }
        ]
    }
    
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
    }
    
    // Глобальное верхнее меню
    GlobalMenu {
        id: globalMenu
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 60
    }
    
    // Основной контент
    StackLayout {
        id: contentStack
        anchors.top: globalMenu.bottom
        anchors.bottom: parent.bottom
        anchors.left: sideMenu.right
        anchors.right: parent.right
        anchors.margins: 20
        currentIndex: globalMenu.currentTab
        
        // Страница оптимизации
        OptimizationPage {}
        
        // Страница восстановления
        RestorePointPage {}
        
        // Страница настроек
        SettingsPage {}
    }
    
    // Боковое меню для раздела оптимизации
    SideMenu {
        id: sideMenu
        visible: globalMenu.currentTab === 0
        anchors.top: globalMenu.bottom
        anchors.bottom: parent.bottom
        width: 250
    }
    
    // Анимация запуска
    Component.onCompleted: {
        splashAnimation.start()
    }
    
    ParallelAnimation {
        id: splashAnimation
        PropertyAnimation {
            target: mainWindow
            property: "opacity"
            from: 0
            to: 1
            duration: 1000
            easing.type: Easing.InOutQuad
        }
        PropertyAnimation {
            target: mainWindow
            property: "scale"
            from: 0.9
            to: 1
            duration: 800
            easing.type: Easing.OutBack
        }
    }
}