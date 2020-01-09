
from tkinter import *
from TkinterExtensionPack import OptFrame, MyDialog

import logging

log = logging.getLogger(__name__)


class ParamsWindow(MyDialog):

    def __init__(self, master, params, title=None, cols=1, defaults=None):
        self.params = params
        self.cols = cols
        self.defaults = defaults
        self.ents = {}

        self.choice = {}
        MyDialog.__init__(self, master, title)

    def body(self, root):

        nparams = len(self.params)
        params_per_col = int(nparams / self.cols + 0.5)

        for n, param in enumerate(self.params):

            try:
                default = self.defaults[param]
            except (TypeError, TclError):
                default = None

            w = OptFrame(root, self.params[param], title=str(param), default=default)
            w.grid(row=n % params_per_col, column=n // params_per_col, padx=2, pady=2, sticky=N)
            self.ents[param] = w

        return

    def applyit(self):

        self.result = {}
        self.choice = {}
        for param in self.params:
            self.result[param] = self.ents[param].get()
            self.choice[param] = self.ents[param].choice()


if __name__ == "__main__":
    import json

    logging.basicConfig(level=logging.DEBUG)

    roots = Tk()

    parameters = {
        'Modulation': {
            'QPSK': {'OSNR target (dB/0.1nm)': 15, 'Bit Rate (Gb/s)': 100, 'Format': 'QPSK'},
            '8QAM': {'OSNR target (dB/0.1nm)': 20.5, 'Bit Rate (Gb/s)': 150, 'Format': '8QAM'},
            '16QAM': {'OSNR target (dB/0.1nm)': 25, 'Bit Rate (Gb/s)': 200, 'Format': '16QAM'}
                        },
        'Repeater': {
            'R2.0 High Bandwidth': {'Noise Figure (dB)': 4, 'Bandwidth (nm)': 63, 'Output Power (dBm)': 17,
                                    'Max Gain (dB)': 14},
            'R1.0 High Bandwidth': {'Noise Figure (dB)': 4, 'Bandwidth (nm)': 55, 'Output Power (dBm)': 16,
                                    'Max Gain (dB)': 14},
            'R1.0 Low Noise': {'Noise Figure (dB)': 2.5, 'Bandwidth (nm)': 35, 'Output Power (dBm)': 16,
                               'Max Gain (dB)': 24}
                     },
        'Grid': {
            '100GHz': {'Spacing (GHz)': 100},
            '37.5GHz': {'Spacing (GHz)': 37.5},
            '50GHz': {'Spacing (GHz)': 50}
                  }
         }

    w1 = ParamsWindow(roots, parameters, cols=2)

    print(w1.choice)

    for p in w1.result:
        print(p)
        print(json.dumps(w1.result[p], indent=4))

    w1 = ParamsWindow(roots, parameters, cols=2, defaults=w1.result)

    print(w1.choice)

    for p in w1.result:
        print(p)
        print(json.dumps(w1.result[p], indent=4))

    mainloop()
