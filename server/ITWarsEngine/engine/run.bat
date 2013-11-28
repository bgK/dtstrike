@echo OFF
cls
setlocal
echo.

REM TODO :
REM    - specialiser le run pour chaque StarterKit


REM Load config
for /F "tokens=1,* delims==" %%A in (run.conf) do (
	if "%%A"=="map" set map=%%B
	if "%%A"=="bot_cmd" set bot_cmd=%%B
)

REM Check config
if "x%map%" == "x" (
	set error=Map file not specified
	goto config_error
)
if not exist %map% (
	set error=Map file not found
	goto config_error
)
if "x%bot_cmd%" == "x" (
	set error=Invalid command bot
	goto config_error
)
REM Extract nb players from map
for /F "tokens=2 delims=\" %%a in ('echo %map%') do (
	set nb_players=%%a
)
if "x%nb_players%" == "x" (
	set error=Player number not specified
	goto config_error
)
echo %nb_players%| findstr /r "^[2-6]$">nul
if errorlevel 1 (
	set error=Invalid player number
	goto config_error
)

REM Define other bots -- you may replace these commands with your own bots
set bot1="java -jar bots/CrazyBot.jar"
set bot2="java -jar bots/DedicatedBot.jar"
set bot3="java -jar bots/DefensiveBot.jar"
set bot4="java -jar bots/DispersionBot.jar"
set bot5="java -jar bots/FlightyBot.jar"
set bot6="java -jar bots/LooterRageBot.jar"
set bot7="java -jar bots/PatientBot.jar"
set bot8="java -jar bots/WarriorRageBot.jar"

echo Starting game with %nb_players% players on map %map%
echo.
echo In the replay file, your bot is always player 1
echo.

:runEngine
set err_file=replay_err.txt
if %nb_players% == 2 set run_cmd="%bot_cmd%" %bot1%
if %nb_players% == 3 set run_cmd="%bot_cmd%" %bot1% %bot2%
if %nb_players% == 4 set run_cmd="%bot_cmd%" %bot1% %bot2% %bot3%
if %nb_players% == 5 set run_cmd="%bot_cmd%" %bot1% %bot2% %bot3% %bot4%
if %nb_players% == 6 set run_cmd="%bot_cmd%" %bot1% %bot2% %bot3% %bot4% %bot5%

REM Cleaning previous game
del %err_file% 2>NUL
del replay_log.txt 2>NUL
del visu\replay.js 2>NUL

echo var replayJson=>visu\replay.js
java -Duser.language=en -jar engine.jar %map% 1000 1000 replay_log.txt %run_cmd% 1>>visu\replay.js 2>%err_file%
if not "%errorlevel%" == "0" goto error

REM Check if replay_err is empty
for %%A in (%err_file%) do if not %%~zA==0 goto error

REM Launch replay
start visu/index.html
echo.
echo ====================================================================
echo ====================================================================
echo                    	Game over
echo You may watch the replay by opening visu/index.html in your browser
echo ====================================================================
echo ====================================================================
echo.
pause
goto end

:error
echo !!!!!!!!!!!!!!!!! Game crashed !!!!!!!!!!!!!!!!!
echo.
type %err_file%
echo.
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo.
pause
goto end

:usage
echo Wrong usage
echo Usage : run.bat MapName "command for MyFirstBot" "command for MySecondBot"
pause
goto end

:config_error
echo !!!!!!!!!!!!!!!!! Error !!!!!!!!!!!!!!!!!!
echo.
echo Invalid configuration :
echo     %error%
echo.
echo Check the configuration file 'run.conf'
echo.
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo.
pause

:end