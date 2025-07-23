import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: driversPage
    
    Column {
        spacing: 25
        anchors.fill: parent
        anchors.margins: 30
        
        Text {
            text: "Управление драйверами"
            font.pixelSize: 28
            font.bold: true
            color: "#FFFFFF"
        }
        
        // Кнопки драйверов
        Grid {
            width: parent.width
            columns: 2
            columnSpacing: 20
            rowSpacing: 15
            
            DriverButton {
                text: "Скачать DirectX"
                onClicked: appEngine.download_driver("directx")
            }
            
            DriverButton {
                text: "Скачать Visual C++"
                onClicked: appEngine.download_driver("vcpp")
            }
            
            // Выбор драйвера NVIDIA
            Rectangle {
                width: 300
                height: 60
                color: "transparent"
                
                ComboBox {
                    id: nvidiaCombo
                    width: parent.width
                    height: 50
                    model: ["NVIDIA 566.14", "NVIDIA 566.36"]
                    font.pixelSize: 16
                    
                    background: Rectangle {
                        color: "#252541"
                        radius: 8
                        border.color: nvidiaCombo.hovered ? "#3498db" : "#444466"
                    }
                    
                    popup: Popup {
                        width: nvidiaCombo.width
                        implicitHeight: contentItem.implicitHeight
                        padding: 1
                        
                        contentItem: ListView {
                            clip: true
                            implicitHeight: contentHeight
                            model: nvidiaCombo.popup.visible ? nvidiaCombo.delegateModel : null
                            currentIndex: nvidiaCombo.highlightedIndex
                            
                            highlight: Rectangle {
                                color: "#3498db"
                                radius: 4
                            }
                        }
                        
                        background: Rectangle {
                            color: "#252541"
                            border.color: "#3498db"
                            radius: 8
                        }
                    }
                }
            }
            
            DriverButton {
                text: "Установить NVIDIA"
                onClicked: appEngine.install_nvidia_driver(nvidiaCombo.currentText)
            }
        }
        
        // Результаты
        ResultsBox {
            id: driversResult
            width: parent.width
            height: 120
        }
        
        // Применить все
        ApplyAllButton {
            onClicked: {
                appEngine.apply_optimization("drivers")
                applyAnimation.start()
            }
        }
    }
    
    Connections {
        target: appEngine
        function onOptimizationComplete(section, result) {
            if (section === "drivers") {
                driversResult.text += result + "\n"
            }
        }
    }
    
    // Анимация кнопки "Применить"
    SequentialAnimation {
        id: applyAnimation
        PropertyAnimation {
            target: applyAllButton
            property: "scale"
            from: 1
            to: 0.9
            duration: 100
        }
        PropertyAnimation {
            target: applyAllButton
            property: "scale"
            from: 0.9
            to: 1
            duration: 200
            easing.type: Easing.OutBack
        }
    }
}