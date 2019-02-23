@echo off

set DARKNET=%DARKNET_DIR%/darknet.exe

REM Download default weights file for yolov3-tiny: https://pjreddie.com/media/files/yolov3-tiny.weights
REM Get pre-trained weights yolov3-tiny.conv.15 using command: darknet.exe partial cfg/yolov3-tiny.cfg yolov3-tiny.weights yolov3-tiny.conv.15 15

:start

if exist weights/yolov3-tablesoccer_last.weights (
    %DARKNET% detector train tablesoccer.data yolov3-tablesoccer.cfg weights/yolov3-tablesoccer_last.weights -map
) else (
    %DARKNET% detector train tablesoccer.data yolov3-tablesoccer.cfg %DARKNET_DIR%/yolov3-tiny.conv.15 -map
)

goto start