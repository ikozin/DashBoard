#from tkinter import *
#from tkinter import ttk
#root = Tk()

## Initialize our country "databases":
##  - the list of country codes (a subset anyway)
##  - a parallel list of country names, in the same order as the country codes
##  - a hash table mapping country code to population<
#countrycodes = ('ar', 'au', 'be', 'br', 'ca', 'cn', 'dk', 'fi', 'fr', 'gr', 'in', 'it', 'jp', 'mx', 'nl', 'no', 'es', 'se', 'ch')
#countrynames = ('Argentina', 'Australia', 'Belgium', 'Brazil', 'Canada', 'China', 'Denmark', \
#        'Finland', 'France', 'Greece', 'India', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway', 'Spain', \
#        'Sweden', 'Switzerland')
#cnames = StringVar(value=countrynames)
#populations = {'ar':41000000, 'au':21179211, 'be':10584534, 'br':185971537, \
#        'ca':33148682, 'cn':1323128240, 'dk':5457415, 'fi':5302000, 'fr':64102140, 'gr':11147000, \
#        'in':1131043000, 'it':59206382, 'jp':127718000, 'mx':106535000, 'nl':16402414, \
#        'no':4738085, 'es':45116894, 'se':9174082, 'ch':7508700}

## Names of the gifts we can send
#gifts = { 'card':'Greeting card', 'flowers':'Flowers', 'nastygram':'Nastygram'}

## State variables
#gift = StringVar()
#sentmsg = StringVar()
#statusmsg = StringVar()

## Called when the selection in the listbox changes; figure out
## which country is currently selected, and then lookup its country
## code, and from that, its population.  Update the status message
## with the new population.  As well, clear the message about the
## gift being sent, so it doesn't stick around after we start doing
## other things.
#def showPopulation(*args):
#    idxs = lbox.curselection()
#    if len(idxs)==1:
#        idx = int(idxs[0])
#        code = countrycodes[idx]
#        name = countrynames[idx]
#        popn = populations[code]
#        statusmsg.set("The population of %s (%s) is %d" % (name, code, popn))
#    sentmsg.set('')

## Called when the user double clicks an item in the listbox, presses
## the "Send Gift" button, or presses the Return key.  In case the selected
## item is scrolled out of view, make sure it is visible.
##
## Figure out which country is selected, which gift is selected with the 
## radiobuttons, "send the gift", and provide feedback that it was sent.
#def sendGift(*args):
#    idxs = lbox.curselection()
#    if len(idxs)==1:
#        idx = int(idxs[0])
#        lbox.see(idx)
#        name = countrynames[idx]
#        # Gift sending left as an exercise to the reader
#        sentmsg.set("Sent %s to leader of %s" % (gifts[gift.get()], name))

## Create and grid the outer content frame
#c = ttk.Frame(root, padding=(5, 5, 12, 0))
#c.grid(column=0, row=0, sticky=(N,W,E,S))
#root.grid_columnconfigure(0, weight=1)
#root.grid_rowconfigure(0,weight=1)

## Create the different widgets; note the variables that many
## of them are bound to, as well as the button callback.
## Note we're using the StringVar() 'cnames', constructed from 'countrynames'
#lbox = Listbox(c, listvariable=cnames, height=5)
#lbl = ttk.Label(c, text="Send to country's leader:")
#g1 = ttk.Radiobutton(c, text=gifts['card'], variable=gift, value='card')
#g2 = ttk.Radiobutton(c, text=gifts['flowers'], variable=gift, value='flowers')
#g3 = ttk.Radiobutton(c, text=gifts['nastygram'], variable=gift, value='nastygram')
#send = ttk.Button(c, text='Send Gift', command=sendGift, default='active')
#sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
#status = ttk.Label(c, textvariable=statusmsg, anchor=W)

