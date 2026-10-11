import QtQuick
import QtQuick.Controls
import "interface"
import "interface/pages"

Window {
    title: "Zhorro"
    width: 1040
    height: 700
    visible: true
    minimumWidth: 800
    minimumHeight: 550

    StackView {
        id: pages

        anchors.left: sidebar.right
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom

        initialItem: GreetingPage {}
    }

    Sidebar {
        id: sidebar
        pageStack: pages

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
    }
}