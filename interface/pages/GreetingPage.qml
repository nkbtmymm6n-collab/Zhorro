import QtQuick
import QtQuick.Controls

Rectangle {
    color: "#090909"
    
    Text {
        anchors.centerIn: parent
        id: zhorro
        text: "ZHORRO."
        color: "#E0E0E0"
        font.pixelSize: 72
    }

    FontLoader {
        id: nunito
        source: "../fonts/NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf"
    }  

    Text {
        anchors.top: zhorro.bottom
        anchors.horizontalCenter: zhorro.horizontalCenter
        id: egg
        text: "silent爱 was here"
        color: "#4A4A4A"
        font.family: nunito.name
        font.weight: Font.Normal
        font.pixelSize: 21
    }
}