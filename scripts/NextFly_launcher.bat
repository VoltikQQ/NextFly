rem NextFly Project Launcher - Copyright (c) 2024 AngelDragon999
rem Licensed under the MIT License. See LICENSE for details.
@echo off
cls
rem ===============================
rem  Project Launcher - Batch Tool
rem ===============================

rem =========================================================
rem   Load configuration from external file
rem =========================================================
set "CONFIG_PATH=..\config\config.env.example"

if exist "%CONFIG_PATH%" (
    for /f "usebackq tokens=* delims=" %%a in (`type "%CONFIG_PATH%"`) do (
        set "%%a"
    )
) else (
    echo ERROR: File config.env not found.
    pause
    goto exit
)

rem ===============================
rem  Automatic project starter
rem ===============================

rem =========================================================
rem   Check required variables
rem =========================================================
if "%JDKS_DIRECTORY%"=="" (
    echo ERROR: JAVA_JDK_HOME variable is not set.
    pause
    goto exit
)

:mainMenu
cls
echo 888b    888 8888888888 Y88b   d88P 88888888888 .d888 888
echo 8888b   888 888         Y88b d88P      888    d88P\"  888          
echo 88888b  888 888          Y88o88P       888    888    888          
echo 888Y88b 888 8888888       Y888P        888    888888 888 888  888 
echo 888 Y88b888 888           d888b        888    888    888 888  888 
echo 888  Y88888 888          d88888b       888    888    888 888  888 
echo 888   Y8888 888         d88P Y88b      888    888    888 Y88b 888 
echo 888    Y888 8888888888 d88P   Y88b     888    888    888  \"Y88888 
echo                                                               888 
echo                                                          Y8b d88P 
echo                                                           \"Y88P\"  
echo.
echo Welcome to the automatic project starter and compiler for ongoing projects!
echo.
echo =====================================================
echo Would You like to start or build the project?
echo =====================================================
echo.
echo       1) Build
echo       2) Starting server
echo       0) ^EXIT
echo.

set /p initialChoice=Please enter the number below (0 - 2):
echo.

if "%initialChoice%"=="1" goto build
if "%initialChoice%"=="2" goto run
if "%initialChoice%"=="0" goto exit

echo Invalid choice. Please try again.
pause
goto mainMenu

rem ==================================
rem				RUN
rem ==================================
:run
cls
echo  Let's run the project! Which project do You want to start?
echo.
echo      1) Project A - Web/API
echo      2) Project A - Core
echo      3) Project B - Web/API
echo      4) Project B - Core
echo      0) Back
echo.

set /p runChoice=Enter the number (0 - 4) below: 
echo.

if "%runChoice%"=="1" goto run_A_WEB
if "%runChoice%"=="2" goto run_A_CORE
if "%runChoice%"=="3" goto run_B_WEB
if "%runChoice%"=="4" goto run_B_CORE
if "%runChoice%"=="0" goto mainMenu

echo Invalid choice. Please try again.
pause
goto run

:run_A_WEB
cls
echo You have chosen  Project A - Web/API
call:setJdk8
echo.
java -version
echo.
call "%SERVERS%%PROJECT_A_WEB_STANDALONE_BAT%" --server-config=standalone.xml
goto end

:run_A_CORE
cls
echo You have chosen Project A - Core
call:setJdk8
echo.
java -version
echo.
call "%SERVERS%%PROJECT_A_CORE_STANDALONE_BAT%" --server-config=standalone.xml
goto end

:run_B_WEB
cls
echo You have chosen Project B - Web/API
call:setJdk8
echo.
java -version
echo.
call "%SERVERS%%PROJECT_B_WEB_STANDALONE_BAT%" ^
 -Dprogram.name="JBossTools: Application Server" ^
 -DXms1024m -DXmx1024m ^
 -DXX:MetaspaceSize=96M -DXX:MaxMetaspaceSize=256m ^
 -Dorg.jboss.resolver.warning=true ^
 -Djava.net.preferIPv4Stack=true ^
 -Dsun.rmi.dgc.client.gcInterval=3600000 ^
 -Dsun.rmi.dgc.server.gcInterval=3600000 ^
 -Djboss.modules.system.pkgs=org.jboss.byteman ^
 -Djava.awt.headless=true ^
 -Dorg.jboss.boot.log.file="%SERVERS%\jboss-eap-standalone\log\boot.log" ^
 -Dlogging.configuration="file:%SERVERS%\jboss-eap-standalone\configuration\logging.properties" ^
 -Djboss.home.dir="%SERVERS%\jboss-eap-standalone" ^
 -Dorg.jboss.logmanager.nocolor=true ^
 -Djboss.bind.address.management=localhost ^
 -Djboss.app.conf.dir="%PROJECT_B_WEB%\shared\configuration" ^
 -Dorg.apache.activemq.SERIALIZABLE_PACKAGES="*" ^
 --server-config=standalone.xml
goto end

:run_B_CORE
cls
echo You have chosen Project B - Core
call:setJdk21
echo.
java -version
echo.
java -Dlogging.config="%PROJECT_B%\config\logback-spring.xml" ^
     -Djboss.app.conf.dir="%PROJECT_B%\config\configuration" ^
     -jar "%PROJECT_B_CORE%\target\project-b-core.jar" ^
     --spring.config.location="file:%PROJECT_B%\config\application.properties"
goto end

