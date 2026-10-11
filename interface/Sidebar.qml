import QtQuick
import QtQuick.Controls
import "designs"
import "icons"

Rectangle {
    width: 250
    anchors.bottom: parent.bottom
    anchors.top: parent.top

    property StackView pageStack

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
        anchors.topMargin: 30
    }

    Column {
        spacing: 10
        anchors.top: logo.bottom
        anchors.topMargin: 20

        SidebarButton {
            icon.source: Qt.resolvedUrl("icons/search.svg")
            text: "Search"

            onClicked: pageStack.replace(Qt.resolvedUrl("pages/SearchPage.qml"))
        }

        SidebarButton {
            icon.source: Qt.resolvedUrl("icons/stack-overflow.svg")
            text: "Indexing"

            onClicked: pageStack.replace(Qt.resolvedUrl("pages/IndexingPage.qml"))
        }

        SidebarButton {
            icon.source: Qt.resolvedUrl("icons/file-earmark.svg")
            text: "Files"
        }
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