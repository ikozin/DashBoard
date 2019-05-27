from typing import Dict, List, Tuple, Optional
from configparser import ConfigParser
from tkinter import messagebox, StringVar, Toplevel, LabelFrame, Label, Entry, Listbox, Button, N, S, E, W
from tkinter.ttk import Frame, Combobox
from ext.base_manager import BaseManager
from ext.modal_dialog import ModalDialog, EntryModalDialog, SelectFrame
from ext.alarm.ui.alarm_setting_ui_file_simple import AlarmSettingUISimple
from ext.alarm.ui.alarm_setting_ui_file_blink import AlarmSettingUIBlink
from ext.alarm.ui.alarm_setting_ui_file_rise import AlarmSettingUIRise
from ext.alarm.alarm_setting_execute import AlarmSettingExecute
from ext.alarm.alarm_setting import AlarmSetting


class AlarmManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(AlarmManager, self).__init__(root, text="Выбор будильника")
        self._mod_list: Dict[str, BaseManager] = dict()
        self.columnconfigure(2, weight=1)
        self._functions = {
            1: AlarmSettingUISimple,
            2: AlarmSettingUIBlink,
            3: AlarmSettingUIRise,
            4: AlarmSettingExecute
        }
        self._alarm_list: Dict[str, AlarmSetting] = dict()
        self._current__name = None
        self._listbox = Listbox(self, width=25)
        self._listbox.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, W))
        self._listbox.bind('<<ListboxSelect>>', self._select_alarm)
        command_frame = Frame(self, padding=(2, 2, 2, 2))
        command_frame.grid(row=0, column=1, sticky=(N, S, W))
        btn = Button(command_frame, text="Создать", command=self._create_alarm)
        btn.grid(row=0, column=0, sticky=(N, S, E, W))
        btn = Button(command_frame, text="Переименовать", command=self._rename_alarm)
        btn.grid(row=1, column=0, sticky=(N, S, E, W))
        btn = Button(command_frame, text="Удалить", command=self._delete_alarm)
        btn.grid(row=2, column=0, sticky=(N, S, E, W))
        self._alarm_frame = Frame(self, padding=(2, 2, 2, 2))
        self._alarm_frame.grid(row=0, column=2, sticky=(N, S, E, W))
        self._frame = SelectFrame(self, "Выбор модулей для отображения во время срабатывания будильника")
        self._frame.grid(row=1, column=0, columnspan=3, sticky=(N, S, E, W), padx=2, pady=2)

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("AlarmBlock"):
            config.add_section("AlarmBlock")
        self._mod_list = module_list
        self._current__name = None
        for schema_name in self._alarm_list:
            block = self._alarm_list[schema_name]
            block.destroy()
        self._alarm_list.clear()
        self._listbox.delete(0, "end")
        section = config["AlarmBlock"]
        selection = [item.strip(" '") for item in section.get("blocklist", fallback="").split(",") if item.strip() in module_list]
        self._frame.load(selection, module_list)
        csv_value = section.get("List", fallback="")
        if csv_value:
            alarm_schemas = [item.strip(" '") for item in csv_value.split(",") if item.strip()]
            alarm_schemas = [str(item) for item in alarm_schemas if config.has_section(item)]
            for item in alarm_schemas:
                section = config[item]
                section_type = section.getint("Type")
                if section_type is None:
                    continue
                alarm_block = self._create_alarm_by_type(section_type, item, list(self._mod_list))
                if alarm_block is None:
                    continue
                alarm_block.load(config, item)
                self._alarm_list[item] = alarm_block
                self._listbox.insert("end", item)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("AlarmBlock"):
            config.add_section("AlarmBlock")
        section = config["AlarmBlock"]

        modules = [x for x in iter(self._alarm_list)]
        for schema_name in modules:
            self._alarm_list[schema_name].pre_save()
        list.sort(modules, key=lambda entry: self._alarm_list[entry]._time)
        section["List"] = ", ".join(modules)
        for schema_name in modules:
            alarm_block = self._alarm_list[schema_name]
            alarm_block.save(config, schema_name)
        section["BlockList"] = self._frame.get_result()

    def _select_alarm(self, event) -> None:
        listbox = event.widget
        selection = listbox.curselection()
        if not selection:
            return
        name = listbox.get(selection[0])

        if self._current__name:
            alarm_block = self._alarm_list[self._current__name]
            alarm_block.grid_forget()
        if not self._alarm_list:
            return
        alarm_block = self._alarm_list[name]
        self._current__name = name
        alarm_block.grid(row=0, column=0, sticky=(N, S, E, W))

    def _create_alarm(self) -> None:
        (item, section_type) = AlarmCreateDialog().execute(self, list(self._functions.keys()))
        if item is None:
            return
        if item in self._alarm_list:
            messagebox.showerror("Ошибка", "Будильник {0} уже существует".format(item))
            return
        alarm_block = self._create_alarm_by_type(section_type, item, list(self._mod_list))
        if alarm_block is not None:
            self._alarm_list[item] = alarm_block
            self._listbox.insert("end", item)

    def _rename_alarm(self) -> None:
        selection = self._listbox.curselection()
        if not selection:
            return
        name = self._listbox.get(selection[0])
        alarm_block = self._alarm_list[name]
        newname = EntryModalDialog("Переименовать").execute(self, name)
        if newname == "":
            return
        if newname in self._alarm_list:
            messagebox.showerror("Ошибка", "Будильник {0} уже существует".format(newname))
            return
        alarm_block.rename(newname)
        del self._alarm_list[name]
        self._alarm_list[newname] = alarm_block
        if self._current__name == name:
            self._current__name = newname
        self._listbox.delete(selection)
        self._listbox.insert(selection, newname)

    def _delete_alarm(self) -> None:
        selection = self._listbox.curselection()
        if not selection:
            return
        name = self._listbox.get(selection[0])
        if messagebox.askquestion("Удалить", "Вы действительно хотите удалить будильник {0}".format(name)) == "no":
            return
        alarm_block = self._alarm_list[name]
        self._listbox.delete(selection)
        del self._alarm_list[name]
        alarm_block.destroy()
        if self._current__name == name:
            self._current__name = None

    def _create_alarm_by_type(self, section_type: int, item: str, mod_list: List[str]) -> Optional[AlarmSetting]:
        func = self._functions.get(section_type, None)
        if func is None:
            return None
        return func(self._alarm_frame, item, mod_list)


