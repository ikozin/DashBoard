if "%1"=="" exit 1
rmdir "\\%1\obmen\DashBoard" /S /Q
xcopy "*.py"        "\\%1\obmen\DashBoard\" /E /Y /EXCLUDE:excludelist.txt
xcopy "*.ini"       "\\%1\obmen\DashBoard\" /E /Y /EXCLUDE:excludelist.txt
xcopy "*.sh"        "\\%1\obmen\DashBoard\" /E /Y /EXCLUDE:excludelist.txt
xcopy "music\*.*"   "\\%1\obmen\DashBoard\music\" /E /Y /EXCLUDE:excludelist.txt
xcopy "weather\*.*" "\\%1\obmen\DashBoard\weather\" /E /Y  /EXCLUDE:excludelist.txt