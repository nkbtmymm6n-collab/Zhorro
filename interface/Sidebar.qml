import QtQuick
import QtQuick.Controls
import "designs"
import "icons"

Rectangle {
    width: 250
    height: 700

    color: "#0C0B0A"

    FontLoader {
        id: nunito
        source: "fonts/NunitoSans-VariableFont_YTLC,opsz,wdth,wght.ttf"
    }

    Image {
        id: logo

        source: "icons/alien_icon.svg"

        width: 50
        height: 50

        fillMode: Image.PreserveAspectFit

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 20
    }

    Column {
        spacing: 10
        anchors.top: logo.bottom
        anchors.topMargin: 30

        SidebarButton {
            icon.source: Qt.resolvedUrl("icons/search.svg")
            text: "Search"
        }

        SidebarButton {
            icon.source: Qt.resolvedUrl("icons/stack-overflow.svg")
            text: "Indexing"
        }

        SidebarButton {
            icon.source: Qt.resolvedUrl("icons/file-earmark.svg")
            text: "Files"
        }
    }
}