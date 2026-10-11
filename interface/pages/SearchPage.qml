import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Basic

Rectangle {
    color: "#090909"
    
    Text {
        id: title

        text: "Search"
        color: "#E0E0E0"
        font.pixelSize: 32
        font.weight: Font.DemiBold

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 40
        anchors.topMargin: 35
    }

    Text {
        id: description

        text: "Search through your indexed documents"
        color: "#666666"
        font.pixelSize: 14

        anchors.left: title.left
        anchors.top: title.bottom
        anchors.topMargin: 6
    }

    Row {
        spacing: 10
        anchors.top: description.bottom
        anchors.left: parent.left
        anchors.topMargin: 18
        anchors.leftMargin: 40

        TextField {
            id: inputSearch

            width: 600
            height: 50

            placeholderText: "What are you searching for?"
            color: "#E0E0E0"
            placeholderTextColor: "#555555"
            font.pixelSize: 15

            background: Rectangle {
            color: "#111111"
            }

            onAccepted: searchButton.clicked()
        }

        Button {
            id: searchButton

            width: 100
            height: 50

            background: Rectangle {
                color: searchButton.pressed? "#6F0C14" : (searchButton.hovered? "#A51622" : "#8B101A")
            }

            text: "Search"
            font.weight: Font.Medium
            font.pixelSize: 20

            onClicked: {
                backend.search(inputSearch.text)
            }
        }
    }

    Repeater {
        model: results

        Rectangle {
            width: 710
            color: "#111111"
        }
    }
}