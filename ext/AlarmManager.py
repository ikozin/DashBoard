from typing import *

from configparser import ConfigParser
from tkinter import *

from ext.BaseSetting import BaseSetting
from ext.BaseManager import BaseManager
from ext.ModalDialog import ModalDialog
from ext.ModalDialog import EntryModalDialog
from ext.ModalDialog import SelectFrame
from ext.alarm.ui.AlarmSettingUI_Simple import AlarmSettingUI_Simple
from ext.alarm.ui.AlarmSettingUI_Blink import AlarmSettingUI_Blink
from ext.alarm.ui.AlarmSettingUI_Rise import AlarmSettingUI_Rise
from ext.alarm.AlarmSetting_Execute import AlarmSetting_Execute


class AlarmManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(AlarmManager, self).__init__(root, text="Выбор будильника")
        self._modList = None
        self.columnconfigure(2, weight=1)
        self._functions = {
            1: AlarmSettingUI_Simple,
            2: AlarmSettingUI_Blink,
            3: AlarmSettingUI_Rise,
            4: AlarmSetting_Execute
        }
        self._alarmlist = dict()
        self._currentName = None
        self._listBox = Listbox(self, width=25)
        self._listBox.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, W))
        self._listBox.bind('<<ListboxSelect>>', self._selectAlarm)
        commandFrame = ttk.Frame(self, padding=(2, 2, 2, 2))
        commandFrame.grid(row=0, column=1, sticky=(N, S, W))
        btn = Button(commandFrame, text="Создать", command=self._createAlarm)
        btn.grid(row=0, column=0, sticky=(N, S, E, W))
        btn = Button(commandFrame, text="Переименовать", command=self._renameAlarm)
        btn.grid(row=1, column=0, sticky=(N, S, E, W))
        btn = Button(commandFrame, text="Удалить", command=self._deleteAlarm)
        btn.grid(row=2, column=0, sticky=(N, S, E, W))
        self._alarmFrame = ttk.Frame(self, padding=(2, 2, 2, 2))
        self._alarmFrame.grid(row=0, column=2, sticky=(N, S, E, W))
        self._frame = SelectFrame(self, "Выбор модулей для отображения во время срабатывания будильника")
        self._frame.grid(row=1, column=0, columnspan=3, sticky=(N, S, E, W), padx=2, pady=2)

    def load(self, config: ConfigParser, modulelist: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("AlarmBlock"):
            config.add_section("AlarmBlock")
        self._modList = modulelist
        self._currentName = None
        for schemaName in self._alarmlist.keys():
            alarmBlock = self._alarmlist[schemaName]
            alarmBlock.destroy()
        self._alarmlist.clear()
        self._listBox.delete(0, "end")
        section = config["AlarmBlock"]
        selection = section.get("blocklist", "")
        selection = [item.strip(" '") for item in selection.split(",") if item.strip() in modulelist]
        self._frame.load(selection, modulelist)
        csvValue = section.get("List", "")
        if csvValue:
            alarmSchemas = [item.strip(" '") for item in csvValue.split(",") if item.strip()]
            alarmSchemas = [str(item) for item in alarmSchemas if config.has_section(item)]
            for item in alarmSchemas:
                section = config[item]
                type = section.getint("Type")
                if type is None:
                    continue
                alarmBlock = self._createAlarmByType(type, item, self._modList)
                if alarmBlock is None:
                    continue
                alarmBlock.load(config, item)
                self._alarmlist[item] = alarmBlock
                self._listBox.insert("end", item)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("AlarmBlock"):
            config.add_section("AlarmBlock")
        section = config["AlarmBlock"]

        modules = [x for x in iter(self._alarmlist)]
        for schemaName in modules:
            self._alarmlist[schemaName].pre_save()
        list.sort(modules, key=lambda entry: self._alarmlist[entry]._time)
        section["List"] = ", ".join(modules)
        for schemaName in modules:
            alarmBlock = self._alarmlist[schemaName]
            alarmBlock.save(config, schemaName)
        section["BlockList"] = self._frame.getResult()

    def _selectAlarm(self, event) -> None:
        listBox = event.widget
        selection = listBox.curselection()
        if not selection:
            return
        name = listBox.get(selection[0])

        if self._currentName:
            alarmBlock = self._alarmlist[self._currentName]
            alarmBlock.grid_forget()
        if len(self._alarmlist) == 0:
            return
        alarmBlock = self._alarmlist[name]
        self._currentName = name
        alarmBlock.grid(row=0, column=0, sticky=(N, S, E, W))

    def _createAlarm(self) -> None:
        (item, type) = AlarmCreateDialog().Execute(self, list(self._functions.keys()))
        if item is None:
            return
        if item in self._alarmlist:
            messagebox.showerror("Ошибка", "Будильник {0} уже существует".format(item))
            return
        alarmBlock = self._createAlarmByType(type, item, self._modList)
        if alarmBlock is not None:
            self._alarmlist[item] = alarmBlock
            self._listBox.insert("end", item)

    def _renameAlarm(self) -> None:
        selection = self._listBox.curselection()
        if not selection:
            return
        name = self._listBox.get(selection[0])
        alarmBlock = self._alarmlist[name]
        newname = EntryModalDialog("Переименовать").Execute(self, name)
        if newname == "":
            return
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

    def _deleteAlarm(self) -> None:
        selection = self._listBox.curselection()
        if not selection:
            return
        name = self._listBox.get(selection[0])
        if messagebox.askquestion("Удалить", "Вы действительно хотите удалить будильник {0}".format(name)) == "no":
            return
        alarmBlock = self._alarmlist[name]
        self._listBox.delete(selection)
        del self._alarmlist[name]
        alarmBlock.destroy()
        if self._currentName == name:
            self._currentName = None

    def _createAlarmByType(self, type: int, item: str, modList: List[str]) -> BaseSetting:
        func = self._functions.get(type, None)
        if func is None:
            return None
        return func(self._alarmFrame, item, modList)


class AlarmCreateDialog(ModalDialog):

    def Execute(self, root: AlarmManager, list: List[int]) -> Tuple[str, str]:
        self._modal = Toplevel(root)
        self._modal.title("Создать")
        # self._modal.geometry('+400+400')
        self._valueName = StringVar()
        self._valueType = StringVar()
        self._valueType.set('1')
        lbl = Label(self._modal, text="Имя будильника")
        lbl.grid(row=0, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))
        entry = Entry(self._modal, textvariable=self._valueName)
        entry.grid(row=1, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))
        entry.focus_set()
        # vcmd = (entry.register(self._validateName), '%s', '%P')
        vcmd = (entry.register(self._validateName), '%P')
        entry.configure(validate="key", validatecommand=vcmd)
        lbl = Label(self._modal, text="Тип будильника")
        lbl.grid(row=2, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))
        combo = ttk.Combobox(self._modal, state="readonly", values=list, textvariable=self._valueType)
        combo.grid(row=3, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))
        combo.bind('<<ComboboxSelected>>', lambda e: self._selectType())
        self._btnOk = Button(self._modal, text="OK", state="disabled", command=self._ok)
        self._btnOk.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))
        btn = Button(self._modal, text="Cancel", command=self._cancel)
        btn.grid(row=4, column=2, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))
        self._waitDialog(self._modal, root)
        name = self._valueName.get()
        type = self._valueType.get()
        name = name if name else None
        type = int(type) if type else None
        return (name, type)

    # def _validateName(self, old, new):
    def _validateName(self, new: str) -> bool:
        if " " in new:
            return False
        if "," in new:
            return False
        if "'" in new:
            return False
        if "(" in new:
            return False
        if ")" in new:
            return False
        if "[" in new:
            return False
        if "]" in new:
            return False
        if '"' in new:
            return False
        if len(new) > 1:
            self._btnOk.configure(state="normal")
        return True

    def _selectType(self) -> None:
        self._btnOk.configure(state="normal")

    def _ok(self) -> None:
        self._modal.destroy()

    def _cancel(self) -> None:
        self._modal.destroy()
        self._valueName.set("")
        self._valueType.set("")
