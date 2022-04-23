timeout /T 2 /NOBREAK
taskkill /F /IM n2n_client.exe
move update\* .\
move update\Ver\* .\Ver
rd /s/q update\Ver
rd /s/q debug.log
pause