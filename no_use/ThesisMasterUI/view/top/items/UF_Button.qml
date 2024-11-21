import QtQuick 2.15
import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.15

Item {
    required property string text_button
    required property string color_button

    FileDialog {
        id: folderDialog
        title: "Please choose a folder"
        folder: shortcuts.desktop
        selectFolder : true
        onAccepted: {
            console.log("You chose: " + folderDialog.folder)
        }
        onRejected: {
            console.log("Folder Canceled")
        }
    }

    Button {
        id: control
        text: text_button
        contentItem: Text {
            text: control.text
            font: control.font
            opacity: enabled ? 1.0 : 0.3
            color: "black"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }

        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            color: control.hovered ? "#0DC3F1" : color_button
            opacity: enabled ? 1 : 0.3
            radius: 2
        }

        onClicked: {
            folderDialog.open()
        }
    }
}