## Grid all the widgets
#lbox.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W))
#lbl.grid(column=1, row=0, padx=10, pady=5)
#g1.grid(column=1, row=1, sticky=W, padx=20)
#g2.grid(column=1, row=2, sticky=W, padx=20)
#g3.grid(column=1, row=3, sticky=W, padx=20)
#send.grid(column=2, row=4, sticky=E)
#sentlbl.grid(column=1, row=5, columnspan=2, sticky=N, pady=5, padx=5)
#status.grid(column=0, row=6, columnspan=2, sticky=(W,E))
#c.grid_columnconfigure(0, weight=1)
#c.grid_rowconfigure(5, weight=1)

## Set event bindings for when the selection in the listbox changes,
## when the user double clicks the list, and when they hit the Return key
#lbox.bind('<<ListboxSelect>>', showPopulation)
#lbox.bind('<Double-1>', sendGift)
#root.bind('<Return>', sendGift)

## Colorize alternating lines of the listbox
#for i in range(0,len(countrynames),2):
#    lbox.itemconfigure(i, background='#f0f0ff')

## Set the starting state of the interface, including selecting the
## default gift to send, and clearing the messages.  Select the first
## country in the list; because the <<ListboxSelect>> event is only
## generated when the user makes a change, we explicitly call showPopulation.
#gift.set('card')
#sentmsg.set('')
#statusmsg.set('')
#lbox.selection_set(0)
#showPopulation()

#root.mainloop()




import datetime

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

