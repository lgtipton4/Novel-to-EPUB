@echo off
if exist "config.txt" goto exists
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

:next
cls
echo --------------------------------------------------------
echo Would you like to pair a phone with this software? (Y/N) 
echo --------------------------------------------------------
set /p c=
if "%c%"=="Y" goto phone_setup
if "%c%"=="y" goto phone_setup
echo N/A >> config.txt
exit

:kindle_setup
cls
echo Please enter the email associated with your Kindle. If you are unsure of where to find it, review the documentation (https://github.com/lgtipton4/Novel-to-EPUB)
set /p kindle_email=
echo %kindle_email% >> config.txt
goto next

:phone_setup
cls
echo Please enter your phone number with NO spaces. ex. 1234567890
set /p phone_number=
cls
echo Please go to this website (https://www.textsendr.com/emailsms.php), locate your carrier and paste everything after and including the "@" symbol. ex. @tmomail.com. Note that Verizon Wireless no longer supports this feature.
timeout /t 3 >nul
start https://www.textsendr.com/emailsms.php
set /p suffix=
echo %phone_number%%suffix% >> config.txt
cls
echo Succesfully setup.
pause
exit

:exists
echo Setup has already been run. If you wish to change settings, delete the "config.txt" file and rerun this file.
pause
exit
