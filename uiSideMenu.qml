import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: sideMenu
    color: "#2A2A4A"
    radius: 8
    
    ListView {
        id: menuList
        anchors.fill: parent
        anchors.margins: 10
        model: ListModel {
            ListElement { name: "Драйверы"; icon: "drivers" }
            ListElement { name: "Windows"; icon: "windows" }
            ListElement { name: "Службы"; icon: "services" }
            ListElement { name: "Клавиатура и мышь"; icon: "mouse" }
            ListElement { name: "CPU"; icon: "cpu" }
            ListElement { name: "GPU"; icon: "gpu" }
            ListElement { name: "Приложения"; icon: "apps" }
            ListElement { name: "Интернет"; icon: "internet" }
            ListElement { name: "ResolutionFix"; icon: "resolution" }
            ListElement { name: "Питание"; icon: "power" }
            ListElement { name: "Игры"; icon: "games" }
            ListElement { name: "Телеметрия"; icon: "telemetry" }
            ListElement { name: "Очистка"; icon: "clean" }
            ListElement { name: "Отключение драйверов"; icon: "disable" }
            ListElement { name: "Отключение устройств"; icon: "devices" }
        }
        delegate: MenuItem {
            text: name
            iconSource: `assets/icons/${icon}.svg`
            selected: ListView.isCurrentItem
            onClicked: {
                menuList.currentIndex = index
                optimizationPage.currentSection = index
            }
        }
        
        highlight: Rectangle {
            color: "#3498db"
            radius: 6
            opacity: 0.7
        }
        
        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AsNeeded
        }
    }
    
    // Анимация появления
    PropertyAnimation {
        id: enterAnimation
        target: sideMenu
        property: "x"
        from: -width
        to: 0
        duration: 500
        easing.type: Easing.OutBack
    }
    
    Component.onCompleted: enterAnimation.start()
}