import datetime
import configparser

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

from ext.ModalDialog import ModalDialog
from ext.ModalDialog import EntryModalDialog
from ext.AlarmSetting import AlarmSimpleSetting
from ext.AlarmSetting import AlarmBlinkSetting
from ext.AlarmSetting import AlarmRiseSetting

class AlarmCreateDialog(ModalDialog):

    def Execute(self, root):
        self._modal = Toplevel(root)
        self._modal.title("Создать")
        #self._modal.geometry('+400+400')
        self._valueName = StringVar()
        self._valueType = StringVar()
        self._valueType.set('1')
        ttk.Label(self._modal, text="Имя будильника").grid(row=0, column=0, columnspan=4, padx=2, pady=2, sticky=(N,S,E,W))
        entry = ttk.Entry(self._modal, textvariable=self._valueName)
        entry.grid(row=1, column=0, columnspan=4, padx=2, pady=2, sticky=(N,S,E,W))
        entry.focus_set()
        #vcmd = (entry.register(self._validateName), '%s', '%P')
        vcmd = (entry.register(self._validateName), '%P')
        entry.configure(validate="key", validatecommand=vcmd)
        ttk.Label(self._modal, text="Тип будильника").grid(row=2, column=0, columnspan=4, padx=2, pady=2, sticky=(N,S,E,W))
        combo = ttk.Combobox(self._modal, state="readonly", values=('1','2','3'), textvariable=self._valueType)
        combo.grid(row=3, column=0, columnspan=4, padx=2, pady=2, sticky=(N,S,E,W))
        combo.bind('<<ComboboxSelected>>', lambda e: self._selectType())
        self._btnOk = ttk.Button(self._modal, text="OK", state="disabled", command=self._ok)
        self._btnOk.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=(N,S,E,W))
        ttk.Button(self._modal, text="Cancel", command=self._cancel).grid(row=4, column=2, columnspan=2, padx=2, pady=2, sticky=(N,S,E,W))
        self._waitDialog(self._modal, root)        
        name = self._valueName.get()
        type = self._valueType.get()
        name = name if name else None
        type = int(type) if type else None
        return (name, type)

    #def _validateName(self, old, new):
    def _validateName(self, new):
        if " " in new : return False
        if "," in new : return False
        if "'" in new : return False
        if "(" in new : return False
        if ")" in new : return False
        if "[" in new : return False
        if "]" in new : return False
        if '"' in new : return False
        if len(new) > 1: self._btnOk.configure(state="normal")
        return True

    def _selectType(self):
        self._btnOk.configure(state="normal")
        pass

    def _ok(self):
        self._modal.destroy()

    def _cancel(self):
        self._modal.destroy()
        self._valueName.set("")
        self._valueType.set("")


class AlarmManager(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root):
        """ """
        super(AlarmManager, self).__init__(root, text="Выбор будильника")
        self.columnconfigure(2, weight=1)
        self._functions = {1: AlarmSimpleSetting, 2: AlarmBlinkSetting, 3: AlarmRiseSetting}
        self._alarmlist = dict()
        self._currentName = None
        self._listBox = Listbox(self, width=25)
        self._listBox.grid(row=0, column=0, padx=2, pady=2, sticky=(N,S,W))
        self._listBox.bind('<<ListboxSelect>>', self._selectAlarm)
        commandFrame = ttk.Frame(self, padding=(2,2,2,2))
        commandFrame.grid(row=0, column=1, sticky=(N,S,W))
        ttk.Button(commandFrame, text="Создать", command=self._createAlarm).grid(row=0, column=0, sticky=(N,S,E,W))
        ttk.Button(commandFrame, text="Переименовать", command=self._renameAlarm).grid(row=1, column=0, sticky=(N,S,E,W))
        ttk.Button(commandFrame, text="Удалить", command=self._deleteAlarm).grid(row=2, column=0, sticky=(N,S,E,W))
        self._alarmFrame = ttk.Frame(self, padding=(2,2,2,2))
        self._alarmFrame.grid(row=0, column=2, sticky=(N,S,E,W))


    def load(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("AlarmBlock"): config.add_section("AlarmBlock")

        self._currentName = None
        for schemaName in self._alarmlist.keys():
            alarmBlock = self._alarmlist[schemaName]
            alarmBlock.destroy()
        self._alarmlist.clear()
        self._listBox.delete(0, "end")
        section = config["AlarmBlock"]
        csvValue = section.get("List", "")
        if csvValue:
            alarmSchemas = [item.strip(" '") for item in csvValue.split(",") if item.strip()]
            alarmSchemas = [str(item) for item in alarmSchemas if config.has_section(item)]
            for item in alarmSchemas:
                section = config[item]
                type = section.getint("Type")
                if type is None: continue
                alarmBlock = self._createAlarmByType(type, item)
                if alarmBlock is None: continue
                alarmBlock.load(config, item)
                self._alarmlist[item] = alarmBlock
                self._listBox.insert("end", item)


    def save(self, config):
        if not isinstance(config, configparser.ConfigParser): raise TypeError("config")
        if not config.has_section("AlarmBlock"): config.add_section("AlarmBlock")
        section = config["AlarmBlock"]
        section["List"] = ", ".join(self._alarmlist.keys())
        for schemaName in self._alarmlist.keys():
            alarmBlock = self._alarmlist[schemaName]
            alarmBlock.save(config, schemaName)


    def _selectAlarm(self, event):
        listBox = event.widget
        selection = listBox.curselection() 
        if not selection: return
        name = listBox.get(selection[0])

        if self._currentName:
            alarmBlock = self._alarmlist[self._currentName]
            alarmBlock.grid_forget()
        if len(self._alarmlist) == 0: return
        alarmBlock = self._alarmlist[name]
        self._currentName = name
        alarmBlock.grid(row=0, column=0, sticky=(N,S,E,W))


    def _createAlarm(self):
        (item, type) = AlarmCreateDialog().Execute(self)
        if item is None: return
        if item in self._alarmlist:
            messagebox.showerror("Ошибка", "Будильник {0} уже существует".format(item))
            return
        alarmBlock = self._createAlarmByType(type, item)
        if not alarmBlock is None:
            self._alarmlist[item] = alarmBlock
            self._listBox.insert("end", item)


    def _renameAlarm(self):
        selection = self._listBox.curselection() 
        if not selection: return
        name = self._listBox.get(selection[0])
        alarmBlock = self._alarmlist[name]
        newname = EntryModalDialog("Переименовать").Execute(self, name)
        if newname == "": return
        if newname in self._alarmlist:
            messagebox.showerror("Ошибка", "Будильник {0} уже существует".format(newname))
            return
        alarmBlock.rename(newname)
        del self._alarmlist[name]
        self._alarmlist[newname] = alarmBlock
        if self._currentName == name:
            self._currentName = newname
        self._listBox.delete(selection) 
        self._listBox.insert(selection, newname)


    def _deleteAlarm(self):
        selection = self._listBox.curselection() 
        if not selection: return
        name = self._listBox.get(selection[0])
        if messagebox.askquestion("Удалить", "Вы действительно хотите удалить будильник {0}".format(name)) == "no":
            return
        alarmBlock = self._alarmlist[name]
        self._listBox.delete(selection) 
        del self._alarmlist[name]
        alarmBlock.destroy()
        if self._currentName == name:
            self._currentName = None


    def _createAlarmByType(self, type, item):
        func = self._functions.get(type, None)
        if func is None: return None
        return func(self._alarmFrame, item)
