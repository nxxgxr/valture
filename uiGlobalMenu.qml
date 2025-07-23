import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: globalMenu
    color: "#252541"
    radius: 8
    border.color: "#3498db"
    border.width: 1
    
    property int currentTab: 0
    
    Row {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 15
        
        MenuTabButton {
            text: "Оптимизация"
            icon: "assets/icons/optimize.svg"
            selected: globalMenu.currentTab === 0
            onClicked: globalMenu.currentTab = 0
            animationScale: 1.05
        }
        
        MenuTabButton {
            text: "Восстановление"
            icon: "assets/icons/restore.svg"
            selected: globalMenu.currentTab === 1
            onClicked: globalMenu.currentTab = 1
            animationScale: 1.05
        }
        
        MenuTabButton {
            text: "Настройки"
            icon: "assets/icons/settings.svg"
            selected: globalMenu.currentTab === 2
            onClicked: globalMenu.currentTab = 2
            animationScale: 1.05
        }
        
        // Информация о системе
        SystemInfoPanel {
            height: parent.height
            Layout.fillWidth: true
        }
        
        // Выбор языка
        LanguageSelector {}
    }
}