@echo off
for /f "delims=" %%a in ('dir /b /a-d .') do (
	if "%%~xa"==".py" (
		autopep8 --in-place --aggressive --aggressive %%a
		echo %%a OK
	)
)
