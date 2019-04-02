
from Tkinter import *

import logging
log = logging.getLogger(__name__)

class OptFrame(Frame):

    def __init__(self, parent, conf, title = None):

        Frame.__init__(self, parent)

        def _OnSelChange(name, index, mode):
            sel = selected.get()
            pars = conf[sel]

            for par in self.paras:
                self.ents[par].delete(0, END)
                
            for par in pars:
                self.ents[par].insert(0, pars[par])

        chooser = Frame(self)
        chooser.pack()

        opts=[]
        self.paras=[]
        for opt in conf:
            opts.append(opt)
            for para in conf[opt]:
                if not para in self.paras:
                    self.paras.append(para)

##        log.debug(opts)
##        log.debug(self.paras)

        selected = StringVar(chooser)
        selected.trace("w", _OnSelChange)

        Label(chooser, text=title, font="bold", bg="grey").grid(row=1,column=1, sticky=E)
        OptionMenu(chooser, selected, *opts).grid(row=1,column=2, padx = 2, pady = 2, sticky=W)

        self.ents={}
        for grid_row, para in enumerate(self.paras):
            Label(chooser, text=str(para), anchor=E).grid(row = grid_row+2, column = 1, padx = 2, pady = 2, sticky = E)
            e = Entry(chooser)
            e.grid(row = grid_row+2, column = 2, padx = 2, pady = 2, sticky = W)
            self.ents[para]=e

        selected.set(opts[0]) # initial value


    def get(self):

        vals = {}
        for para in self.paras:
            vals[para] = self.ents[para].get()

        return vals

if __name__ == "__main__":

    import json

    logging.basicConfig(level=logging.DEBUG)

    root=Tk()

    parameters = { \
        u'QPSK': {u'OSNR target (dB/0.1nm)': 15, u'Bit Rate (Gb/s)': 100, u'Format': u'QPSK'}, \
        u'8QAM': {u'OSNR target (dB/0.1nm)': 20.5, u'Bit Rate (Gb/s)': 150, u'Format': u'8QAM'}, \
        u'16QAM': {u'OSNR target (dB/0.1nm)': 25, u'Bit Rate (Gb/s)': 200, u'Format': u'16QAM'} \
        }

    w = OptFrame(root, parameters, title="Modulation")
    w.pack()

    mainloop()



