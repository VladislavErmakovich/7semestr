@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title Лабораторная работа 3

:MENU
cls
echo ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
echo ♥        МЕНЮ (не блюд)         ♥  
echo ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥
echo.
echo [1] ► Резервное копирование 
echo [2] ► Анализ логов 
echo [3] ► Тестирование портов 
echo [4] ► Процессы пользователя 
echo [5] ► Производительность 
echo [6] ► Выход 

echo.
choice /C 123456 /N /M ""
cls

if %errorlevel% equ 1 goto RESERV_COPY
if %errorlevel% equ 2 goto SYSTEMINFO
if %errorlevel% equ 3 goto PORT_TEST
if %errorlevel% equ 4 goto TASKLIST
if %errorlevel% equ 5 goto PERFORMANCE
if %errorlevel% equ 6 goto EXIT
goto MENU

:RESERV_COPY
cls
set "source=E:\4 курс\7semestr\СОМЕД\lab3"
set "destination=E:\4 курс\7semestr\ПОВМС\lab3\резерв"

echo ╔═══════════════════════════╗
echo ║ ♂ РЕЗЕРВНОЕ КОПИРОВАНИЕ ♀ ║
echo ╚═══════════════════════════╝
echo.

set count=0

if not exist "%source%" (
    echo [ОШИБКА] Исходная папка не найдена!
    echo Путь: %source%
    pause
    goto MENU
)

if not exist "%destination%" (
    echo Создание папки назначения...
    mkdir "%destination%"
)

echo Источник:    %source%
echo Назначение:  %destination%
echo.
echo Начинаем копирование...
echo.

for %%F in ("%source%\*.*") do (
    echo [!count!] Копирование: %%~nxF
    copy "%%F" "%destination%\" > nul 2>&1
    
    if !errorlevel! equ 0 (
        set /a count+=1
    ) else (
        echo    └─ [ОШИБКА] Не удалось скопировать
    )
)

echo.
echo ══════════════════════
echo Копирование завершено!
echo Скопировано файлов: !count!
echo ══════════════════════
pause
goto MENU

:SYSTEMINFO
cls
echo ╔══════════════════╗
echo ║ ♠ Анализ логов ♠ ║
echo ╚══════════════════╝
echo.
echo Информация о системе:
echo.
systeminfo | findstr /I "Host.*Name OS.*Name Version Manufacturer"

echo.
pause
goto MENU

:PORT_TEST
cls
echo ╔═════════════════════════╗
echo ║ ♪ Тестирование портов ♪ ║
echo ╚═════════════════════════╝
echo.
echo Активные сетевые подключения:
netstat -an | findstr "LISTENING"
echo.
pause
goto MENU

:TASKLIST
cls
echo ╔═══════════════════════════╗
echo ║ ¾ Процессы пользователя ¼ ║
echo ╚═══════════════════════════╝
echo.
tasklist /V | findstr /C:"%username%"
pause
goto MENU

:PERFORMANCE
cls
echo ╔════════════════════════╗
echo ║ ¾ Производительность ¼ ║
echo ╚════════════════════════╝
echo.
echo Использование памяти:
wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value
echo Загрузка процессора:
wmic cpu get loadpercentage /value
echo Информация о дисках:
wmic logicaldisk get name,size,freespace /format:list
pause
goto MENU

:EXIT
cls
echo.
echo      ╔══════════╗
echo      ║ Прощай ♂ ║
echo      ╚══════════╝
timeout /t 6 > nul
cls
exit