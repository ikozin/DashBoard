from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser

class ModalDialog:

    def _ok(self):
        """ """
        pass

    def _cancel(self):
        """ """
        pass

    def _waitDialog(self, modal, root):
        """ """
        modal.bind('<Key-Return>', lambda e: self._ok())
        modal.bind('<Key-Escape>', lambda e: self._cancel())
        modal.transient(root)
        modal.grab_set()
        modal.resizable(False, False)
        main = root.winfo_toplevel()
        main.update_idletasks()
        x = main.winfo_x() + ((main.winfo_width() - modal.winfo_width()) >> 1)
        y = main.winfo_y() + ((main.winfo_height() - modal.winfo_height()) >> 1)
        modal.geometry("+{0}+{1}".format(x, y))
        root.wait_window(modal)


class EntryModalDialog(ModalDialog):

    def __init__(self, title):
        """ """
        self._title = str(title)

    def Execute(self, root, text):
        """ """
        self._modal = Toplevel(root)
        self._modal.title(self._title)
        self._value = StringVar()
        self._value.set(text)
        entry = Entry(self._modal, textvariable=self._value)
        entry.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky=NSEW)
        entry.focus_set()
        ttk.Button(self._modal, text="OK", command=self._ok).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=NSEW)
        ttk.Button(self._modal, text="Cancel", command=self._cancel).grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky=NSEW)
        self._waitDialog(self._modal, root)
        return self._value.get()

    def _ok(self):
        """ """
        self._modal.destroy()

    def _cancel(self):
        """ """
        self._modal.destroy()
        self._value.set("")

#class ColorChooserFrame(LabelFrame):
#    def __init__(self, root, text, color):
#        """ """
#        if not isinstance(color, tuple): raise TypeError("color")
#        super(ColorChooserFrame, self).__init__(root, text=str(text))
#        self._root = root
#        self._vR = IntVar()
#        self._vG = IntVar()
#        self._vB = IntVar()
#        self._vR.set(color[0])
#        self._vG.set(color[1])
#        self._vB.set(color[2])
#        Label(self, text = "Красный:").grid(row = 0, column = 0, padx = 2, pady = 2)
#        Spinbox(self, from_=0, to=255, increment=1, width=3, textvariable=self._vR).grid(row = 0, column = 1, padx = 2, pady = 2)
#        Label(self, text = "Зеленый:").grid(row = 0, column = 2, padx = 2, pady = 2)
#        Spinbox(self, from_=0, to=255, increment=1, width=3, textvariable=self._vG).grid(row = 0, column = 3, padx = 2, pady = 2)
#        Label(self, text = "Синий:").grid(row = 0, column = 4, padx = 2, pady = 2)
#        Spinbox(self, from_=0, to=255, increment=1, width=3, textvariable=self._vB).grid(row = 0, column = 5, padx = 2, pady = 2)
#        Button(self, text = "...", command=self._selectColor).grid(row = 0, column = 6, padx = 2, pady = 2)
#    def _selectColor(self):
#        """ """
#        color = (self._vR.get(), self._vG.get(), self._vB.get())
#        (tripleColor, tkColor) = colorchooser.askcolor(color)
#        if tripleColor is None: return
#        self._vR.set(int(tripleColor[0]))
#        self._vG.set(int(tripleColor[1]))
#        self._vB.set(int(tripleColor[2]))
#    def getResult(self):
#        """ """
#        color = (self._vR.get(), self._vG.get(), self._vB.get())
#        return color

#class ColorChooserFrame(LabelFrame):
#    def __init__(self, root, text, color):
#        """ """
#        if not isinstance(color, tuple): raise TypeError("color")
#        super(ColorChooserFrame, self).__init__(root, text=str(text))
#        self._root = root
#        self._color = color
#        color = "#%02x%02x%02x" % color
#        self._selector = Button(self, text=str(text), background=color, command=self._selectColor)
#        self._selector.grid(row = 0, column = 0, padx = 2, pady = 2)
#    def _selectColor(self):
#        """ """
#        (tripleColor, tkColor) = colorchooser.askcolor(self._color)
#        if tripleColor is None: return
#        self._selector.configure(background=tkColor)
#        self._color = tripleColor
#    def getResult(self):
#        """ """
#        return self._color

