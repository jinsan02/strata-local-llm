@echo off
rem Run the STRATA CLI with the conda env strata_local_llm (no .venv).
rem Engine checkout: C:\strata-lab\engine   Model data: C:\strata-lab\data (both outside git)
rem Example: scripts\strata.cmd launch --plan --family qwen36 --model ud-q4_k_xl --data-dir C:\strata-lab\data
rem (ASCII only: cmd.exe reads .cmd files in the console code page)
setlocal
set "STRATA_PYTHON=C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe"
call "C:\strata-lab\engine\bin\strata.cmd" %*
exit /b %ERRORLEVEL%
