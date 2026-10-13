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

            onAccepted: fileDialog.open()
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
                fileDialog.open()
            }
        }
    }

    Dialog {
        id: fileDialog
        width: 600
        height: 500

        background: Rectangle {
        color: "#111111"
        }

        Text {
            id: srch
            text: "Select files"

            anchors.top: parent.top
            anchors.topMargin: 20
            anchors.left: parent.left
            anchors.leftMargin: 20

            color: "#E0E0E0"
            font.pixelSize: 32
            font.weight: Font.DemiBold
        }

        Text {
            id: exp
            text: "Click on the files which ones you want to search in"
            
            anchors.left: srch.left
            anchors.top: srch.bottom
            anchors.topMargin: 10

            color: "#666666"
            font.pixelSize: 14
        }
        modal: true
        Overlay.modal: Rectangle {
            color: "#B0000000"
        }
        standardButtons: Dialog.Cancel | Dialog.Ok

        x: (parent.width - width) / 2 - 140
        y: (parent.height - height) / 2
    }
}