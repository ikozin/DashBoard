#!/usr/bin/python3
# feedback_solution.py by Barron Stone
# This is an exercise file from Python GUI Development with Tkinter on lynda.com

import datetime
import configparser
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from ext.MainManager import MainManager
from ext.TimeManager import TimeManager
from ext.AlarmManager import AlarmManager
from ext.VoiceManager import VoiceManager
from ext.YandexNewsManager import YandexNewsManager
from ext.CalendarManager import CalendarManager
from ext.OpenWeatherMapManager import OpenWeatherMapManager

class App(object):
    """description of class"""
    def __init__(self):
        self._managerList = { "MainManager": MainManager, "TimeManager": TimeManager, "AlarmManager": AlarmManager, "VoiceManager": VoiceManager, "YandexNewsManager": YandexNewsManager, "OpenWeatherMapManager": OpenWeatherMapManager, "CalendarManager": CalendarManager}
        self._list = dict()
        self._currentName = None
        self._root = Tk()
        self._root.title('DashBoard Tool')
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)
        
        self._fileName = StringVar()

        self._window = ttk.Frame(self._root)
        self._window.grid(row=0, column=0, sticky=(N,S,E,W))
        self._window.rowconfigure(1, weight=1)
        self._window.columnconfigure(1, weight=1)

        header = ttk.LabelFrame(self._window, text="Configuration", width=300, height=100)
        header.grid(row=0, column=0, columnspan=2, sticky=(N,S,E,W))
        header.columnconfigure(4, weight=1)
        ttk.Entry(header, width=24, textvariable=self._fileName).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(header, text="...", command=self.selectFile).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(header, text= "Load", command=self.loadData).grid(row=0, column=2, padx=2, pady=2)
        ttk.Button(header, text= "Save", command=self.saveData).grid(row=0, column=3, padx=2, pady=2)
        self._listBox = Listbox(self._window, width=25)
        self._listBox.grid(row=1, column=0, padx=2, pady=2, sticky=(N,S,W))
        self._listBox.bind('<<ListboxSelect>>', lambda e: self._selectManager())
        for item in self._managerList.keys():
            self._listBox.insert("end", item)
        self._content = Frame(self._window, bg="blue", width=500)
        self._content.grid(row=1, column=1, sticky=(N,S,E,W))

        #self._text = Text(self._window, wrap=NONE)
        #self._text.grid(row=99, column=0, columnspan=2, sticky=(N,S,E,W))

        self._root.bind('<Key-Escape>', lambda e: self._root.destroy())
        #self._root.resizable(False, False)
        self._root.geometry("+100+100")

    
    def run(self):
        self._root.mainloop()


    def selectFile(self): 
        fileName = filedialog. Open(self._root, filetypes = [('*.ini files', '.ini')]).show()
        if fileName == '': return
        self._fileName.set(fileName)


    def loadData(self): 
        fileName = self._fileName.get()
        if not fileName: return
        config = configparser.ConfigParser()
        config.read(fileName, encoding="utf-8")
        
        #self._text.delete('1.0', 'end') 
        #self._text.insert('1.0', open(fileName, 'rt').read())

        for name in self._list.keys():
            manager = self._list[name]
            manager.destroy()
        self._list.clear()

        for name in self._managerList.keys():
            manager = self._managerList[name](self._content)
            manager.load(config)
            self._list[name] = manager

    def saveData(self): 
        fileName = self._fileName.get()
        if not fileName: return
        config = configparser.ConfigParser()
        for item in self._list:
            item.save(config)
        with open('new_setting.ini', 'w') as fp:
            config.write(fp)

        self._text.delete('1.0', 'end') 
        self._text.insert('1.0', open(fileName, 'rt').read())

    def _selectManager(self):
        selection = self._listBox.curselection() 
        if not selection: return
        name = self._listBox.get(selection[0])

        if self._currentName:
            manager = self._list[self._currentName]
            manager.grid_forget()
        manager = self._list[name]
        self._currentName = name
        manager.grid(row=0, column=0, sticky=(N,S,E,W))

def main():            
    App().run()
    
if __name__ == "__main__":
    main()
