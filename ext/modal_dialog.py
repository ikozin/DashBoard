from typing import Tuple
from tkinter import font, colorchooser, BooleanVar, IntVar, StringVar, Toplevel, LabelFrame, Label, Entry, Checkbutton, Spinbox, Listbox, Button, Scrollbar, Canvas, N, S, E, W, RIGHT, VERTICAL, FALSE, TRUE, LEFT, BOTH, Y, NW
from tkinter.ttk import Frame, Combobox


class ModalDialog:

    def _ok(self):
        pass

    def _cancel(self):
        pass

    def _wait_dialog(self, modal, root):
        modal.bind('<Key-Return>', lambda e: self._ok())
        modal.bind('<Key-Escape>', lambda e: self._cancel())
        modal.transient(root)
        modal.grab_set()
        modal.resizable(False, False)
        main = root.winfo_toplevel()
        main.update_idletasks()
        pos_x = main.winfo_x() + ((main.winfo_width() - modal.winfo_width()) >> 1)
        pos_y = main.winfo_y() + ((main.winfo_height() - modal.winfo_height()) >> 1)
        modal.geometry("+{0}+{1}".format(pos_x, pos_y))
        root.wait_window(modal)


class EntryModalDialog(ModalDialog):

    def __init__(self, title):
        self._title = str(title)
        self._modal = None
        self._value = None

    def execute(self, root, text):
        self._modal = Toplevel(root)
        self._modal.title(self._title)
        self._value = StringVar()
        self._value.set(text)
        entry = Entry(self._modal, textvariable=self._value)
        entry.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky=(N, S, E, W))
        entry.focus_set()
        btn = Button(self._modal, text="OK", command=self._ok)
        btn.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=(N, S, E, W))
        btn = Button(self._modal, text="Cancel", command=self._cancel)
        btn.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky=(N, S, E, W))
        self._wait_dialog(self._modal, root)
        return self._value.get()

    def _ok(self):
        self._modal.destroy()

    def _cancel(self):
        self._modal.destroy()
        self._value.set("")


class ColorsChooserFrame(LabelFrame):

    def __init__(self, root, text):
        if not isinstance(text, str):
            raise TypeError("text")
        super(ColorsChooserFrame, self).__init__(root, text=text)
        self._root = root
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self._back_color = None
        self._fore_color = None
        self._back_selector = Button(self, text="Цвет фона", command=self._select_back_color)
        self._back_selector.grid(row=0, column=0, padx=2, pady=2, sticky=(N, S, E, W))
        self._fore_selector = Button(self, text="Цвет текста", command=self._select_fore_color)
        self._fore_selector.grid(row=0, column=1, padx=2, pady=2, sticky=(N, S, E, W))
        self.load((0, 0, 0), (0, 0, 0))

    def load(self, back_color, fore_color):
        if not isinstance(back_color, tuple):
            raise TypeError("back_color")
        if not isinstance(fore_color, tuple):
            raise TypeError("fore_color")
        self._back_color = back_color
        self._fore_color = fore_color
        back_color = "#%02x%02x%02x" % back_color
        fore_color = "#%02x%02x%02x" % fore_color
        self._back_selector.configure(background=back_color, foreground=fore_color)
        self._fore_selector.configure(background=back_color, foreground=fore_color)

    def _select_back_color(self):
        (triple_color, tk_color) = colorchooser.askcolor(self._back_color)
        if triple_color is None:
            return
        self._back_selector.configure(background=tk_color)
        self._fore_selector.configure(background=tk_color)

        self._back_color = (int(triple_color[0]), int(triple_color[1]), int(triple_color[2]))

    def _select_fore_color(self):
        (triple_color, tk_color) = colorchooser.askcolor(self._fore_color)
        if triple_color is None:
            return
        self._back_selector.configure(foreground=tk_color)
        self._fore_selector.configure(foreground=tk_color)
        self._fore_color = (int(triple_color[0]), int(triple_color[1]), int(triple_color[2]))

    def get_result(self) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        return (self._back_color, self._fore_color)


