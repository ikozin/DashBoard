#!/usr/bin/python3

from configparser import ConfigParser
from tkinter import ttk, filedialog, Tk, Listbox, StringVar, N, S, E, W
from ext.modal_dialog import VerticalScrolledFrame
from ext.main_manager import MainManager
from ext.time_manager import TimeManager
from ext.alarm_manager import AlarmManager
from ext.voice_manager import VoiceManager
from ext.yandex_news_manager import YandexNewsManager
from ext.calendar_manager import CalendarManager
from ext.open_weather_map_manager import OpenWeatherMapManager
# from ext.wunder_ground_manager import WunderGroundManager
from ext.swap_manager import SwapManager
from ext.watcher_manager import WatcherManager
from ext.mt8057_manager import MT8057Manager
from ext.yandex_weather_manager import YandexWeatherManager
from ext.ir_manager import IRManager
from ext.bme280_manager import Bme280Manager
from ext.volume_manager import VolumeManager


class App:
    """description of class"""

    def __init__(self):
        self._manager_list = {
            "Main": MainManager,
            "Time": TimeManager,
            "Alarm": AlarmManager,
            "Voice": VoiceManager,
            "YandexNews": YandexNewsManager,
            "OpenWeatherMap": OpenWeatherMapManager,
            # "WunderGround": WunderGroundManager,
            "Calendar": CalendarManager,
            "Swap": SwapManager,
            "Watcher": WatcherManager,
            "MT8057": MT8057Manager,
            "YandexWeather": YandexWeatherManager,
            "IR": IRManager,
            "BME280": Bme280Manager,
            "Volume": VolumeManager,
        }
        self._list = dict()
        self._current__name = None
        self._root = Tk()
        self._root.title('DashBoard Tool')
        self._root.columnconfigure(1, weight=1)
        self._root.rowconfigure(1, weight=1)
        self._root.minsize(740, 480)
        self._filename = StringVar()
        header = ttk.LabelFrame(self._root, text="Configuration")
        header.grid(row=0, column=0)
        header.columnconfigure(4, weight=1)
        ttk.Entry(header, width=24, textvariable=self._filename).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(header, text="...", command=self.select_file).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(header, text="Load", command=self.load_data).grid(row=0, column=2, padx=2, pady=2)
        ttk.Button(header, text="Save", command=self.save_data).grid(row=0, column=3, padx=2, pady=2)
        window = ttk.Frame(self._root)
        window.grid(row=1, column=0, columnspan=2, sticky=(N, S, E, W))
        window.rowconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)
        self._listbox = Listbox(window, width=25)
        self._listbox.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E, W))
        self._listbox.bind('<<ListboxSelect>>', lambda e: self._select_manager())
        list_name = [name for name, block in self._manager_list.items()]
        list.sort(list_name)
        for name in list_name:
            self._listbox.insert("end", name)
        self._content = ttk.Frame(window, width=500)
        self._content = VerticalScrolledFrame(window)
        self._content.grid(row=0, column=1, sticky=(N, S, E, W))
        self._content.columnconfigure(0, weight=1)
        self._content.rowconfigure(0, weight=1)
        self._root.bind('<Key-Escape>', lambda e: self._root.destroy())
        # self._root.resizable(False, False)
        self._root.geometry("+100+100")

    def run(self):
        self._root.mainloop()

    def select_file(self):
        filename = filedialog.Open(self._root, filetypes=[('*.ini files', '.ini')]).show()
        if filename == '':
            return
        self._filename.set(filename)

    def load_data(self):
        filename = self._filename.get()
        if not filename:
            return
        config = ConfigParser(interpolation=None)
        config.read(filename, encoding='utf-8')
        for name in self._list:
            manager = self._list[name]
            manager.destroy()
        self._list.clear()
        modulelist = [name for name in iter(self._manager_list)]
        list.sort(modulelist)
        for name in self._manager_list:
            manager = self._manager_list[name](self._content.interior)
            manager.load(config, modulelist)
            self._list[name] = manager

    def save_data(self):
        filename = self._filename.get()
        if not filename:
            return
        config = ConfigParser(interpolation=None)
        list_name = [name for name, block in self._list.items()]
        list.sort(list_name)
        for name in list_name:
            manager = self._list[name]
            manager.save(config)
        with open(filename, 'w', encoding='utf-8') as file:
            config.write(file)

    def _select_manager(self):
        selection = self._listbox.curselection()
        if not selection:
            return
        name = self._listbox.get(selection[0])
        if self._current__name:
            manager = self._list[self._current__name]
            manager.grid_forget()
        if not self._list:
            return
        manager = self._list[name]
        self._current__name = name
        manager.grid(row=0, column=0, sticky=(N, S, E, W))


if __name__ == "__main__":
    App().run()
