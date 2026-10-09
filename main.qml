import QtQuick
import "interface"

Window {
    width: 800
    height: 500
    visible: true
    title: "Zhorro"

    Sidebar {
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
    }
}