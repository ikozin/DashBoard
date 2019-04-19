from typing import *

from configparser import ConfigParser
from tkinter import *

from ext.BaseManager import BaseManager
from ext.ModalDialog import ModalDialog

KEY_CODE_LIST = (
'KEY_0',
'KEY_1',
'KEY_102ND',
'KEY_10CHANNELSDOWN',
'KEY_10CHANNELSUP',
'KEY_2',
'KEY_3',
'KEY_4',
'KEY_5',
'KEY_6',
'KEY_7',
'KEY_8',
'KEY_9',
'KEY_A',
'KEY_AB',
'KEY_ADDRESSBOOK',
'KEY_AGAIN',
'KEY_ALS_TOGGLE',
'KEY_ALTERASE',
'KEY_ANGLE',
'KEY_APOSTROPHE',
'KEY_APPSELECT',
'KEY_ARCHIVE',
'KEY_ATTENDANT_OFF',
'KEY_ATTENDANT_ON',
'KEY_ATTENDANT_TOGGLE',
'KEY_AUDIO',
'KEY_AUX',
'KEY_B',
'KEY_BACK',
'KEY_BACKSLASH',
'KEY_BACKSPACE',
'KEY_BASSBOOST',
'KEY_BATTERY',
'KEY_BLUE',
'KEY_BLUETOOTH',
'KEY_BOOKMARKS',
'KEY_BREAK',
'KEY_BRIGHTNESSDOWN',
'KEY_BRIGHTNESSUP',
'KEY_BRIGHTNESS_AUTO',
'KEY_BRIGHTNESS_CYCLE',
'KEY_BRIGHTNESS_MAX',
'KEY_BRIGHTNESS_MIN',
'KEY_BRL_DOT1',
'KEY_BRL_DOT10',
'KEY_BRL_DOT2',
'KEY_BRL_DOT3',
'KEY_BRL_DOT4',
'KEY_BRL_DOT5',
'KEY_BRL_DOT6',
'KEY_BRL_DOT7',
'KEY_BRL_DOT8',
'KEY_BRL_DOT9',
'KEY_BUTTONCONFIG',
'KEY_C',
'KEY_CALC',
'KEY_CALENDAR',
'KEY_CAMERA',
'KEY_CAMERA_DOWN',
'KEY_CAMERA_FOCUS',
'KEY_CAMERA_LEFT',
'KEY_CAMERA_RIGHT',
'KEY_CAMERA_UP',
'KEY_CAMERA_ZOOMIN',
'KEY_CAMERA_ZOOMOUT',
'KEY_CANCEL',
'KEY_CAPSLOCK',
'KEY_CD',
'KEY_CHANNEL',
'KEY_CHANNELDOWN',
'KEY_CHANNELUP',
'KEY_CHAT',
'KEY_CLEAR',
'KEY_CLOSE',
'KEY_CLOSECD',
'KEY_COFFEE',
'KEY_COMMA',
'KEY_COMPOSE',
'KEY_COMPUTER',
'KEY_CONFIG',
'KEY_CONNECT',
'KEY_CONTEXT_MENU',
'KEY_CONTROLPANEL',
'KEY_COPY',
'KEY_CUT',
'KEY_CYCLEWINDOWS',
'KEY_D',
'KEY_DASHBOARD',
'KEY_DATABASE',
'KEY_DELETE',
'KEY_DELETEFILE',
'KEY_DEL_EOL',
'KEY_DEL_EOS',
'KEY_DEL_LINE',
'KEY_DIGITS',
'KEY_DIRECTION',
'KEY_DIRECTORY',
'KEY_DISPLAYTOGGLE',
'KEY_DISPLAY_OFF',
'KEY_DOCUMENTS',
'KEY_DOLLAR',
'KEY_DOT',
'KEY_DOWN',
'KEY_DVD',
'KEY_E',
'KEY_EDIT',
'KEY_EDITOR',
'KEY_EJECTCD',
'KEY_EJECTCLOSECD',
'KEY_EMAIL',
'KEY_END',
'KEY_ENTER',
'KEY_EPG',
'KEY_EQUAL',
'KEY_ESC',
'KEY_EURO',
'KEY_EXIT',
'KEY_F',
'KEY_F1',
'KEY_F10',
'KEY_F11',
'KEY_F12',
'KEY_F13',
'KEY_F14',
'KEY_F15',
'KEY_F16',
'KEY_F17',
'KEY_F18',
'KEY_F19',
'KEY_F2',
'KEY_F20',
'KEY_F21',
'KEY_F22',
'KEY_F23',
'KEY_F24',
'KEY_F3',
'KEY_F4',
'KEY_F5',
'KEY_F6',
'KEY_F7',
'KEY_F8',
'KEY_F9',
'KEY_FASTFORWARD',
'KEY_FAVORITES',
'KEY_FILE',
'KEY_FINANCE',
'KEY_FIND',
'KEY_FIRST',
'KEY_FN',
'KEY_FN_1',
'KEY_FN_2',
'KEY_FN_B',
'KEY_FN_D',
'KEY_FN_E',
'KEY_FN_ESC',
'KEY_FN_F',
'KEY_FN_F1',
'KEY_FN_F10',
'KEY_FN_F11',
'KEY_FN_F12',
'KEY_FN_F2',
'KEY_FN_F3',
'KEY_FN_F4',
'KEY_FN_F5',
'KEY_FN_F6',
'KEY_FN_F7',
'KEY_FN_F8',
'KEY_FN_F9',
'KEY_FN_S',
'KEY_FORWARD',
'KEY_FORWARDMAIL',
'KEY_FRAMEBACK',
'KEY_FRAMEFORWARD',
'KEY_FRONT',
'KEY_G',
'KEY_GAMES',
'KEY_GOTO',
'KEY_GRAPHICSEDITOR',
'KEY_GRAVE',
'KEY_GREEN',
'KEY_H',
'KEY_HANGEUL',
'KEY_HANJA',
'KEY_HELP',
'KEY_HENKAN',
'KEY_HIRAGANA',
'KEY_HOME',
'KEY_HOMEPAGE',
'KEY_HP',
'KEY_I',
'KEY_IMAGES',
'KEY_INFO',
'KEY_INSERT',
'KEY_INS_LINE',
'KEY_ISO',
'KEY_J',
'KEY_JOURNAL',
'KEY_K',
'KEY_KATAKANA',
'KEY_KATAKANAHIRAGANA',
'KEY_KBDILLUMDOWN',
'KEY_KBDILLUMTOGGLE',
'KEY_KBDILLUMUP',
'KEY_KBDINPUTASSIST_ACCEPT',
'KEY_KBDINPUTASSIST_CANCEL',
'KEY_KBDINPUTASSIST_NEXT',
'KEY_KBDINPUTASSIST_NEXTGROUP',
'KEY_KBDINPUTASSIST_PREV',
'KEY_KBDINPUTASSIST_PREVGROUP',
'KEY_KEYBOARD',
'KEY_KP0',
'KEY_KP1',
'KEY_KP2',
'KEY_KP3',
'KEY_KP4',
'KEY_KP5',
'KEY_KP6',
'KEY_KP7',
'KEY_KP8',
'KEY_KP9',
'KEY_KPASTERISK',
'KEY_KPCOMMA',
'KEY_KPDOT',
'KEY_KPENTER',
'KEY_KPEQUAL',
'KEY_KPJPCOMMA',
'KEY_KPLEFTPAREN',
'KEY_KPMINUS',
'KEY_KPPLUS',
'KEY_KPPLUSMINUS',
'KEY_KPRIGHTPAREN',
'KEY_KPSLASH',
'KEY_L',
'KEY_LANGUAGE',
'KEY_LAST',
'KEY_LEFT',
'KEY_LEFTALT',
'KEY_LEFTBRACE',
'KEY_LEFTCTRL',
'KEY_LEFTMETA',
'KEY_LEFTSHIFT',
'KEY_LIGHTS_TOGGLE',
'KEY_LINEFEED',
'KEY_LIST',
'KEY_LOGOFF',
'KEY_M',
'KEY_MACRO',
'KEY_MAIL',
'KEY_MAX',
'KEY_MEDIA',
'KEY_MEDIA_REPEAT',
'KEY_MEMO',
'KEY_MENU',
'KEY_MESSENGER',
'KEY_MHP',
'KEY_MICMUTE',
'KEY_MINUS',
'KEY_MODE',
'KEY_MOVE',
'KEY_MP3',
'KEY_MSDOS',
'KEY_MUHENKAN',
'KEY_MUTE',
'KEY_N',
'KEY_NEW',
'KEY_NEWS',
'KEY_NEXT',
'KEY_NEXTSONG',
'KEY_NUMERIC_0',
'KEY_NUMERIC_1',
'KEY_NUMERIC_2',
'KEY_NUMERIC_3',
'KEY_NUMERIC_4',
'KEY_NUMERIC_5',
'KEY_NUMERIC_6',
'KEY_NUMERIC_7',
'KEY_NUMERIC_8',
'KEY_NUMERIC_9',
'KEY_NUMERIC_POUND',
'KEY_NUMERIC_STAR',
'KEY_NUMLOCK',
'KEY_O',
'KEY_OK',
'KEY_OPEN',
'KEY_OPTION',
'KEY_P',
'KEY_PAGEDOWN',
'KEY_PAGEUP',
'KEY_PASTE',
'KEY_PAUSE',
'KEY_PAUSECD',
'KEY_PC',
'KEY_PHONE',
'KEY_PLAY',
'KEY_PLAYCD',
'KEY_PLAYER',
'KEY_PLAYPAUSE',
'KEY_POWER',
'KEY_POWER2',
'KEY_PRESENTATION',
'KEY_PREVIOUS',
'KEY_PREVIOUSSONG',
'KEY_PRINT',
'KEY_PROG1',
'KEY_PROG2',
'KEY_PROG3',
'KEY_PROG4',
'KEY_PROGRAM',
'KEY_PROPS',
'KEY_PVR',
'KEY_Q',
'KEY_QUESTION',
'KEY_R',
'KEY_RADIO',
'KEY_RECORD',
'KEY_RED',
'KEY_REDO',
'KEY_REFRESH',
'KEY_REPLY',
'KEY_RESERVED',
'KEY_RESTART',
'KEY_REWIND',
'KEY_RFKILL',
'KEY_RIGHT',
'KEY_RIGHTALT',
'KEY_RIGHTBRACE',
'KEY_RIGHTCTRL',
'KEY_RIGHTMETA',
'KEY_RIGHTSHIFT',
'KEY_RO',
'KEY_S',
'KEY_SAT',
'KEY_SAT2',
'KEY_SAVE',
'KEY_SCALE',
'KEY_SCREEN',
'KEY_SCREENSAVER',
'KEY_SCROLLDOWN',
'KEY_SCROLLLOCK',
'KEY_SCROLLUP',
'KEY_SEARCH',
'KEY_SELECT',
'KEY_SEMICOLON',
'KEY_SEND',
'KEY_SENDFILE',
'KEY_SETUP',
'KEY_SHOP',
'KEY_SHUFFLE',
'KEY_SLASH',
'KEY_SLEEP',
'KEY_SLOW',
'KEY_SOUND',
'KEY_SPACE',
'KEY_SPELLCHECK',
'KEY_SPORT',
'KEY_SPREADSHEET',
'KEY_STOP',
'KEY_STOPCD',
'KEY_SUBTITLE',
'KEY_SUSPEND',
'KEY_SWITCHVIDEOMODE',
'KEY_SYSRQ',
'KEY_T',
'KEY_TAB',
'KEY_TAPE',
'KEY_TASKMANAGER',
'KEY_TEEN',
'KEY_TEXT',
'KEY_TIME',
'KEY_TITLE',
'KEY_TOUCHPAD_OFF',
'KEY_TOUCHPAD_ON',
'KEY_TOUCHPAD_TOGGLE',
'KEY_TUNER',
'KEY_TV',
'KEY_TV2',
'KEY_TWEN',
'KEY_U',
'KEY_UNDO',
'KEY_UNKNOWN',
'KEY_UP',
'KEY_UWB',
'KEY_V',
'KEY_VCR',
'KEY_VCR2',
'KEY_VENDOR',
'KEY_VIDEO',
'KEY_VIDEOPHONE',
'KEY_VIDEO_NEXT',
'KEY_VIDEO_PREV',
'KEY_VOICECOMMAND',
'KEY_VOICEMAIL',
'KEY_VOLUMEDOWN',
'KEY_VOLUMEUP',
'KEY_W',
'KEY_WAKEUP',
'KEY_WLAN',
'KEY_WORDPROCESSOR',
'KEY_WPS_BUTTON',
'KEY_WWAN',
'KEY_WWW',
'KEY_X',
'KEY_XFER',
'KEY_Y',
'KEY_YELLOW',
'KEY_YEN',
'KEY_Z',
'KEY_ZENKAKUHANKAKU',
'KEY_ZOOM',
'KEY_ZOOMIN',
'KEY_ZOOMOUT',
'KEY_ZOOMRESET',
'BTN_0',
'BTN_1',
'BTN_2',
'BTN_3',
'BTN_4',
'BTN_5',
'BTN_6',
'BTN_7',
'BTN_8',
'BTN_9',
'BTN_BACK',
'BTN_BASE',
'BTN_BASE2',
'BTN_BASE3',
'BTN_BASE4',
'BTN_BASE5',
'BTN_BASE6',
'BTN_C',
'BTN_DEAD',
'BTN_DIGI',
'BTN_DPAD_DOWN',
'BTN_DPAD_LEFT',
'BTN_DPAD_RIGHT',
'BTN_DPAD_UP',
'BTN_EAST',
'BTN_EXTRA',
'BTN_FORWARD',
'BTN_GAMEPAD',
'BTN_GEAR_DOWN',
'BTN_GEAR_UP',
'BTN_JOYSTICK',
'BTN_LEFT',
'BTN_MIDDLE',
'BTN_MISC',
'BTN_MODE',
'BTN_MOUSE',
'BTN_NORTH',
'BTN_PINKIE',
'BTN_RIGHT',
'BTN_SELECT',
'BTN_SIDE',
'BTN_SOUTH',
'BTN_START',
'BTN_STYLUS',
'BTN_STYLUS2',
'BTN_TASK',
'BTN_THUMB',
'BTN_THUMB2',
'BTN_THUMBL',
'BTN_THUMBR',
'BTN_TL',
'BTN_TL2',
'BTN_TOOL_AIRBRUSH',
'BTN_TOOL_BRUSH',
'BTN_TOOL_DOUBLETAP',
'BTN_TOOL_FINGER',
'BTN_TOOL_LENS',
'BTN_TOOL_MOUSE',
'BTN_TOOL_PEN',
'BTN_TOOL_PENCIL',
'BTN_TOOL_QUADTAP',
'BTN_TOOL_QUINTTAP',
'BTN_TOOL_RUBBER',
'BTN_TOOL_TRIPLETAP',
'BTN_TOP',
'BTN_TOP2',
'BTN_TOUCH',
'BTN_TR',
'BTN_TR2',
'BTN_TRIGGER',
'BTN_TRIGGER_HAPPY',
'BTN_TRIGGER_HAPPY1',
'BTN_TRIGGER_HAPPY10',
'BTN_TRIGGER_HAPPY11',
'BTN_TRIGGER_HAPPY12',
'BTN_TRIGGER_HAPPY13',
'BTN_TRIGGER_HAPPY14',
'BTN_TRIGGER_HAPPY15',
'BTN_TRIGGER_HAPPY16',
'BTN_TRIGGER_HAPPY17',
'BTN_TRIGGER_HAPPY18',
'BTN_TRIGGER_HAPPY19',
'BTN_TRIGGER_HAPPY2',
'BTN_TRIGGER_HAPPY20',
'BTN_TRIGGER_HAPPY21',
'BTN_TRIGGER_HAPPY22',
'BTN_TRIGGER_HAPPY23',
'BTN_TRIGGER_HAPPY24',
'BTN_TRIGGER_HAPPY25',
'BTN_TRIGGER_HAPPY26',
'BTN_TRIGGER_HAPPY27',
'BTN_TRIGGER_HAPPY28',
'BTN_TRIGGER_HAPPY29',
'BTN_TRIGGER_HAPPY3',
'BTN_TRIGGER_HAPPY30',
'BTN_TRIGGER_HAPPY31',
'BTN_TRIGGER_HAPPY32',
'BTN_TRIGGER_HAPPY33',
'BTN_TRIGGER_HAPPY34',
'BTN_TRIGGER_HAPPY35',
'BTN_TRIGGER_HAPPY36',
'BTN_TRIGGER_HAPPY37',
'BTN_TRIGGER_HAPPY38',
'BTN_TRIGGER_HAPPY39',
'BTN_TRIGGER_HAPPY4',
'BTN_TRIGGER_HAPPY40',
'BTN_TRIGGER_HAPPY5',
'BTN_TRIGGER_HAPPY6',
'BTN_TRIGGER_HAPPY7',
'BTN_TRIGGER_HAPPY8',
'BTN_TRIGGER_HAPPY9',
'BTN_WEST',
'BTN_WHEEL',
'BTN_Z'
)

