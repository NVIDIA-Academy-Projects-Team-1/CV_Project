// alarm.js
var myWindow = null;
var audio = null;

function openAlarmWindow() {
    myWindow = window.open("", "AlarmWindow", "width=200,height=100");
    myWindow.document.write("<p style='text-align:center;'>실신이 감지되었습니다.</p>");
    audio = new Audio('/CV_Project/alarm-clock-short-6402.mp3');
    audio.play();
}

function closeAlarmWindow() {
    if (myWindow !== null) {
        myWindow.close();
    }
    if (audio !== null) {
        audio.pause();
    }
}