fonts = [
    '@Arial Unicode MS','@Batang','@BatangChe','@DFKai-SB','@DengXian','@Dotum','@DotumChe','@FangSong','@Gulim','@GulimChe','@Gungsuh','@GungsuhChe',
    '@KaiTi','@MS Gothic','@MS Mincho','@MS PGothic','@MS PMincho','@MS UI Gothic','@Malgun Gothic','@Meiryo','@Meiryo UI','@Microsoft JhengHei',
    '@Microsoft MHei','@Microsoft NeoGothic','@Microsoft YaHei','@MingLiU','@MingLiU-ExtB','@MingLiU_HKSCS','@MingLiU_HKSCS-ExtB','@NSimSun',
    '@PMingLiU','@PMingLiU-ExtB','@SimHei','@SimSun','@SimSun-ExtB','@Yu Gothic','Agency FB','Aharoni','Algerian','Andalus','Angsana New','AngsanaUPC',
    'Aparajita','Arabic Transparent','Arabic Typesetting','Arial','Arial Baltic','Arial Black','Arial CE','Arial CYR','Arial Cyr','Arial Greek',
    'Arial Narrow','Arial Rounded MT Bold','Arial TUR','Arial Unicode MS','Baskerville Old Face','Batang','BatangChe','Bauhaus 93','Bell MT', 
    'Berlin Sans FB','Berlin Sans FB Demi','BernardMT Condensed','Blackadder ITC','Bodoni MT','Bodoni MT Black','Bodoni MT Condensed',
    'Bodoni MT Poster Compressed','Book Antiqua','Bookman Old Style','Bookshelf Symbol 7','Bradley Hand ITC','Britannic Bold','Broadway',
    'Browallia New','BrowalliaUPC','Brush Script MT','Buxton Sketch','Calibri','Californian FB','Calisto MT','Cambria','Cambria Math','Candara',
    'Castellar','Centaur','Century','Century Gothic','Century Schoolbook','Chiller','Colonna MT','Comic Sans MS','Consolas','Constantia','Cooper Black',
    'Copperplate Gothic Bold','Copperplate Gothic Light','Corbel','Cordia New','CordiaUPC','Courier','Courier','Courier New','Courier New Baltic',
    'Courier New CE','Courier New CYR','Courier New Cyr','Courier New Greek','Courier New TUR','Curlz MT','DFKai-SB','DaunPenh','David','DengXian', 
    'DilleniaUPC','DokChampa','Dotum','DotumChe','Ebrima', 'Edwardian Script ITC','Elephant','Engravers MT','Eras Bold ITC','Eras Demi ITC',
    'Eras Light ITC','Eras Medium ITC','Estrangelo Edessa','EucrosiaUPC','Euphemia','FangSong','Felix Titling','Fixedsys','Footlight MT Light',
    'Forte', 'FrankRuehl','Franklin Gothic Book','Franklin Gothic Demi','Franklin Gothic Demi Cond','Franklin Gothic Heavy','Franklin Gothic Medium',
    'Franklin Gothic Medium Cond','FreesiaUPC','Freestyle Script','French Script MT','Gabriola','Garamond','Gautami','Georgia','Gigi','Gill Sans MT',
    'Gill Sans MT Condensed','Gill Sans MT Ext Condensed Bold','Gill Sans Ultra Bold','Gill Sans Ultra Bold Condensed','Gisha',
    'Gloucester MT Extra Condensed','Goudy Old Style','Goudy Stout','Gulim','GulimChe','Gungsuh','GungsuhChe','Haettenschweiler','Harlow Solid Italic',
    'Harrington','High Tower Text','Impact','Imprint MT Shadow','Informal Roman','IrisUPC','Iskoola Pota','JasmineUPC','Jokerman','Juice ITC','KaiTi', 
    'Kalinga','Kartika','Khmer UI','KodchiangUPC','Kokila','Kristen ITC','Kunstler Script','Lao UI','Latha','Leelawadee','Levenim MT','LilyUPC',
    'Lucida Bright','Lucida Calligraphy','LucidaConsole','Lucida Fax','Lucida Handwriting','Lucida Sans','Lucida Sans Typewriter','Lucida Sans Unicode',
    'MS Gothic','MS Mincho','MS Outlook','MS PGothic','MS PMincho','MS Reference Sans Serif','MS Reference Specialty','MS Sans Serif','MS Serif', 
    'MS UI Gothic','MT Extra','MV Boli','Magneto','MaiandraGD','Malgun Gothic','Mangal','Marlett','Matura MT Script Capitals','Meiryo','Meiryo UI',
    'Microsoft Himalaya','Microsoft JhengHei','Microsoft MHei','Microsoft NeoGothic','Microsoft New Tai Lue','Microsoft PhagsPa','Microsoft Sans Serif',
    'Microsoft Tai Le','Microsoft Uighur','Microsoft YaHei','MicrosoftYi Baiti','MingLiU','MingLiU-ExtB','MingLiU_HKSCS','MingLiU_HKSCS-ExtB','Miriam',
    'Miriam Fixed','Mistral','Modern','Modern No. 20','Mongolian Baiti','Monotype Corsiva','MoolBoran','NSimSun','Narkisim','Niagara Engraved',
    'Niagara Solid', 'Nyala','OCR A Extended','Old English Text MT','Onyx','PMingLiU','PMingLiU-ExtB','Palace Script MT','Palatino Linotype','Papyrus',
    'Parchment','Perpetua','Perpetua Titling MT','Plantagenet Cherokee','Playbill','Poor Richard','Pristina','Raavi','Rage Italic','Ravie','Rockwell', 
    'Rockwell Condensed','Rockwell Extra Bold','Rod','Roman','Sakkal Majalla','Script','Script MT Bold','Segoe Marker','Segoe Print','Segoe Script',
    'Segoe UI','Segoe UI Light','Segoe UI Semibold','Segoe UI Symbol','Segoe WP','Segoe WP Black','Segoe WP Light','Segoe WP SemiLight',
    'Segoe WP Semibold','Shonar Bangla','Showcard Gothic','Shruti','SimHei','SimSun','SimSun-ExtB','Simplified Arabic','Simplified Arabic Fixed',
    'SketchFlow Print','Small Fonts','Snap ITC','Stencil','Sylfaen','Symbol','System','Tahoma','TeamViewer11','Tempus Sans ITC','Terminal',
    'Times New Roman','Times New Roman Baltic','Times New Roman CE','Times New Roman CYR','Times New Roman Cyr','Times New Roman Greek',
    'Times New Roman TUR','Traditional Arabic','Trebuchet MS','Tunga','Tw Cen MT','Tw Cen MT Condensed','Tw Cen MT Condensed Extra Bold','Utsaah',
    'Vani','Verdana','Vijaya','Viner Hand ITC','Vivaldi','Vladimir Script','Vrinda','Webdings','Wide Latin','Wingdings','Wingdings 2','Wingdings 3',
    'Yu Gothic']

