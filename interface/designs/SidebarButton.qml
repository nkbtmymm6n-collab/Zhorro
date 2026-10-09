import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Effects

Button {
    id: button
    width: 250
    height: 70

    leftPadding: 0
    rightPadding: 0
    topPadding: 0
    bottomPadding: 0

    FontLoader {
        id: nunito
        source: "../fonts/NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf"
    }

    background: Rectangle {
        color: button.pressed ? "#3A0B12" : (button.hovered ? "#241010" : "#0C0B0A")

        Behavior on color {
            ColorAnimation {
                duration: 40
            }
        }
    }

    contentItem: Row {

        spacing: 5

        Rectangle {
            width: 11
            height: 70
            color: button.pressed ? "#FF1F35" : (button.hovered ? "#8B101A" : "transparent")
        }

        Item {
            width: 10
            height: 1
        }

        Image {
            id: icon
            source: button.icon.source
            visible: false
        }

        MultiEffect {
            source: icon
            width: icon.width
            height: icon.height

            anchors.verticalCenter: parent.verticalCenter

            colorization: 1.0
            colorizationColor: button.pressed ? "#FF1F35" : (button.hovered ? "#FF3045" : "#E0E0E0")

            Behavior on colorizationColor {
                ColorAnimation {
                    duration: 40
                }
            }
        }

        Item {
            width: 18
            height: 1
        }
        
        Text {
            text: button.text
            color: button.pressed ? "#FF1F35" : (button.hovered ? "#FF3045" : "#E0E0E0")
            font.pixelSize: 18
            font.family: nunito.name
            font.weight: Font.Normal
            anchors.verticalCenter: parent.verticalCenter
            
            Behavior on color {
                ColorAnimation {
                    duration: 40
                }
            }
        }
    }
}