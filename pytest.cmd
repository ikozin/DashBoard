rem "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\pytest.exe" --help
xcopy setting.py test\ /y
xcopy exceptions.py test\ /y
rem "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\pytest.exe" -v --setup-show  test\test_block_alarm.py
"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\pytest.exe" -v --setup-show
pause