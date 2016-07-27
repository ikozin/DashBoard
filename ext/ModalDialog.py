from tkinter import *
from tkinter import ttk
from tkinter import font
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
        entry.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky=(N,S,E,W))
        entry.focus_set()
        ttk.Button(self._modal, text="OK", command=self._ok).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=(N,S,E,W))
        ttk.Button(self._modal, text="Cancel", command=self._cancel).grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky=(N,S,E,W))
        self._waitDialog(self._modal, root)
        return self._value.get()

    def _ok(self):
        """ """
        self._modal.destroy()

    def _cancel(self):
        """ """
        self._modal.destroy()
        self._value.set("")


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
        self._backSelector.grid(row=0, column=0, padx=2, pady=2, sticky=(N,S,E,W))
        self._foreSelector = Button(self, text="Цвет текста", command=self._selectForeColor)
        self._foreSelector.grid(row=0, column=1, padx=2, pady=2, sticky=(N,S,E,W))
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


class XYFrame(ttk.LabelFrame):
    """description of class"""

    def __init__(self, root, text, textX, textY):
        """ """
        super(XYFrame, self).__init__(root, text=text)
        self._X = IntVar()
        self._Y = IntVar()
        ttk.Label(self, text=textX).grid(row=0, column=0, padx=2, pady=2)
        Spinbox(self, from_=0, to=1800, increment=1, width=5, textvariable=self._X).grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(self, text=textY).grid(row=0, column=2, padx=2, pady=2)
        Spinbox(self, from_=0, to=1800, increment=1, width=5, textvariable=self._Y).grid(row=0, column=3, padx=2, pady=2)

    def load(self, x, y):
        """ """
        self._X.set(x)
        self._Y.set(y)

    def getResult(self):
        """ """
        return (self._X.get(), self._Y.get())


# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

