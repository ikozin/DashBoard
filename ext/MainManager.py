import datetime
import configparser

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

from ext.ModalDialog import ColorsChooserFrame
from ext.ModalDialog import EntryModalDialog
from ext.MainSetting import MainSetting

class MainManager(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root):
        """ """
        super(MainManager, self).__init__(root, text="Основные настройки")
        self.columnconfigure(4, weight=1)
        self._sectionlist = dict()
        self._currentName = None
        self._idleVariable = StringVar()
        self._listBox = Listbox(self)
        self._listBox.grid(row=0, column=0, rowspan=3, padx=2, pady=2)
        self._listBox.bind('<<ListboxSelect>>', lambda e: self._selectSection())
        commandFrame = ttk.Frame(self, padding=(2,2,2,2))
        commandFrame.grid(row=0, column=1, rowspan=3, sticky=(N,S,E,W))
        ttk.Button(commandFrame, text="Создать", command=self._createSection).grid(row=0, column=0, sticky=(N,S,E,W))
        ttk.Button(commandFrame, text="Переименовать", command=self._renameSection).grid(row=1, column=0, sticky=(N,S,E,W))
        ttk.Button(commandFrame, text="Удалить", command=self._deleteSection).grid(row=2, column=0, sticky=(N,S,E,W))
        idleFrame = ttk.LabelFrame(self, text="Время простоя")
        idleFrame.grid(row=0, column=2, sticky=(N,E,W))
        Spinbox(idleFrame, from_=5, to=60, increment=1, width=3, textvariable=self._idleVariable).grid(row=0, column=0, padx=2, pady=2)
        ttk.Label(idleFrame, text="минут").grid(row=0, column=2, pady=2)
        self._colorFrame = ColorsChooserFrame(self, "Цвет")
        self._colorFrame.grid(row=0, column=3, sticky=(N,E,W))
        self._setcionFrame = ttk.Frame(self, padding=(2,2,2,2))
        self._setcionFrame.grid(row=1, column=2, rowspan=2, columnspan=3,  sticky=(N,S,E,W))

    def load(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        self._currentName = None
        for sectionName in self._sectionlist.keys():
            sectionBlock = self._sectionlist[sectionName]
            sectionBlock.destroy()
        self._sectionlist.clear()
        self._listBox.delete(0, "end")
        section = config["MAIN"]
        idle = section.getint("idletime", 1)
        self._idleVariable.set(idle)
        backColor = self._getTuple(section.get("backgroundcolor", "(0, 0, 0)"))
        foreColor = self._getTuple(section.get("foregroundcolor", "(255, 255, 255)"))
        self._colorFrame.load(backColor, foreColor)
        section = config["TIMELINE"]
        csvValue = section.get("sections")
        if csvValue:
            sectionSchemas = [item.strip(" '") for item in csvValue.split(",") if item.strip()]
            sectionSchemas = [str(item) for item in sectionSchemas if config.has_section(item)]
            for item in sectionSchemas:
                section = config[item]
                sectionBlock = MainSetting(self._setcionFrame, item)
                sectionBlock.load(config, item)
                self._sectionlist[item] = sectionBlock
                self._listBox.insert("end", item)

    def save(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("MAIN"):      config.add_section("MAIN")
        if not config.has_section("TIMELINE"):  config.add_section("TIMELINE")
        section = config["MAIN"]
        (backgroundColor, foregroundColor) = self._colorFrame.getResult()
        section["idletime"] = str(self._idleVariable.get())
        section["backgroundcolor"] = "(%d, %d, %d)" % backgroundColor
        section["foregroundcolor"] = "(%d, %d, %d)" % foregroundColor
        section = config["TIMELINE"]
        section["sections"] = ", ".join(self._sectionlist)
        for sectionName in self._sectionlist.keys():
            sectionBlock = self._sectionlist[sectionName]
            sectionBlock.save(config, sectionName)

    def _selectSection(self):
        selection = self._listBox.curselection() 
        if not selection: return
        name = self._listBox.get(selection[0])
        if self._currentName:
            sectionBlock = self._sectionlist[self._currentName]
            sectionBlock.grid_forget()
        sectionBlock = self._sectionlist[name]
        self._currentName = name
        sectionBlock.grid(row=0, column=0, sticky=NSEW)

    def _createSection(self):
        item = EntryModalDialog("Создать").Execute(self, "")
        if item == "": return
        if item in self._sectionlist:
            messagebox.showerror("Ошибка", "Расписание {0} уже существует".format(item))
            return
        sectionBlock = MainSetting(self._setcionFrame, item)
        self._sectionlist[item] = sectionBlock
        self._listBox.insert("end", item)

    def _renameSection(self):
        selection = self._listBox.curselection() 
        if not selection: return
        name = self._listBox.get(selection[0])
        sectionBlock = self._sectionlist[name]
        newname = EntryModalDialog("Переименовать").Execute(self, name)
        if newname == "": return
        if newname in self._sectionlist:
            messagebox.showerror("Ошибка", "Расписание {0} уже существует".format(newname))
            return
        sectionBlock.rename(newname)
        del self._sectionlist[name]
        self._sectionlist[newname] = sectionBlock
        if self._currentName == name:
            self._currentName = newname
        self._listBox.delete(selection) 
        self._listBox.insert(selection, newname)

    def _deleteSection(self):
        selection = self._listBox.curselection() 
        if not selection: return
        name = self._listBox.get(selection[0])
        if messagebox.askquestion("Удалить", "Вы действительно хотите удалить расписание {0}".format(name)) == "no":
            return
        sectionBlock = self._sectionlist[name]
        self._listBox.delete(selection) 
        del self._sectionlist[name]
        sectionBlock.destroy()
        if self._currentName == name:
            self._currentName = None

    def _getTuple(self, value):
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        try:
            return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
        except Exception as ex:
            return None