class IRManager(BaseManager):
    """description of class"""

    def __init__(self, root: LabelFrame):
        """ """
        super(IRManager, self).__init__(root, text="Настройки IR")
        self._modulelist = None

        self._listBox = Listbox(self, width=25)
        self._listBox.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, W))
        self._listBox.bind('<<ListboxSelect>>', self._selectCode)

        commandFrame = ttk.Frame(self, padding=(2, 2, 2, 2))
        commandFrame.grid(row=0, column=1, sticky=(N, S, W))

        btn = Button(commandFrame, text="Создать", command=self._createCode)
        btn.grid(row=0, column=0, sticky=(N, S, E, W))

        btn = Button(commandFrame, text="Удалить", command=self._deleteCode)
        btn.grid(row=2, column=0, sticky=(N, S, E, W))


    def load(self, config: ConfigParser, modulelist: Dict[str, BaseManager]) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("IRBlock"):
            config.add_section("IRBlock")

        section = config["IRBlock"]
        self._listBox.delete(0, "end")

        self._modulelist = modulelist

    def save(self, config: ConfigParser) -> None:
        if not isinstance(config, ConfigParser):
            raise TypeError("config")
        if not config.has_section("IRBlock"):
            config.add_section("IRBlock")

        section = config["IRBlock"]

    def _selectCode(self, event) -> None:
        listBox = event.widget
        selection = listBox.curselection()
        if not selection:
            return
        name = listBox.get(selection[0])

    def _createCode(self) -> None:
        (code, module, param) = KeyCodeCreateDialog().Execute(self, self._modulelist)
        if code is None:
            return
        #if item in self._alarmlist:
        #    messagebox.showerror("Ошибка", "Код {0} уже существует".format(item))
        #    return
        #alarmBlock = self._createAlarmByType(type, item)
        #if alarmBlock is not None:
        #    self._alarmlist[item] = alarmBlock
        #    self._listBox.insert("end", item)
        self._listBox.insert("end", code)

    def _deleteCode(self) -> None:
        selection = self._listBox.curselection()
        if not selection:
            return
        name = self._listBox.get(selection[0])
        if messagebox.askquestion("Удалить", "Вы действительно хотите удалить код {0}".format(name)) == "no":
            return
        self._listBox.delete(selection)

