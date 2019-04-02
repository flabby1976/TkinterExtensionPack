##    My module of tkinter based stuff
##
##    This file is part of TkinterExtensionPack
##    Copyright (C) 2017,2018, 2019 Andrew Robinson
##
##    TkinterExtensionPack is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    TkinterExtensionPack is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with TkinterExtensionPack.  If not, see <https://www.gnu.org/licenses/>.
##
from __future__ import division

from Tkinter import *

import logging
log = logging.getLogger(__name__)

class MyTable(Toplevel):

    def __init__(self, parent, rows, cols, title = None, initial_values=None, col_width=None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.rows = rows
        self.cols = cols

        self.col_width = col_width

        self.initial_values = initial_values

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)


    def body(self, master):

        for grid_col, head in enumerate(self.cols):
            Label(master, text=head).grid(row=0,column=grid_col+2)

        self.ents={}
        for grid_row, item in enumerate(self.rows):
            sroot = str(item)
            l = Label(master, text = sroot, anchor=E)
            l.grid(row = grid_row+1, column = 1, padx = 2, pady = 2, sticky = E)
            self.ents[item]={}
            for grid_col, head in enumerate(self.cols):
                e = Entry(master, width=self.col_width)
                e.grid(row = grid_row+1, column = grid_col+2, padx = 2, pady = 2, sticky = W)
                self.ents[item][head]=e

        if self.initial_values:
            for row in self.initial_values:
                if row in self.rows:
                    for col in self.initial_values[row]:
                        if col in self.cols:
                            self.ents[row][col].insert(0, self.initial_values[row][col])
                        else:
                            log.warning("Warning: initial_value key '%s' not found in %s" % (col, self.cols))
                else:
                    log.warning("Warning: initial_value key '%s' not found in %s" % (row, self.rows))

        return 

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.applyit()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        # Override if need to validate inputs before apply to result

        return 1


    def applyit(self):

        self.result={}
        for item in self.rows:
            self.result[item]={}
            for head in self.cols:
                val = self.ents[item][head].get()
                self.result[item][head]=val                      

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    root=Tk()

    class popupWindow(MyTable):

        def validate(self):
            for item in self.rows:
                for head in self.cols:
                    val = self.ents[item][head].get()
                    if not val == "":
                        try:
                            valf = float(val)
                        except ValueError:
                            tkMessageBox.showwarning(
                                "Bad input",
                                "Illegal value:\n '%s' '%s' '%s'\n Please try again" % (item, head, val)
                            )
                            return 0
            return 1
            

    cols = ["dB", "dB/km"]
    rows = ["LW", "LWP", "SA"]

    init = { u'DA': {'dB/km': 0.183}, u'SA': {'dB/km': 0.183}, u'LWP': {'dB/km': 0.183}, u'LW': {'dB/km': 0.183}}

    w = popupWindow(root, rows, cols, initial_values = init, title = "Set losses", col_width=5)

    log.debug("Result: %s" % w.result)

    mainloop()
