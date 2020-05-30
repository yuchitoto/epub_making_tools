#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This plugin is rewritten from John Crew's TextImporter v0.1.0.5 to suit personal use
John's copyright statement below
Original Plugin Posted URL: https://www.mobileread.com/forums/showthread.php?t=285771
"""

"""
Copyright (c) 2017 John Crew
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
for commercial and non-commercial purposes are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox as tkMessageBox        #Needed for messagebox
from tkinter import filedialog  #Needed for the file dialog box
import tkinter as tk
import locale
import ntpath
from sigil_bs4 import BeautifulSoup
from pTagger import PTagger
from GenUtils import centerWindow
import csv

class importTxtFile:
    dlgTop=""
    def __init__(self, parent, bk, prefs):
        self.top = tk.Toplevel(parent)
        self.top.title("txt importer")
        importTxtFile.dlgTop=self.top    #used to ensure this dialog window is destroyed before main section continues
        self.bk=bk
        self.prefs = prefs
        self.rule = None
        self.rule_path = tk.StringVar()
        self.rule_path.set("Rule:")

        self.is_checked = IntVar()

        self.is_checked.set(self.prefs['ConvertAngularBrackets'])

        self.dlgframe = ttk.Frame(self.top, padding="15 15 12 12")
        self.dlgframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.dlgframe.columnconfigure(1, weight=1)
        self.dlgframe.rowconfigure(1, weight=1)

        self.check = ttk.Checkbutton(self.dlgframe, text="Convert angular brackets to html code", variable=self.is_checked)
        self.check.grid(column=0, row=0, sticky=W)
        ttk.Label(self.dlgframe, text="").grid(column=0, row=1, sticky=(E, W))    #Blank row
        tk.Button(self.dlgframe, text='Get rules file', command = self.set_rules).grid(column=0, row=2, sticky=W, pady=4)
        ttk.Label(self.dlgframe, textvariable=self.rule_path).grid(column=1, row=2, sticky=(W))

        ttk.Label(self.dlgframe, text="").grid(column=0, row=3, sticky=(E, W))    #Blank row
        tk.Button(self.dlgframe, text='Get text file', command = self.ProcessTextFile).grid(column=0, row=4, sticky=W, pady=4)
        tk.Button(self.dlgframe, text="Close", command=self.Close, width = 15).grid(column=1, row=4, sticky=(E, W))
        centerWindow(self.top)


    def set_rules(self):
        """
        This method load rule book to guide txt loading using PTagger
        """

        FILEOPENOPTIONS = dict(title='Choose rule book', initialfile='', filetypes=[('Comma Separated Values', ('.csv')), ('Text files', ('.txt')), ('All files', ('*.*'))])
        fhandle = filedialog.askopenfile(**FILEOPENOPTIONS)

        with open(fhandle.name, 'rt', encoding='utf8') as rulebook:
            tmpcontent = rulebook.readlines()
            csvReader = csv.reader(filter(lambda row:row[0]!='#', tmpcontent))
            self.rule = [row for row in csvReader]
            self.rule_path.set("Rule: "+fhandle.name)


    def ProcessTextFile(self):
        """
        This method runs when the button marked 'Get text file' is clicked
        """
        #Request name of file to open
        FILEOPENOPTIONS = dict(title='Choose a text file to import', initialfile = '', filetypes=[('Text files', ('.txt')), ('All files', ('*.*'))])
        fHandle = filedialog.askopenfile(**FILEOPENOPTIONS)

        #Get the encoding of the text file
        with open(fHandle.name, "rb") as binary_file:
            data = binary_file.read()
            soup = BeautifulSoup(data)

        #Read the file
        with open(fHandle.name, 'rt', encoding=soup.original_encoding) as f:
            content = f.readlines()
            content = [x.strip() for x in content]

        #Replace angular brackets if required
        if self.is_checked.get() == True:
            print("Changing brackets")
            content = [x.replace('<', '&lt;') for x in content]
            content = [x.replace('>', '&gt;') for x in content]

        """
        #Replace newlines with paragraph tags
        bodyText = bodyText.replace('\n', '</p>\n\n<p>').replace('\r', '')
        bodyText= bodyText.replace('<p></p>', '<p>&nbsp;</p>')
        """

        # use PTagger to tag new lines
        if self.rule is None:
            self.set_rules()

        tagger = PTagger(self.rule)
        content = tagger.tag(content)

        #Now write the xhtml file
        xml  = '<?xml version="1.0" encoding="utf-8"?>\n'
        xml += '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n\n'
        xml += '<html xmlns="http://www.w3.org/1999/xhtml">\n'
        xml += '<head>\n'
        xml += '<title></title>\n'
        xml += '</head>\n'
        xml += '<body>\n'
        for row in content:
            xml += row + '\n'
        xml += '</body>\n'
        xml += '</html>\n'

        #Set the name of the new xhtml section in the ePub to that of the filename
        Filename=fHandle.name
        head, fName = ntpath.split(fHandle.name)
        ChapterName = fName[:fName.index(".")] #Remove extension

        #Check whether this file already exists in the ePub
        for (id, href) in self.bk.text_iter():
            if id==ChapterName or href=='Text/'+ChapterName+ '.xhtml':    #If the section already exists
                reply=tkMessageBox.askquestion("WARNING", "Do you want to delete the current page named "+ ChapterName+".xhtml?")
                if reply=="yes":        #and it is not wanted
                    bk.deletefile(id)   #then delete it
                else:                   #otherwise do not import the text file
                    print("Present xhtml page has been retained.")
                    return

        #Add text file to ePub in a new xhtml section
        uid  = ChapterName
        basename = uid +'.xhtml'
        mime = 'application/xhtml+xml'
        self.bk.addfile(uid, basename, xml, mime)


    def Close(self):
        """
        Called when the user clicks the "Close" button
        It destroys the dialog window
        """
        self.prefs['ConvertAngularBrackets'] = self.is_checked.get()
        self.top.destroy()


def run(bk):
    root = tk.Tk()
    root.withdraw() #Hide

    #Check that version of Sigil is at least 0.9.1
    print('Python Laucher Version:', bk.launcher_version())
    if bk.launcher_version() < 20151024:
        print("You need to use Sigil 0.9.1 or greater for this plugin")
        print('\n\nPlease click OK to close the Plugin Runner window.')
        return 0        #....and return if Sigil is not greater than 0.9.1

    prefs = bk.getPrefs()
    prefs.defaults['ConvertAngularBrackets'] = True

    #TODO insert data below when published
    textImporterDialog = importTxtFile(root, bk, prefs) #Initialise instance of class
    root.wait_window(importTxtFile.dlgTop) #Wait until importTxtFile closes
    root.destroy()

    bk.savePrefs(prefs)

    print('\n\nPlease click OK to close the Plugin Runner window.')

    root.mainloop()

    return 0        #0 - means success, anything else means failure


def main():
    print ("This module should not be run as a stand-alone module")
    return -1

if __name__ == "__main__":
    sys.exit(main())
