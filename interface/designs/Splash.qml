import QtQuick
import QtQuick.Window

Window {
    width: 250
    height: 250
    visible: true

    flags: Qt.FramelessWindowHint | Qt.SplashScreen

    color: "#0C0B0A"

    FontLoader {
        id: nunito
        source: "../fonts/Nunito-Regular.ttf"
    }

    Image {
        anchors.centerIn: parent
        source: "../icons/alien_icon logo.svg"
        fillMode: Image.PreserveAspectFit
    }

    Text {
        id: version
        text: "ZHORRO v0.1.0"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        color: "#666666"
        font.family: nunito.name
        font.weight: Font.Normal
        font.pixelSize: 12
    }
}