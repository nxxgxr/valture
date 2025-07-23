import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    id: animatedButton
    property real animationScale: 1.05
    property real animationDuration: 150
    
    background: Rectangle {
        color: "#3498db"
        radius: 8
        opacity: animatedButton.down ? 0.8 : 1
        
        // Эффект свечения
        Glow {
            anchors.fill: parent
            source: parent
            color: "#3498db"
            radius: animatedButton.hovered ? 10 : 0
            samples: 16
            spread: 0.5
            
            Behavior on radius {
                NumberAnimation { duration: 300 }
            }
        }
    }
    
    contentItem: Text {
        text: animatedButton.text
        color: "#FFFFFF"
        font.pixelSize: 16
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    
    // Анимация наведения
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        
        onEntered: hoverAnim.start()
        onExited: hoverAnimReverse.start()
    }
    
    ParallelAnimation {
        id: hoverAnim
        NumberAnimation {
            target: animatedButton
            property: "scale"
            from: 1
            to: animationScale
            duration: animationDuration
            easing.type: Easing.OutBack
        }
        NumberAnimation {
            target: animatedButton
            property: "rotation"
            from: 0
            to: Math.random() * 4 - 2 // Случайный угол
            duration: animationDuration
        }
    }
    
    ParallelAnimation {
        id: hoverAnimReverse
        NumberAnimation {
            target: animatedButton
            property: "scale"
            from: animationScale
            to: 1
            duration: animationDuration
            easing.type: Easing.InOutQuad
        }
        NumberAnimation {
            target: animatedButton
            property: "rotation"
            to: 0
            duration: animationDuration
        }
    }
}