class App(object):
    """description of class"""
    def __init__(self):
        self._root = Tk()
        self._root.title('DashBoard Tool')
        #self._root.columnconfigure(0, weight=1)
        #self._root.rowconfigure(0, weight=1)
        
        window = Frame(self._root)
        window.grid(row=0, column=0, sticky=(N,S,E,W))

        Button(window, text="Вверх", command=self.command_up).grid(row=0, column=0, sticky=(N,S,E,W), padx=5, pady=5)
        Button(window, text="Вниз", command=self.command_down).grid(row=1, column=0, sticky=(N,S,E,W), padx=5, pady=5)
        self._selListBox = Listbox(window)
        self._selListBox.grid(row=0, column=1, rowspan=2)
        Button(window, text="Включить", command=self.command_include).grid(row=0, column=2, sticky=(N,S,E,W), padx=5, pady=5)
        Button(window, text="Выключить", command=self.command_exclude).grid(row=1, column=2, sticky=(N,S,E,W), padx=5, pady=5)
        self._srcListBox = Listbox(window)
        self._srcListBox.grid(row=0, column=3, rowspan=2)

        window.columnconfigure(1, weight=1)
        window.columnconfigure(3, weight=1)
        window.rowconfigure(0, weight=1)
        window.rowconfigure(1, weight=1)

        self._selList = []
        self._srcList = ["Main", "Time", "Alarm", "Voice", "YandexNews", "OpenWeatherMap", "WunderGround", "Calendar", "Swap", "Watcher"]

        for item in self._selList:  self._selListBox.insert("end", item)
        self._selListBox.selection_set(0)
        for item in self._srcList:  self._srcListBox.insert("end", item)
        self._srcListBox.selection_set(0)

        self._root.bind('<Key-Escape>', lambda e: self._root.destroy())
        #self._root.resizable(False, False)
        self._root.geometry("+0+0")
        self._root.mainloop()
    
    def command_up(self):
        selection = self._selListBox.curselection() 
        if not selection: return
        if selection[0] == 0: return
        item = self._selList.pop(selection[0])
        self._selList.insert(selection[0] - 1, item)
        self.update_selected_list(selection[0] - 1)


    def command_down(self):
        selection = self._selListBox.curselection() 
        if not selection: return
        if selection[0] == len(self._selList) - 1: return
        item = self._selList.pop(selection[0])
        self._selList.insert(selection[0] + 1, item)
        self.update_selected_list(selection[0] + 1)

    def command_include(self):
        selection = self._srcListBox.curselection() 
        if not selection: return
        name = self._srcListBox.get(selection[0])
        if name in self._selList: return

        self._selList.append(name)
        self.update_selected_list()
        pass

    def command_exclude(self):
        selection = self._srcListBox.curselection() 
        if not selection: return
        name = self._srcListBox.get(selection[0])
        if name not in self._selList: return

        self._selList.remove(name)
        self.update_selected_list()
        pass

    def update_selected_list(self, selection = None):
        self._selListBox.delete(0, 'end')
        for item in self._selList:  self._selListBox.insert("end", item)
        if selection:
            self._selListBox.selection_set(selection)

def main():            
    App()
    
if __name__ == "__main__":
    main()

    #currentTime = datetime.datetime.now()
    #startTime = datetime.datetime.strptime("14:44:10", "%H:%M:%S")
    #stopTime = datetime.datetime.strptime("14:50:00", "%H:%M:%S")

    #print((currentTime - startTime).seconds)
    #print((currentTime - stopTime).seconds)


    #print((currentDate - date1).seconds)
    #print((date1 - currentDate).seconds)
    #print(3600*24)
    #print((currentDate - date2).seconds)
    #print((date2 - currentDate).seconds)
    #print(3600*24)

    #list = [ "Main", "Time", "Alarm", "Voice", "YandexNews", "OpenWeatherMap", "WunderGround", "Calendar", "Swap", "Watcher"]
    #print(list)
    #item = list.pop(1)
    #print(item)
    #print(list)
    #list.insert(0, item)
    #print(list)
