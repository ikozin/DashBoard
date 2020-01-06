rmdir "\\192.168.1.65\obmen\DashBoard" /S /Q
xcopy "*.py"        "\\192.168.1.65\obmen\DashBoard\" /E /Y /EXCLUDE:excludelist.txt
xcopy "*.ini"       "\\192.168.1.65\obmen\DashBoard\" /E /Y /EXCLUDE:excludelist.txt
xcopy "*.sh"        "\\192.168.1.65\obmen\DashBoard\" /E /Y /EXCLUDE:excludelist.txt
xcopy "music\*.*"   "\\192.168.1.65\obmen\DashBoard\music\" /E /Y /EXCLUDE:excludelist.txt
xcopy "weather\*.*" "\\192.168.1.65\obmen\DashBoard\weather\" /E /Y  /EXCLUDE:excludelist.txt