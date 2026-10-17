import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Basic

Rectangle {
    color: "#090909"

    property var needs: []
    property StackView pageStack

    Component.onCompleted: {
        backend.show()
    }

    Connections {
        target: backend

        function onNeed2Show(shows) {
            needs=shows
        }
    }
    
    Text {
        id: title

        text: "Files"
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

        text: "All your indexed (searchable) files"
        color: "#666666"
        font.pixelSize: 14

        anchors.left: title.left
        anchors.top: title.bottom
        anchors.topMargin: 6
    }

    Rectangle {
        id: noFile
        color: "#111111"
        anchors.left: parent.left
        anchors.top: description.bottom
        anchors.leftMargin: 40
        anchors.topMargin: 18

        width: 600
        height: 60
        
        visible: needs.length === 0

        Image {
            id: img1
            source: "../icons/emoji-frown.svg"

            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 15
        }

        Text {
            id: no
            text: "No files :("
            color: "#E0E0E0"
            anchors.left: add.left
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -10
            font.pixelSize: 16
            font.weight: Font.Medium
        }

        Text {
            id: add
            text: "You can add them via the Indexing page"
            color: "#666666"
            anchors.left: img1.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: 10
            anchors.leftMargin: 15
            font.pixelSize: 14
            font.weight: Font.Medium
        }

        Rectangle {
            id: goButton
            width: 60
            height: 60

            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right

            color: mouseArea.pressed ? "#141414" : mouseArea.containsMouse ? "#1A1A1A" : "#252525"

            Image {
                anchors.centerIn: parent
                anchors.horizontalCenterOffset: 1
                anchors.verticalCenterOffset: 2
                source: "../icons/arrow-right.svg"
            }

            MouseArea {
                id: mouseArea
                anchors.fill: parent
                hoverEnabled: true
                onClicked: {
                    pageStack.push(Qt.resolvedUrl("IndexingPage.qml"))
                }
            }
        }
    }


    Column {
        anchors.left: parent.left
        anchors.top: description.bottom
        anchors.leftMargin: 40
        anchors.topMargin: 18
        spacing: 10

        Repeater {
            model: needs

            Rectangle {
                id: file
                color: "#111111"

                property string extension: modelData.slice(modelData.lastIndexOf("."))
                property string name: modelData.slice(
                    Math.max(modelData.lastIndexOf("/"), modelData.lastIndexOf("\\")) + 1
                )

                width: 600
                height: 60

                Image {
                    id: img
                    source: file.extension === ".pdf"
                        ? Qt.resolvedUrl("../icons/file-earmark-pdf copy.svg")
                        : file.extension === ".docx"
                        ? Qt.resolvedUrl("../icons/filetype-docx copy.svg")
                        : Qt.resolvedUrl("../icons/filetype-txt copy.svg")

                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 65

                    MouseArea {
                        onClicked: backend.open(modelData["path"])
                    }
                }

                Text {
                    id: name
                    text: file.name
                    color: "#E0E0E0"
                    anchors.left: img.right
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: -10
                    anchors.leftMargin: 15
                    font.pixelSize: 16
                    font.weight: Font.Medium
                }

                Text {
                    id: path
                    text: modelData
                    color: "#666666"
                    anchors.left: img.right
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: 10
                    anchors.leftMargin: 15
                    font.pixelSize: 14
                    font.weight: Font.Medium
                }

                MouseArea {
                    width: 540
                    height: 60
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    onClicked: {
                        backend.open(modelData)
                    }
                }

                Image {
                    id: tick
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: img.left
                    anchors.rightMargin: 24

                        source: backend.isSelected(modelData)
                            ? "../icons/checkbox_checked_sharp.svg"
                            : "../icons/checkbox_unchecked_sharp.svg"

                    z: 2

                    MouseArea {
                        anchors.fill: parent

                        onClicked: {
                            tick.source = backend.manager(modelData)
                                ? "../icons/checkbox_checked_sharp.svg"
                                : "../icons/checkbox_unchecked_sharp.svg"
                        }
                    }
                }

                Rectangle {
                    id: deleteButton
                    width: 60
                    height: 60
                    color: "#181818"

                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right

                    Image {
                        anchors.centerIn: parent
                        anchors.horizontalCenterOffset: 1
                        anchors.verticalCenterOffset: 2
                        source: "../icons/trash.svg"
                    }

                    MouseArea {
                        anchors.fill: parent

                        onClicked: {
                            backend.erase(modelData)
                            backend.show()
                        }
                    }
                }
            }
        }
    }
}