class FontChooserFrame(LabelFrame):

    def __init__(self, root, text):
        if not isinstance(text, str):
            raise TypeError("text")
        super(FontChooserFrame, self).__init__(root, text=text)
        self._root = root
        self._font_name = StringVar()
        self._font_size = IntVar()
        self._is_bold = BooleanVar()
        self._is_italic = BooleanVar()
        Label(self, text="Шрифт").grid(row=0, column=0, padx=2, pady=2)
        fonts = list(font.families())
        list.sort(fonts)
        combo = Combobox(self, values=fonts, textvariable=self._font_name)
        combo.grid(row=0, column=1, padx=2, pady=2)
        lbl = Label(self, text="Размер")
        lbl.grid(row=0, column=2, padx=2, pady=2)
        spin = Spinbox(self, from_=1, to=500, increment=1, width=4, textvariable=self._font_size)
        spin.grid(row=0, column=3, padx=2, pady=2)
        chk = Checkbutton(self, text="Жирный", variable=self._is_bold)
        chk.grid(row=0, column=4, padx=2, pady=2)
        chk = Checkbutton(self, text="Наклон", variable=self._is_italic)
        chk.grid(row=0, column=5, padx=2, pady=2)

    def load(self, font_name, font_size, is_bold, is_italic):
        if not isinstance(font_name, str):
            raise TypeError("font_name")
        if not isinstance(font_size, int):
            raise TypeError("font_size")
        if not isinstance(is_bold, bool):
            raise TypeError("is_bold")
        if not isinstance(is_italic, bool):
            raise TypeError("is_italic")
        self._font_name.set(font_name)
        self._font_size.set(font_size)
        self._is_bold.set(is_bold)
        self._is_italic.set(is_italic)

    def get_result(self):
        return (self._font_name.get(), self._font_size.get(), self._is_bold.get(), self._is_italic.get())


class XYFrame(LabelFrame):
    """description of class"""

    def __init__(self, root, text, text_x, text_y):
        super(XYFrame, self).__init__(root, text=text)
        self._pos_x = IntVar()
        self._pos_y = IntVar()
        lbl = Label(self, text=text_x)
        lbl.grid(row=0, column=0, padx=2, pady=2)
        spin = Spinbox(self, from_=0, to=1800, increment=1, width=5, textvariable=self._pos_x)
        spin.grid(row=0, column=1, padx=2, pady=2)
        lbl = Label(self, text=text_y)
        lbl.grid(row=0, column=2, padx=2, pady=2)
        spin = Spinbox(self, from_=0, to=1800, increment=1, width=5, textvariable=self._pos_y)
        spin.grid(row=0, column=3, padx=2, pady=2)

    def load(self, pos_x, pos_y):
        self._pos_x.set(pos_x)
        self._pos_y.set(pos_y)

    def get_result(self):
        return (self._pos_x.get(), self._pos_y.get())


class SelectFrame(LabelFrame):

    def __init__(self, root, text):
        super(SelectFrame, self).__init__(root, text=text)
        self._sel_list = []
        self._src_list = []
        btn = Button(self, text="Вверх", command=self._command_up)
        btn.grid(row=0, column=0, sticky=(N, S, E, W), padx=5, pady=5)
        btn = Button(self, text="Вниз", command=self._command_down)
        btn.grid(row=1, column=0, sticky=(N, S, E, W), padx=5, pady=5)
        self._sel_listbox = Listbox(self)
        self._sel_listbox.grid(row=0, column=1, rowspan=2)
        btn = Button(self, text="Включить", command=self._command_include)
        btn.grid(row=0, column=2, sticky=(N, S, E, W), padx=5, pady=5)
        btn = Button(self, text="Выключить", command=self._command_exclude)
        btn.grid(row=1, column=2, sticky=(N, S, E, W), padx=5, pady=5)
        self._src_listbox = Listbox(self)
        self._src_listbox.grid(row=0, column=3, rowspan=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def load(self, selection=[], mod_list=[]):
        self._sel_list = selection
        self._src_list = mod_list
        for item in self._sel_list:
            self._sel_listbox.insert("end", item)
        self._sel_listbox.selection_set(0)
        for item in self._src_list:
            self._src_listbox.insert("end", item)
        self._src_listbox.selection_set(0)

    def get_result(self):
        return ", ".join(self._sel_list)

    def _command_up(self):
        selection = self._sel_listbox.curselection()
        if not selection:
            return
        if selection[0] == 0:
            return
        item = self._sel_list.pop(selection[0])
        self._sel_list.insert(selection[0] - 1, item)
        self._update_selected_list(selection[0] - 1)

    def _command_down(self):
        selection = self._sel_listbox.curselection()
        if not selection:
            return
        if selection[0] == len(self._sel_list) - 1:
            return
        item = self._sel_list.pop(selection[0])
        self._sel_list.insert(selection[0] + 1, item)
        self._update_selected_list(selection[0] + 1)

    def _command_include(self):
        selection = self._src_listbox.curselection()
        if not selection:
            return
        name = self._src_listbox.get(selection[0])
        if name in self._sel_list:
            return
        self._sel_list.append(name)
        self._update_selected_list()

    def _command_exclude(self):
        selection = self._src_listbox.curselection()
        if not selection:
            return
        name = self._src_listbox.get(selection[0])
        if name not in self._sel_list:
            return
        self._sel_list.remove(name)
        self._update_selected_list()

    def _update_selected_list(self, selection=None):
        self._sel_listbox.delete(0, 'end')
        for item in self._sel_list:
            self._sel_listbox.insert("end", item)
        if selection:
            self._sel_listbox.selection_set(selection)


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
        canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

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
