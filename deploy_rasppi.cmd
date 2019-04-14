xcopy "*.py"        "\\RASPBERRYPI\obmen\DashBoard\" /E /Y /EXCLUDE:excludelist.txt
xcopy "*.ini"       "\\RASPBERRYPI\obmen\DashBoard\" /E /Y /EXCLUDE:excludelist.txt
xcopy "*.sh"        "\\RASPBERRYPI\obmen\DashBoard\" /E /Y /EXCLUDE:excludelist.txt
xcopy "music\*.*"   "\\RASPBERRYPI\obmen\DashBoard\music\" /E /Y /EXCLUDE:excludelist.txt
xcopy "weather\*.*" "\\RASPBERRYPI\obmen\DashBoard\weather\" /E /Y  /EXCLUDE:excludelist.txt