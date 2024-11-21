import QtQuick 2.15
import QtQuick.Layouts 1.15

import "top"
Item {
    readonly property color background_color : "#4E4A4A"
    Rectangle{
        anchors.fill: parent
        color: background_color

        ColumnLayout{
            spacing: 2
            anchors.fill: parent
            Rectangle {
                Layout.alignment: Qt.AlignTop
                Layout.preferredWidth: parent.width
                Layout.preferredHeight: parent.height/4
                color:  background_color

                UploadFolder{
                    background_color: background_color
                    anchors.fill: parent
                }
            }

            Rectangle {
                Layout.alignment: Qt.AlignCenter
                color: "green"
                Layout.preferredWidth: parent.width
                Layout.preferredHeight: parent.height/2
            }

            Rectangle {
                Layout.alignment: Qt.AlignBottom
                Layout.fillHeight: true
                color: "blue"
                Layout.preferredWidth: parent.width
                Layout.preferredHeight: parent.height/4
            }
        }
    }
}
