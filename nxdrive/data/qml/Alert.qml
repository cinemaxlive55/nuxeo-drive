import QtQuick 2.13

ShadowRectangle {
    id: control

    property string text
    property int size: 12
    property int padding: 10
    height: content.contentHeight + (padding * 2)

    radius: 2

    signal display(string msg, string type)

    onDisplay: {
        if (type == 'error') {
            control.color = red
        } else {
            control.color = lightBlue
        }
        control.text = msg
        control.visible = true
        timer.running = true
    }

    ScaledText {
        id: content
        anchors.fill: parent
        padding: control.padding
        color: "white"

        text: control.text
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    Timer {
        id: timer
        interval: 5000
        onTriggered: { control.visible = false }
    }
}
