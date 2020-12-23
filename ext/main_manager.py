from typing import Dict, Tuple
from configparser import ConfigParser
from tkinter import messagebox, BooleanVar, StringVar, LabelFrame, Label, Checkbutton, Spinbox, Listbox, Button, Entry, N, S, E, W, RIGHT
from tkinter.ttk import Frame
from ext.base_manager import BaseManager
from ext.modal_dialog import ColorsChooserFrame, EntryModalDialog, SelectFrame
from ext.main_setting import MainSetting


class MainManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(MainManager, self).__init__(root, text="Основные настройки")
        self.columnconfigure(4, weight=1)
        self._section_list: Dict[str, MainSetting] = dict()
        self._current__name = None
        self._idle_variable = StringVar()
        self._full_screen = BooleanVar()
        self._pir_value = StringVar()
        self._led_value = StringVar()

        var_frame = Frame(self, padding=(2, 2, 2, 2))
        var_frame.grid(row=0, column=0, columnspan=3, sticky=(N, S, E, W))
        Checkbutton(var_frame, text="Полный экран", variable=self._full_screen).grid(row=0, column=0, sticky=(W))
        Label(var_frame, justify=RIGHT, text="PIR Pin").grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))
        Entry(var_frame, textvariable=self._pir_value, width=8).grid(row=0, column=2, padx=2, pady=2, sticky=(N, S, E, W))
        Label(var_frame, justify=RIGHT, text="LED Pin").grid(row=0, column=3, padx=2, pady=2, sticky=(N, S, E, W))
        Entry(var_frame, textvariable=self._led_value, width=8).grid(row=0, column=4, padx=2, pady=2, sticky=(N, S, E, W))

        self._listbox = Listbox(self)
        self._listbox.grid(row=1, column=0, rowspan=3, padx=2, pady=2)
        self._listbox.bind('<<ListboxSelect>>', self._select_section)

        command_frame = Frame(self, padding=(2, 2, 2, 2))
        command_frame.grid(row=1, column=1, rowspan=3, sticky=(N, S, E, W))

        btn = Button(command_frame, text="Создать", command=self._create_section)
        btn.grid(row=0, column=0, sticky=(N, S, E, W))

        btn = Button(command_frame, text="Переименовать", command=self._rename_section)
        btn.grid(row=1, column=0, sticky=(N, S, E, W))

        btn = Button(command_frame, text="Удалить", command=self._delete_section)
        btn.grid(row=2, column=0, sticky=(N, S, E, W))

        idle_frame = LabelFrame(self, text="Время простоя")
        idle_frame.grid(row=1, column=2, sticky=(N, E, W))

        spin = Spinbox(idle_frame, from_=5, to=60, increment=1, width=3, textvariable=self._idle_variable)
        spin.grid(row=0, column=0, padx=2, pady=2)

        lbl = Label(idle_frame, text="минут")
        lbl.grid(row=0, column=2, pady=2)

        self._color_frame = ColorsChooserFrame(self, "Цвет")
        self._color_frame.grid(row=1, column=3, sticky=(N, E, W))

        self._section_frame = LabelFrame(self)
        self._section_frame.grid(row=2, column=2, rowspan=2, columnspan=3, sticky=(N, S, E, W))

        self._frame = SelectFrame(self, "Выбор модулей для загрузки")
        self._frame.grid(row=4, column=0, columnspan=4, sticky=(N, S, E, W), padx=2, pady=2)

    def load(self, config: ConfigParser, module_list: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("MAIN"):
            config.add_section("MAIN")
        if not config.has_section("TIMELINE"):
            config.add_section("TIMELINE")
        self._current__name = None
        for section_name in self._section_list:
            section_block = self._section_list[section_name]
            section_block.destroy()
        self._section_list.clear()
        self._listbox.delete(0, "end")
        section = config["MAIN"]
        self._full_screen.set(section.getboolean("FullScreen", fallback=False))
        self._pir_value.set(section.get("PIR", fallback=""))
        self._led_value.set(section.get("LED", fallback=""))
        idle = section.getint("idletime", fallback=1)
        self._idle_variable.set(idle)
        back_color = self._get_tuple(section.get("BackgroundColor", fallback="(0, 0, 0)"))
        fore_color = self._get_tuple(section.get("ForegroundColor", fallback="(255, 255, 255)"))
        self._color_frame.load(back_color, fore_color)
        selection = [item.strip(" '") for item in section.get("BlockList", fallback="").split(",")
                     if item.strip() in module_list]
        self._frame.load(selection, module_list)
        section = config["TIMELINE"]
        csv_value = section.get("sections")
        if csv_value:
            section_schemas = [item.strip(" '") for item in csv_value.split(",") if item.strip()]
            section_schemas = [str(item) for item in section_schemas if config.has_section(item)]
            for item in section_schemas:
                section = config[item]
                section_block = MainSetting(self._section_frame, item)
                section_block.load(config, item)
                self._section_list[item] = section_block
                self._listbox.insert("end", item)

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("MAIN"):
            config.add_section("MAIN")
        if not config.has_section("TIMELINE"):
            config.add_section("TIMELINE")
        section = config["MAIN"]
        section["FullScreen"] = str(self._full_screen.get())
        section["PIR"] = self._pir_value.get()
        section["LED"] = self._led_value.get()
        (background_color, foreground_color) = self._color_frame.get_result()
        section["idletime"] = str(self._idle_variable.get())
        section["BackgroundColor"] = "(%d, %d, %d)" % background_color
        section["ForegroundColor"] = "(%d, %d, %d)" % foreground_color
        section["BlockList"] = self._frame.get_result()

        section = config["TIMELINE"]

        parts = [name for name in iter(self._section_list)]
        for schema_name in parts:
            self._section_list[schema_name].pre_save()
        list.sort(parts, key=lambda entry: self._section_list[entry]._time)
        section["sections"] = ", ".join(parts)
        for section_name in parts:
            section_block = self._section_list[section_name]
            section_block.save(config, section_name)

    def _select_section(self, event) -> None:
        listbox = event.widget
        selection = listbox.curselection()
        if not selection:
            return
        name = listbox.get(selection[0])
        if self._current__name:
            section_block = self._section_list[self._current__name]
            section_block.grid_forget()
        if not self._section_list:
            return
        section_block = self._section_list[name]
        self._current__name = name
        section_block.grid(row=0, column=0, sticky=(N, S, E, W))

    def _create_section(self) -> None:
        item = EntryModalDialog("Создать").execute(self, "")
        if item == "":
            return
        if item in self._section_list:
            messagebox.showerror("Ошибка", "Расписание {0} уже существует".format(item))
            return
        section_block = MainSetting(self._section_frame, item)
        self._section_list[item] = section_block
        self._listbox.insert("end", item)

    def _rename_section(self) -> None:
        selection = self._listbox.curselection()
        if not selection:
            return
        name = self._listbox.get(selection[0])
        section_block = self._section_list[name]
        newname = EntryModalDialog("Переименовать").execute(self, name)
        if newname == "":
            return
        if newname in self._section_list:
            messagebox.showerror("Ошибка", "Расписание {0} уже существует".format(newname))
            return
        section_block.rename(newname)
        del self._section_list[name]
        self._section_list[newname] = section_block
        if self._current__name == name:
            self._current__name = newname
        self._listbox.delete(selection)
        self._listbox.insert(selection, newname)

    def _delete_section(self) -> None:
        selection = self._listbox.curselection()
        if not selection:
            return
        name = self._listbox.get(selection[0])
        if messagebox.askquestion("Удалить", "Вы действительно хотите удалить расписание {0}".format(name)) == "no":
            return
        section_block = self._section_list[name]
        self._listbox.delete(selection)
        del self._section_list[name]
        section_block.destroy()
        if self._current__name == name:
            self._current__name = None

    def _get_tuple(self, value: str) -> Tuple[int, ...]:
        """  Конвертирует строку '0, 0, 0' в кортеж (0, 0, 0) """
        return tuple(int(item.strip("([ '])")) for item in value.split(",") if item.strip())