class KeyCodeCreateDialog(ModalDialog):

    def Execute(self, root, modulelist: Dict[str, BaseManager]) -> Tuple[str, str, str]:
        self._modal = Toplevel(root)
        self._modal.title("Создать")
        # self._modal.geometry('+400+400')
        self._valueKeyCode = StringVar()
        self._valueModule = StringVar()
        self._valueParam  = StringVar()

        lblCode = Label(self._modal, text="Код кнопки")
        lblCode.grid(row=0, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, W))

        comboCode = ttk.Combobox(self._modal, state="readonly", values=KEY_CODE_LIST, textvariable=self._valueKeyCode)
        comboCode.grid(row=1, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))
        comboCode.bind('<<ComboboxSelected>>', lambda e: self._selectCode())

        lblMod = Label(self._modal, text="Модуль")
        lblMod.grid(row=2, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, W))

        comboModule = ttk.Combobox(self._modal, state="readonly", values=modulelist, textvariable=self._valueModule)
        comboModule.grid(row=3, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))

        lblParam = Label(self._modal, text="Параметры")
        lblParam.grid(row=4, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, W))
        
        entry = Entry(self._modal, textvariable=self._valueParam)
        entry.grid(row=5, column=0, columnspan=4, padx=2, pady=2, sticky=(N, S, E, W))

        self._btnOk = Button(self._modal, text="OK", state="disabled", command=self._ok)
        self._btnOk.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        btn = Button(self._modal, text="Cancel", command=self._cancel)
        btn.grid(row=6, column=2, columnspan=2, padx=2, pady=2, sticky=(N, S, E, W))

        self._waitDialog(self._modal, root)

        code = self._valueKeyCode.get()
        module  = self._valueModule.get()
        param = self._valueParam.get()

        code = code if code else None

        return (code, module, param)

    def _selectCode(self) -> None:
        self._btnOk.configure(state="normal")

    def _ok(self) -> None:
        self._modal.destroy()

    def _cancel(self) -> None:
        self._modal.destroy()
        self._valueKeyCode.set("")
        self._valueModule.set("")
        self._valueParam.set("")
