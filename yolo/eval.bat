@echo off

set DARKNET=%DARKNET_DIR%/darknet.exe

for /f %%f in ('dir /b weights') do (
	echo %%f >> eval.txt
	%DARKNET% detector map tablesoccer.data yolov3-tablesoccer.cfg weights/%%f -iou_thresh 0.25 >> eval.txt
)
rem darknet.exe detector map data/voc.data cfg/yolov2-voc.cfg yolo-voc.weights