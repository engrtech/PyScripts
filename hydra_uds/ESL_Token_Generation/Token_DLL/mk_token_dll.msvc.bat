@REM --------------------------------------------------------------------
@REM Batch file to build DLL for token exchange.
@REM --------------------------------------------------------------------

@REM Keep changes to environment variables local to this batch file.
SETLOCAL

@REM Create a directory to store the object files
IF NOT EXIST obj_dll_msvc MKDIR obj_dll_msvc
@IF %ERRORLEVEL% NEQ 0 GOTO EndError

@REM Compile the sources
%OPENECU_MSVC_V2008%cl.exe /nologo /W3 /EHsc /O2 /D "WIN32" /D "_MBCS" /I%OPENECU_MSVC_V2008%\..\include /I%OPENECU_WINDOWS_SDK%Include /Foobj_dll_msvc/token_dll.o    /c token_dll.c
@IF %ERRORLEVEL% NEQ 0 GOTO EndError

@REM Compile the sources
%OPENECU_MSVC_V2008%cl.exe /nologo /W3 /EHsc /O2 /D "WIN32" /D "_MBCS" /I%OPENECU_MSVC_V2008%\..\include /I%OPENECU_WINDOWS_SDK%Include /Foobj_dll_msvc/aes-cbc-cmac.o /c aes_cmac_rfc\aes-cbc-cmac.c
@IF %ERRORLEVEL% NEQ 0 GOTO EndError

@REM Compile the sources
%OPENECU_MSVC_V2008%cl.exe /nologo /W3 /EHsc /O2 /D "WIN32" /D "_MBCS" /I%OPENECU_MSVC_V2008%\..\include /I%OPENECU_WINDOWS_SDK%Include /Foobj_dll_msvc/TI_aes_128.o   /c aes_cmac_rfc\TI_aes_128.c
@IF %ERRORLEVEL% NEQ 0 GOTO EndError

@REM Create a directory to store the binary files
IF NOT EXIST bin_dll_msvc MKDIR bin_dll_msvc
@IF %ERRORLEVEL% NEQ 0 GOTO EndError

@REM Remove previous build file to avoid accumulating old and new objects into the same file
IF EXIST bin_dll_msvc\token_dll.dll DEL /Q /F bin_dll_msvc\token_dll.dll
@IF %ERRORLEVEL% NEQ 0 GOTO EndError

@REM /libpath:%OPENECU_MSVC_V2008%..\VC\ATLMFC\LIB
@REM Create the DLL
%OPENECU_MSVC_V2008%link.exe /nologo /libpath:%OPENECU_WINDOWS_SDK%Lib /libpath:%OPENECU_MSVC_V2008%..\lib obj_dll_msvc/token_dll.o obj_dll_msvc/aes-cbc-cmac.o obj_dll_msvc/TI_aes_128.o /DLL /OUT:bin_dll_msvc/token_dll.dll
@IF %ERRORLEVEL% NEQ 0 GOTO EndError

@GOTO End

:EndError

@ECHO Error: build incomplete.

:End

@REM Return to the same directory as the batch file was started in.
CD %~dp0
