import QtQuick
import QtQuick.Controls.Basic

Rectangle {
    id: card

    property bool expanded: false

    property string filename: ""
    property string path: ""

    property var contexts: []
    property var semanticResults: []

    property string extension: card.filename.slice(card.filename.lastIndexOf("."))

    height: expanded ? content.height + 70 : 70
    color: "#111111"

    Row {
        id: header

        anchors {
            left: parent.left
            leftMargin: 40
            right: parent.right
            rightMargin: 20
            top: parent.top
            margins: 16
        }

        height: 38

        Image {
            transform: Translate {
                y: 4
                x: -20
            }
            source: card.extension === ".pdf"
                        ? Qt.resolvedUrl("../icons/file-earmark-pdf copy.svg")
                        : card.extension === ".docx"
                        ? Qt.resolvedUrl("../icons/filetype-docx copy.svg")
                        : Qt.resolvedUrl("../icons/filetype-txt copy.svg")

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    backend.open(card.path)
                }
            }
            
        }

        Text {
            id: filenameText
            text: card.filename
            color: "white"
            font.pixelSize: 18
            font.weight: Font.Medium
            transform: Translate {
                y: -12
            }

            anchors.verticalCenter: parent.verticalCenter
        }
    }

    Text {

        text: card.path
        color: "#777777"
        font.pixelSize: 12
        font.weight: Font.Medium
        anchors.bottom: header.bottom
        anchors.left: header.left
        anchors.leftMargin: 30


        elide: Text.ElideMiddle
    }

    Image {
        id: arrow

        source: card.expanded ? "../icons/chevron-up.svg" : "../icons/chevron-down.svg"

        y: 20
        anchors.right: parent.right
        anchors.rightMargin: 23

        MouseArea {
            anchors.fill: parent

            onClicked: {
                    card.expanded = !card.expanded
            }
        }
    }

    Column {
        id: content

        anchors {
            left: parent.left
            right: parent.right
            top: header.bottom
            margins: 16
        }

        spacing: 14
        visible: card.expanded

        Column {
            width: parent.width
            spacing: 10

            visible: card.contexts.length > 0

            Text {
                text: "Exact matches"
                color: "white"
                font.pixelSize: 16
                font.weight: Font.DemiBold
            }

            Repeater {
                model: card.contexts

                delegate: Rectangle {

                    width: parent.width
                    height: exactContent.height + 20
                    color: "#111111"

                    Column {
                        id: exactContent

                        anchors {
                            left: parent.left
                            right: parent.right
                            top: parent.top
                            margins: 10
                        }

                        spacing: 4

                        Text {
                            text: (modelData.page !== undefined && card.extension == ".pdf")
                                  ? `Page ${modelData.page}`
                                  : (modelData.paragraph !== undefined && card.extension == ".docx")
                                    ? `Paragraph ${modelData.paragraph}`
                                    : `Line ${modelData.line_number}`

                            color: "#999999"
                            font.pixelSize: 12
                        }

                        Text {
                            width: parent.width
                            text: modelData.previous
                            color: "#666666"
                            wrapMode: Text.Wrap
                        }

                        Text {
                            width: parent.width
                            text: modelData.current
                            color: "white"
                            font.weight: Font.DemiBold
                            wrapMode: Text.Wrap
                        }

                        Text {
                            width: parent.width
                            text: modelData.upcoming
                            color: "#666666"
                            wrapMode: Text.Wrap
                        }
                    }
                }
            }
        }

        Column {
            width: parent.width
            spacing: 10

            visible: card.semanticResults.length > 0

            Text {
                text: "Semantic matches"
                color: "white"
                font.pixelSize: 16
                font.weight: Font.DemiBold
            }

            Repeater {
                model: card.semanticResults

                delegate: Rectangle {
                    width: parent.width
                    height: semanticContent.height + 20

                    color: "#111111"

                    Column {
                        id: semanticContent

                        anchors {
                            left: parent.left
                            right: parent.right
                            top: parent.top
                            margins: 10
                        }

                        spacing: 6

                        Text {
                            text: (modelData.page !== null && card.extension == ".pdf")
                                  ? `Page ${modelData.page} · Lines ${modelData.start}–${modelData.end}`
                                  : `Lines ${modelData.start}–${modelData.end}`

                            color: "#999999"
                            font.pixelSize: 12
                        }

                        Text {
                            text: `Similarity · ${modelData.similarity.toFixed(3)}`
                            color: "#FB222C"
                            font.pixelSize: 12
                            font.weight: Font.DemiBold
                        }

                        Text {
                            width: parent.width
                            text: modelData.chunk
                            color: "#D0D0D0"
                            wrapMode: Text.Wrap
                        }
                    }
                }
            }
        }
    }
}