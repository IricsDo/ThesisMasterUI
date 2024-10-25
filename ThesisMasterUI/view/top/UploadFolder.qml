import QtQuick 2.15
import QtQuick.Layouts 1.15

import "items"

Item {
    required property string background_color

    RowLayout {
        anchors.fill: parent
        spacing: 6

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredWidth: 3*parent.width/4
            Layout.preferredHeight: parent.height

            ColumnLayout{
                spacing: 2
                anchors.fill: parent
                Rectangle {
                    Layout.alignment: Qt.AlignCenter
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: parent.height/2 - parent.spacing

                    UF_Label{
                        anchors.margins: 10
                    }
                }

                Rectangle {
                    Layout.alignment: Qt.AlignCenter
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: parent.height/2 - parent.spacing
                    UF_Label{
                        anchors.margins: 10
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredWidth: parent.width/4
            Layout.preferredHeight: parent.height

            ColumnLayout{
                spacing: 2
                anchors.fill: parent
                Rectangle {
                    Layout.alignment: Qt.AlignCenter
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: parent.height/2 - parent.spacing

                    UF_Button{
                        text_button: "Input folder"
                        color_button: "#7F7F7F"
                    }
                }

                Rectangle {
                    Layout.alignment: Qt.AlignCenter
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: parent.height/2 - parent.spacing

                    UF_Button{
                        text_button: "Output folder"
                        color_button: "#7F7F7F"
                    }
                }
            }
        }
    }
}