class AlarmCreateDialog(ModalDialog):

    def __init__(self):
        self._value_name = None
        self._value_type = None
        self._modal = None
        self._btn_ok = None

    def execute(self, root: AlarmManager, mod_list: List[int]) -> Tuple[str, int]:
        self._modal = Toplevel(root)
        self._modal.title("Создать")
        # self._modal.geometry('+400+400')
        self._value_name = StringVar()
        self._value_type = StringVar()
        self._value_type.set('1')
        lbl = Label(self._modal, text="Имя будильника")
        lbl.grid(row=0, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))
        entry = Entry(self._modal, textvariable=self._value_name)
        entry.grid(row=1, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))
        entry.focus_set()
        # vcmd = (entry.register(self._validateName), '%s', '%P')
        vcmd = (entry.register(self._validate_name), '%P')
        entry.configure(validate="key", validatecommand=vcmd)
        lbl = Label(self._modal, text="Тип будильника")
        lbl.grid(row=2, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))
        combo = Combobox(self._modal, state="readonly", values=mod_list, textvariable=self._value_type)
        combo.grid(row=3, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))
        combo.bind('<<ComboboxSelected>>', lambda e: self._select_type())
        self._btn_ok = Button(self._modal, text="OK", state="disabled", command=self._ok)
        self._btn_ok.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))
        btn = Button(self._modal, text="Cancel", command=self._cancel)
        btn.grid(row=4, column=2, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))
        self._wait_dialog(self._modal, root)
        section_name = self._value_name.get()
        section_type = self._value_type.get()
        section_name = section_name if section_name else None
        section_type = int(section_type) if section_type else None
        return (section_name, section_type)

    def _validate_name(self, new: str) -> bool:
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
            self._btn_ok.configure(state="normal")
        return True

    def _select_type(self) -> None:
        self._btn_ok.configure(state="normal")

    def _ok(self) -> None:
        self._modal.destroy()

    def _cancel(self) -> None:
        self._modal.destroy()
        self._value_name.set("")
        self._value_type.set("")
