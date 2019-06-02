if exist "dist" del /F /Q dist\*
if not exist "dist" mkdir dist
cd src\
python setup.py py2exe > ../dist/build.log 2>&1

copy /Y config.ini ..\dist\ >> ../dist/build.log 2>&1
del log.txt >> ../dist/build.log 2>&1
del ..\dist\log.txt >> ../dist/build.log 2>&1