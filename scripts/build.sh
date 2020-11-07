#!/bin/bash
# setting.ini
sed -i -e 's/<OPENWEATHERMAP_KEY>/'${OPENWEATHER_KEY}'/g' setting.ini
sed -i -e 's/<YANDEXVOICE_KEY>/'${YANDEX_VOICE_KEY}'/g' setting.ini
sed -i -e 's/<WUNDERGROUND_KEY>/'${WUNDERGROUND_KEY}'/g' setting.ini
# setting_opiwin.ini
sed -i -e 's/<OPENWEATHERMAP_KEY>/'${OPENWEATHER_KEY}'/g' setting_opiwin.ini
sed -i -e 's/<YANDEXVOICE_KEY>/'${YANDEX_VOICE_KEY}'/g' setting_opiwin.ini
sed -i -e 's/<WUNDERGROUND_KEY>/'${WUNDERGROUND_KEY}'/g' setting_opiwin.ini
# setting_rasppi.ini
sed -i -e 's/<OPENWEATHERMAP_KEY>/'${OPENWEATHER_KEY}'/g' setting_rasppi.ini
sed -i -e 's/<YANDEXVOICE_KEY>/'${YANDEX_VOICE_KEY}'/g' setting_rasppi.ini
sed -i -e 's/<WUNDERGROUND_KEY>/'${WUNDERGROUND_KEY}'/g' setting_rasppi.ini
# setting_win.ini
sed -i -e 's/<OPENWEATHERMAP_KEY>/'${OPENWEATHER_KEY}'/g' setting_win.ini
sed -i -e 's/<YANDEXVOICE_KEY>/'${YANDEX_VOICE_KEY}'/g' setting_win.ini
sed -i -e 's/<WUNDERGROUND_KEY>/'${WUNDERGROUND_KEY}'/g' setting_win.ini
# zip
zip build -R ext modules music weather "*.py" "*.ini" "*.sh" "*.cmd" "*.txt" "*.mp3" "*.png" "*.gif" -x test/*