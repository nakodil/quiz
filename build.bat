@echo off
chcp 65001 >nul
echo Building with PyInstaller...

pyinstaller main.py ^
    --noconsole ^
    --icon=icon.ico ^
    --add-data "assets;assets" ^
    --name=Знатоки_ПДД ^
    --distpath=dist

echo Build finished. Output is in the "dist" folder.
