import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Basic
import "../designs"

Rectangle {
    color: "#090909"

    Connections {
        target: backend
    }


    
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

    Button {
        id: resetButton

        width: 100
        height: 50
        anchors.top: title.top
        anchors.right: searchRow.right
        visible: backend.exactResults.length > 0 || backend.semanticResults.length > 0

        text: "Reset"

        font.pixelSize: 16
        font.weight: Font.Medium

        background: Rectangle {

            color: resetButton.pressed
                ? "#5C0A10"
                : resetButton.hovered
                    ? "#8B101A"
                    : "#3A0D11"
        }

        contentItem: Text {
            text: resetButton.text
            color: "#E0E0E0"
            font: resetButton.font
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        onClicked: {
            backend.reset()
            amountText.visible=false
        }
    }

    Row {
        id: searchRow
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
            font.pixelSize: 19

            onClicked: {
                resultsDialog.open()
            }
        }
    }

    Dialog {
        id: resultsDialog

        width: 420
        height: 300

        modal: true
        anchors.centerIn: Overlay.overlay

        padding: 0

        background: Rectangle {
            color: "#111111"
            border.width: 1
            border.color: "#252525"
        }

        Text {
            id: res

            text: "How many results?"
            color: "#E0E0E0"
            font.pixelSize: 22
            font.weight: Font.DemiBold

            anchors {
                top: parent.top
                topMargin: 24
                left: parent.left
                leftMargin: 28
            }
        }

        Text {
            id: choo

            text: "Choose how many results to show for each file"
            color: "#666666"
            font.pixelSize: 13

            anchors {
                left: res.left
                top: res.bottom
                topMargin: 8
            }
        }

        Row {
            id: amountRow
            anchors.centerIn: parent
            anchors.verticalCenterOffset: 10
            spacing: 14

            Rectangle {
                id: decreaseButton

                width: 54
                height: 54

                color: mouseDecrease.containsMouse
                    ? "#242424"
                    : "#1A1A1A"

                border.width: 1
                border.color: "#292929"

                Behavior on color {
                    ColorAnimation {
                        duration: 120
                    }
                }

                Text {
                    anchors.centerIn: parent

                    text: "−"
                    color: "#E0E0E0"

                    font.family: "Inter"
                    font.pixelSize: 28

                    MouseArea {
                        id: mouseDecrease

                        anchors.fill: parent
                        hoverEnabled: true

                        onClicked: {
                            backend.count(0)
                        }
                    }
                }
            }

            Rectangle {
                width: 70
                height: 54

                color: "#181818"

                border.width: 1
                border.color: "#292929"

                Text {
                    anchors.centerIn: parent

                    text: backend.counter
                    color: "#E0E0E0"

                    font.family: "Inter"
                    font.pixelSize: 21
                    font.weight: Font.Medium
                }
            }

            Rectangle {
                id: increaseButton

                width: 54
                height: 54

                color: mouseIncrease.containsMouse ? "#6F0C14" : "#8B101A"

                Behavior on color {
                    ColorAnimation {
                        duration: 120
                    }
                }

                Text {
                    anchors.centerIn: parent

                    text: "+"
                    font.pixelSize: 28

                    MouseArea {
                        id: mouseIncrease

                        anchors.fill: parent
                        hoverEnabled: true

                        onClicked: {
                            backend.count(1)
                        }
                    }
                }
            }
        }

        Text {
            id: advice
            anchors.top: amountRow.bottom
            anchors.topMargin: 8
            anchors.horizontalCenter: parent.horizontalCenter
            text: "(remain 0 for all)"
            color: "#666666"
            font.pixelSize: 13
        }

        Text {
            id: cancelButton

            text: "Cancel"

            color: cancelMouse.containsMouse
                ? "#E0E0E0"
                : "#777777"

            font.family: "Inter"
            font.pixelSize: 14
            font.weight: Font.Medium

            anchors {
                bottom: parent.bottom
                bottomMargin: 22
                left: parent.left
                leftMargin: 28
            }

            Behavior on color {
                ColorAnimation {
                    duration: 120
                }
            }

            MouseArea {
                id: cancelMouse

                anchors.fill: parent
                hoverEnabled: true

                onClicked: {
                    resultsDialog.reject()
                }
            }
        }

        Rectangle {
            id: okButton

            width: 90
            height: 38
            color: okMouse.containsMouse ? "#6F0C14" : "#8B101A"

            anchors {
                bottom: parent.bottom
                bottomMargin: 18
                right: parent.right
                rightMargin: 24
            }

            Behavior on color {
                ColorAnimation {
                    duration: 120
                }
            }

            Text {
                anchors.centerIn: parent

                text: "Search"
                font.pixelSize: 14
                font.weight: Font.DemiBold
            }

            MouseArea {
                id: okMouse

                anchors.fill: parent
                hoverEnabled: true

                onClicked: {
                    resultsDialog.accept()
                }
            }
        }

        onAccepted: {
            backend.search(inputSearch.text)
            amountText.visible=true
        }
    }

    Text {
        id: amountText
        visible: resultsColumn.height>0

        anchors {
            left: searchRow.left
            top: searchRow.bottom
            topMargin: 25
        }

        font.pixelSize: 30
        font.weight: Font.DemiBold
        text: backend.fileCounter > 1
            ? `${backend.resultsCounter} matches · ${backend.fileCounter} files`
            : backend.fileCounter === 1
            ? `${backend.resultsCounter} matches · ${backend.fileCounter} file`
            : backend.selected.length === 0 
            ? "No files are selected. Select them at the Files page.":
            "No matches found"
        color: "#CFCFCF"
    }

    ScrollView {
        id: resultsScroll

        anchors {
            left: parent.left
            right: parent.right
            top: amountText.bottom
            bottom: parent.bottom
            topMargin: 15
        }

        clip: true

        Column {
            id: resultsColumn
            width: resultsScroll.availableWidth - 80
            x: 40
            spacing: 12


           Repeater {
                model: backend.results

                delegate: ResultCard {
                    width: resultsColumn.width

                    filename: modelData.filename
                    path: modelData.path

                    contexts: modelData.exact
                    semanticResults: modelData.semantic
                }
            }
        }
    }
}
