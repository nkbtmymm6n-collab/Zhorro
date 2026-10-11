import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Basic

Rectangle {
    color: "#090909"

    property var selectedFiles: []

    Connections {
        target: backend

        function onFilesChanged(files) {
            selectedFiles=files
        }
}
    
    Text {
        id: title

        text: "Index"
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

        text: "Expand the searching scope via adding more files"
        color: "#666666"
        font.pixelSize: 14

        anchors.left: title.left
        anchors.top: title.bottom
        anchors.topMargin: 6
    }

    Rectangle {
        id: inputIndex
        anchors.top: description.bottom
        anchors.left: parent.left
        anchors.topMargin: 18
        anchors.leftMargin: 40
        color: "#111111"

        width: 600
        height: 250

        Rectangle {
            id: failureMessage
            visible: false
            color: "#111111"
            anchors.fill: parent
            z: 10

            Text {
                text: "Indexation was unsuccessful due to an unknown error. Try again."
                color: "#FF1744"
                font.pixelSize: 25
                width: parent.width - 40
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                anchors.centerIn: parent
            }
        }

        Rectangle {
            id: successMessage
            visible: false
            color: "#111111"
            anchors.fill: parent
            z: 10

            Text {
                text: "Files were indexed successfully. Yay."
                color: "#00E676"
                font.pixelSize: 25
                width: parent.width - 40
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                anchors.centerIn: parent
            }
        }
        

        Timer {
            id: messageTimer
            interval: 3000
            onTriggered: {
                successMessage.visible = false
                failureMessage.visible = false
                addButton.visible = true
                indexButton.visible = true
            }
        }
            
        Flow {
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.topMargin: 10
            anchors.leftMargin: 10

            spacing: 8

            Text {
                id: noFiles
                visible: selectedFiles.length === 0
                text: "No files..."
                color: "#555555"
                font.pixelSize: 15
            }

            Repeater {
                model: selectedFiles

                Button {
                    id: fileButton

                    height: 36
                    width: fileRow.implicitWidth + 20

                    property string extension: modelData.slice(modelData.lastIndexOf("."))
                    property string name: modelData.slice(modelData.lastIndexOf("/") + 1)

                    background: Rectangle {
                        color: fileButton.pressed? "#141414" : (fileButton.hovered? "#1A1A1A" : "#252525")
                    }

                    contentItem: Row {
                        id: fileRow
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 5

                        Image {

                            transform: Translate {
                                x: -4
                                y: 3
                            }

                            source: fileButton.extension === ".pdf"
                                ? Qt.resolvedUrl("../icons/file-earmark-pdf.svg")
                                : fileButton.extension === ".docx"
                                    ? Qt.resolvedUrl("../icons/filetype-docx.svg")
                                    : Qt.resolvedUrl("../icons/filetype-txt.svg")
                        }

                        Text {
                            text: fileButton.name
                            color: "#E0E0E0"
                            font.pixelSize: 18
                        }
                    }

                    onClicked: {
                        backend.delete(modelData)
                    }
                }
            }

        }

        Button {
            id: indexButton
            visible: true
            width: 100
            height: 50
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.bottomMargin: 10

            background: Rectangle {
                color: indexButton.pressed? "#6F0C14" : (indexButton.hovered? "#A51622" : "#8B101A")
            }

            text: "Index"
            font.weight: Font.Medium
            font.pixelSize: 20

            onClicked: {
                var success = backend.index()
                addButton.visible=false
                indexButton.visible=false
                if (success) {successMessage.visible=true}
                else {failureMessage.visible=true}
                backend.clearFiles()
                messageTimer.restart()
                
            }
        }

        Button {
            id: addButton
            visible: true

            width: 100
            height: 50
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.bottomMargin: 10

            background: Rectangle {
                color: addButton.pressed? "#141414" : (addButton.hovered? "#1A1A1A" : "#252525")
            }

            contentItem: Text {
                text: "Add files"
                color: "#E0E0E0"
                font.weight: Font.Medium
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            onClicked: {
                backend.selectFiles()
            }
        }
    }
}