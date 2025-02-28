@echo off
if exist "config.txt" exit
:top
cls
echo SETUP
echo ---------------------------------------------------------
echo Would you like to pair a kindle with this software? (Y/N)
echo ---------------------------------------------------------
set /p c=
if "%c%"=="Y" goto kindle_setup
if "%c%"=="y" goto kindle_setup
echo N/A >> config.txt
goto next

:kindle_setup
cls
echo Please enter the email associated with your Kindle. If you are unsure of where to find it, review the documentation (https://github.com/lgtipton4/Novel-to-EPUB)
set /p kindle_email=
echo %kindle_email% >> config.txt
goto next

:next
cls
echo --------------------------------------------------------
echo Would you like to opt in to automatic chapter downloads? 
echo --------------------------------------------------------
set /p c=
if "%c%"=="Y" goto automatic_chapter_updates
if "%c%"=="y" goto automatic_chapter_updates
echo N/A >> config.txt
exit

:automatic_chapter_updates
echo automatic_chapter_updates >> config.txt
exit