class ColorsChooserFrame(ttk.LabelFrame):

    def __init__(self, root, text):
        """ """
        if not isinstance(text, str): raise TypeError("text")
        super(ColorsChooserFrame, self).__init__(root, text=text)
        self._root = root
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self._backColor = None
        self._foreColor = None
        self._backSelector = Button(self, text="Цвет фона", command=self._selectBackColor)
        self._backSelector.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
        self._foreSelector = Button(self, text="Цвет текста", command=self._selectForeColor)
        self._foreSelector.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
        self.load((0, 0, 0), (255, 255, 255))
    def load(self, backColor, foreColor):
        """ """
        if not isinstance(backColor, tuple): raise TypeError("backColor")
        if not isinstance(foreColor, tuple): raise TypeError("foreColor")
        self._backColor = backColor
        self._foreColor = foreColor
        backColor = "#%02x%02x%02x" % backColor
        foreColor = "#%02x%02x%02x" % foreColor
        self._backSelector.configure(background=backColor, foreground=foreColor)
        self._foreSelector.configure(background=backColor, foreground=foreColor)
    def _selectBackColor(self):
        """ """
        (tripleColor, tkColor) = colorchooser.askcolor(self._backColor)
        if tripleColor is None: return
        self._backSelector.configure(background=tkColor)
        self._foreSelector.configure(background=tkColor)
        self._backColor = (int(tripleColor[0]), int(tripleColor[1]), int(tripleColor[2]))
    def _selectForeColor(self):
        """ """
        (tripleColor, tkColor) = colorchooser.askcolor(self._foreColor)
        if tripleColor is None: return
        self._backSelector.configure(foreground=tkColor)
        self._foreSelector.configure(foreground=tkColor)
        self._foreColor = (int(tripleColor[0]), int(tripleColor[1]), int(tripleColor[2]))
    def getResult(self):
        """ """
        return (self._backColor, self._foreColor)



class FontChooserFrame(ttk.LabelFrame):

    def __init__(self, root, text):
        """ """
        if not isinstance(text, str): raise TypeError("text")
        super(FontChooserFrame, self).__init__(root, text=text)
        self._root = root
        self._fontName = StringVar()
        self._fontSize = IntVar()
        self._isBold = BooleanVar()
        self._isItalic = BooleanVar()
        ttk.Label(self, text="Шрифт").grid(row=0, column=0, padx=2, pady=2)
        fonts = list(font.families())
        list.sort(fonts)
        ttk.Combobox(self, values=fonts, textvariable=self._fontName).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(self, text="Размер").grid(row=0, column=2, padx=2, pady=2)
        Spinbox(self, from_=1, to=500, increment=1, width=4, textvariable=self._fontSize).grid(row=0, column=3, padx=2, pady=2)
        ttk.Checkbutton(self, text="Жирный", variable=self._isBold).grid(row=0, column=4, padx=2, pady=2)
        ttk.Checkbutton(self, text="Наклон", variable=self._isItalic).grid(row=0, column=5, padx=2, pady=2)
    def load(self, fontName, fontSize, isBold, isItalic):
        """ """
        if not isinstance(fontName, str):  raise TypeError("fontName")
        if not isinstance(fontSize, int):  raise TypeError("fontSize")
        if not isinstance(isBold, bool):   raise TypeError("isBold")
        if not isinstance(isItalic, bool): raise TypeError("isItalic")
        self._fontName.set(fontName)
        self._fontSize.set(fontSize)
        self._isBold.set(isBold)
        self._isItalic.set(isItalic)
    def getResult(self):
        """ """
        return (self._fontName.get(), self._fontSize.get(), self._isBold.get(), self._isItalic.get())



