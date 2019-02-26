@echo off

set DARKNET=%DARKNET_DIR%/darknet.exe

REM new_examples.txt should contain lines with paths to new training examples
REM the result will be (for each example) a txt.file that contains the detected labels

%DARKNET% detector test tablesoccer.data yolov3-tablesoccer.cfg weights/yolov3-tablesoccer_last.weights -thresh 0.25 -dont_show -save_labels < new_examples.txt