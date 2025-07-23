import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: serviceGroup
    width: parent.width
    height: header.height + servicesColumn.height + 30
    color: "#252541"
    radius: 12
    border.color: "#3498db"
    border.width: 1
    
    property string title: ""
    property var services: []
    property bool expanded: true
    
    // Анимация сворачивания/разворачивания
    Behavior on height {
        NumberAnimation { duration: 300; easing.type: Easing.InOutQuad }
    }
    
    Column {
        anchors.fill: parent
        anchors.margins: 15
        spacing: 15
        
        // Заголовок группы
        Row {
            width: parent.width
            spacing: 10
            
            Text {
                text: serviceGroup.title
                font.pixelSize: 18
                font.bold: true
                color: "#FFFFFF"
                width: parent.width - 40
                wrapMode: Text.Wrap
            }
            
            Button {
                width: 30
                height: 30
                background: Rectangle {
                    color: "transparent"
                    border.color: "#3498db"
                    radius: 4
                }
                contentItem: Text {
                    text: serviceGroup.expanded ? "−" : "+"
                    color: "#FFFFFF"
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                onClicked: serviceGroup.expanded = !serviceGroup.expanded
                
                // Анимация кнопки
                Behavior on rotation {
                    NumberAnimation { duration: 300 }
                }
            }
        }
        
        // Список служб
        Column {
            id: servicesColumn
            width: parent.width
            spacing: 10
            visible: serviceGroup.expanded
            
            Repeater {
                model: serviceGroup.services
                
                Row {
                    spacing: 15
                    
                    CheckBox {
                        id: serviceCheckbox
                        checked: modelData.enabled
                        onToggled: modelData.enabled = checked
                        
                        indicator: Rectangle {
                            implicitWidth: 24
                            implicitHeight: 24
                            radius: 6
                            color: serviceCheckbox.checked ? "#3498db" : "transparent"
                            border.color: serviceCheckbox.checked ? "#3498db" : "#666699"
                            
                            Image {
                                anchors.centerIn: parent
                                source: "assets/icons/check.svg"
                                width: 16
                                height: 16
                                visible: serviceCheckbox.checked
                            }
                        }
                    }
                    
                    Text {
                        text: modelData.name
                        font.pixelSize: 16
                        color: "#FFFFFF"
                        width: parent.width - 50
                        wrapMode: Text.Wrap
                    }
                    
                    Text {
                        text: modelData.enabled ? "Включено" : "Отключено"
                        font.pixelSize: 16
                        color: modelData.enabled ? "#4ade80" : "#f87171"
                    }
                }
            }
        }
        
        // Кнопка применения
        ApplyButton {
            width: 200
            height: 45
            text: "Применить"
            onClicked: {
                appEngine.apply_services(serviceGroup.services)
                applyAnim.start()
            }
            
            SequentialAnimation {
                id: applyAnim
                PropertyAnimation {
                    target: applyButton
                    property: "opacity"
                    from: 1
                    to: 0.7
                    duration: 100
                }
                PropertyAnimation {
                    target: applyButton
                    property: "opacity"
                    from: 0.7
                    to: 1
                    duration: 300
                }
            }
        }
    }
}