rem =============================
rem           BUILD
rem =============================
:build
cls
echo Which project would You like to build?
echo.
echo      1) Project A - Web/API
echo      2) Project A - Core
echo      3) Project B - Web/API
echo      4) Project B - Core
echo      0) Back
echo.

set /p buildChoice=Enter the number (0 - 4) below: 
echo.

if "%buildChoice%"=="1" goto build_A_WEB
if "%buildChoice%"=="2" goto build_A_CORE
if "%buildChoice%"=="3" goto build_B_WEB
if "%buildChoice%"=="4" goto build_B_CORE
if "%buildChoice%"=="0" goto mainMenu

echo Invalid choice. Please try again.
pause
goto build

:build_A_WEB
cls
rem set the correct JDK right away:
call:setJdk8
cd %PROJECT_A%

echo Removing old package project_a_web
del %SERVERS%%PROJECT_A_WEB_STANDALONE%\project_a_web.*
echo.

echo Removing old package project_a_api
del %SERVERS%%PROJECT_A_WEB_STANDALONE%\project_a_api.*

call mvn -T 1 --settings %MAVEN_HOME%%PROJECT_A_MAVEN_CONFIG% -DXms4096m -DXmx4096m -DXX:PermSize=1024m -DXss240m -Dmaven.wagon.http.ssl.insecure=true clean install -pl project_a_web,project_a_api -am

copy %PROJECT_A%\project_a_web\target\project_a_web.war  %SERVERS%%PROJECT_A_WEB_STANDALONE%\project_a_web.war
copy %PROJECT_A%\project_a_api\target\project_a_api.war  %SERVERS%%PROJECT_A_WEB_STANDALONE%\project_a_api.war

pause
call:notify
goto:run_A_WEB

:build_A_CORE
cls
rem set the correct JDK right away:
call:setJdk8
cd %PROJECT_A%

echo Removing old package tm (transaction-manager)
del %SERVERS%%PROJECT_A_CORE_STANDALONE%\tm.*
echo.

call mvn --settings %MAVEN_HOME%%PROJECT_A_MAVEN_CONFIG% -DXss20m -Dmaven.wagon.http.ssl.insecure=true clean install -pl transaction-manager -am

copy %PROJECT_A%\transaction-manager\target\tm.war %SERVERS%%PROJECT_A_CORE_STANDALONE%\tm.war

pause
call:notify
goto:run_A_CORE

:build_B_WEB
cls
:warning
echo   ======================================================================
echo ^| WARNING: Some worning message for this type of build...              ^|
echo   ======================================================================

set /p option=Enter "Y" below to confirm or "N" to return to the previous menu:

if /i "%option%"=="Y" goto build_confirmation
if /i "%option%"=="N" goto build

echo Invalid choice. Please try again.
pause
goto warning

:build_confirmation
cls
rem set the correct JDK right away:
call:setJdk8
cd %PROJECT_A%

echo Removing old package project_a_api
del %SERVERS%%PROJECT_A_WEB_STANDALONE%\project_a_api.*

call mvn -T 1 --settings %MAVEN_HOME%%PROJECT_A_MAVEN_CONFIG% -DXms4096m -DXmx4096m -DXX:PermSize=1024m -DXss240m -Dmaven.wagon.http.ssl.insecure=true clean install -pl project_a_api -am

copy %PROJECT_A%\project_a_api\target\project_a_api.war  %SERVERS%%PROJECT_A_WEB_STANDALONE%\project_a_api.war

pause
call:notify
goto:run_B_WEB

:build_B_CORE
cls
rem set the correct JDK right away:
call:setJdk8
cd %R2P_WEB%

echo Removing old package project_b_api
del %SERVERS%%R2P_WEB_STANDALONE%\project_b_api.*
echo.

echo Removing old package project_b_web
del %SERVERS%%R2P_WEB_STANDALONE%\project_b_web.*

call mvn -T 1 --settings %MAVEN_HOME%%PROJECT_B_MAVEN_CONFIG% -DXms4096m -DXmx4096m -DXX:PermSize=1024m -DXss240m -Dmaven.wagon.http.ssl.insecure=true -Dmaven.test.skip=true clean install -pl project_b_web -am

copy %R2P_WEB%\r2p-reports\target\project_b_api.war %SERVERS%%R2P_WEB_STANDALONE%\project_b_api.war
copy %R2P_WEB%\project_b_web\target\project_b_web.war %SERVERS%%R2P_WEB_STANDALONE%\project_b_web.war

pause
call:notify
goto:run_B_WEB

cls
:notify
echo   ======================================================================
echo ^|                                                                      ^|
echo ^| BUILD COMPLETE: Do you want to run the project now?                  ^|
echo ^|                                                                      ^|
echo   ======================================================================

set /p decision=Enter "Y" below to confirm or "N" to return to the previous menu:

if /i "%decision%"=="Y" goto eof
if /i "%decision%"=="N" goto mainMenu

echo Invalid choice. Please try again.
pause
goto notify

rem ===========================
rem     CONFIGURATORE JDK
rem ===========================

:setJdk8
set "PATH=%JDKS_DIRECTORY%%JDK_8%;%PATH%"
goto:eof

:setJdk21
set "PATH=%JDKS_DIRECTORY%%JDK_21%;%PATH%"
goto:eof

rem ==========================

:end
echo.
choice /C SN /N /M "Press S to return to the menu or N to ^exit..."
if errorlevel 2 goto exit
if errorlevel 1 goto mainMenu

:exit
cls
echo.
echo Thank you for using the program!
timeout /t 2 >nul
exit
