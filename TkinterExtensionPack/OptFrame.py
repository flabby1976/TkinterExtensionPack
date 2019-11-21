from Tkinter import *

import logging

log = logging.getLogger(__name__)


class OptFrame(Frame):

    def __init__(self, parent, conf, title=None, default=None):

        Frame.__init__(self, parent)

        conf['Custom'] = {}

        # print conf

        self.default = default

        def _on_sel_change(*_):

            sel = self.selected.get()
            pars = conf[sel]

            for par in self.paras:
                self.ents[par].config(state=NORMAL)
                if not sel == 'Custom':
                    self.ents[par].delete(0, END)

            if not sel == 'Custom':
                for par in pars:
                    self.ents[par].insert(0, pars[par])
                    self.ents[par].config(state='readonly')

        chooser = Frame(self)
        chooser.pack()

        opts = []
        self.paras = []
        for opt in conf:
            opts.append(opt)
            for para in conf[opt]:
                if para not in self.paras:
                    self.paras.append(para)

        self.selected = StringVar(chooser)
        self.selected.trace("w", _on_sel_change)

        Label(chooser, text=title, font="bold", bg="grey").grid(row=1, column=1, sticky=E)
        OptionMenu(chooser, self.selected, *opts).grid(row=1, column=2, padx=2, pady=2, sticky=W)

        self.ents = {}
        for grid_row, para in enumerate(self.paras):
            Label(chooser, text=str(para), anchor=E).grid(row=grid_row + 2, column=1, padx=2, pady=2, sticky=E)
            e = Entry(chooser)
            e.config(state='readonly')
            e.grid(row=grid_row + 2, column=2, padx=2, pady=2, sticky=W)
            self.ents[para] = e

        self.selected.set(opts[0])  # initial value
        if default:
            self.selected.set(default[0])  # initial value
            if default[0] == "Custom":
                for para in default[1]:
                    e = self.ents[para]
                    e.delete(0, END)
                    e.insert(0, default[1][para])

    def get(self):

        vals = {}
        for para in self.paras:
            vals[para] = self.ents[para].get()

        return vals

    def choice(self):

        vals = {}
        if self.selected.get() == "Custom":
            for para in self.paras:
                vals[para] = self.ents[para].get()

        return self.selected.get(), vals


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    root = Tk()

    choices = {
        u'QPSK': {u'OSNR target (dB/0.1nm)': 15, u'Bit Rate (Gb/s)': 100, u'Format': u'QPSK'},
        u'8QAM': {u'OSNR target (dB/0.1nm)': 20.5, u'Bit Rate (Gb/s)': 150, u'Format': u'8QAM'},
        u'16QAM': {u'OSNR target (dB/0.1nm)': 25, u'Bit Rate (Gb/s)': 200, u'Format': u'16QAM'}
        }

    w = OptFrame(root, choices, title="Modulation")
    w.pack()

    mainloop()
