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
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)
        
        window = Frame(self._root)
        window.grid(row=0, column=0, sticky=(N,S,E,W))
        window.rowconfigure(1, weight=1)
        window.columnconfigure(0, weight=1)

        for r in range(0, 10):
            Checkbutton(window, text="Demo Text - " + str(r)).grid(row=r, column=0)


        self._root.bind('<Key-Escape>', lambda e: self._root.destroy())
        #self._root.resizable(False, False)
        self._root.geometry("+0+0")
        self._root.mainloop()

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

