@ECHO OFF
color 3F
echo     ------------------
echo         A) LAT
echo         B) DDT
echo         C) S-BOX
echo     ------------------

:choice
set /P c= "-          Start:"
if /I "%c%" EQU "A" goto :lat
if /I "%c%" EQU "B" goto :ddt
if /I "%c%" EQU "C" goto :sbox
goto :choice

:lat

python LAT.py
pause
exit

:ddt

python DDT.py
pause
exit

:sbox

python s-Box.py
python LAT.py -sbox
python DDT.py -sbox
pause
exit