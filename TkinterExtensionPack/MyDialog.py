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


# Class for pop-up dialog boxes
# from http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
#

class MyDialog(Toplevel):

    def __init__(self, parent, title = None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

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

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

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

        return 1 # override

    def applyit(self):

        pass # override

if __name__ == "__main__":

    import tkMessageBox
    class popupWindow(MyDialog):

        def body(self, master):

            self.seg_name_list=["A", "B", "C"]


            label3 = Label(master, text="Segment").grid(row=0,column=0)
            self.var = StringVar(master)
            self.var.set(self.seg_name_list[0]) # initial value

            option=OptionMenu(master, self.var, *self.seg_name_list)

            label1 = Label( master, text="Name").grid(row=1,column=0)
            self.E1 = Entry(master)

            label2 = Label( master, text="Distance").grid(row=2,column=0)
            self.E2 = Entry(master)
            
            option.grid(row=0,column=1)
            self.E1.grid(row=1, column=1)
            self.E2.grid(row=2, column=1)
            
            return self.E1 # initial focus

        def validate(self):
            try:
                my_seg_name = self.var.get()
                my_entry_name = self.E1.get()
                my_distance = self.E2.get()

                self.result=(my_seg_name, my_entry_name, float(my_distance))
                return 1
            except ValueError:
                tkMessageBox.showwarning(
                    "Bad input",
                    "Illegal values, please try again"
                )
            return 0

    logging.basicConfig(level=logging.DEBUG)

    root=Tk()

    w=popupWindow(root, title="Insert RPL Event")

    try:
        (my_seg, my_entry_name, my_distance) = w.result
    except TypeError:
        # This probably means that Cancel was pressed (w.result = None)
        pass

    log.debug("%s %s %s" % (my_seg, my_entry_name, my_distance))

    mainloop()
