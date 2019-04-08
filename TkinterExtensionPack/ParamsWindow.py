
from Tkinter import *
from TkinterExtensionPack import OptFrame, MyDialog

import logging
log = logging.getLogger(__name__)

class ParamsWindow(MyDialog):

    def __init__(self, master, params, title=None, cols=1):
        self.params=params
        self.cols=cols
        MyDialog.__init__(self, master, title)

    def body(self, root):

        Nparams=len(self.params)
        params_per_col = Nparams // self.cols

        self.ents={}
        for n, param in enumerate(self.params):
            w = OptFrame(root, self.params[param], title=str(param))
            w.grid(row=n % params_per_col, column= n // params_per_col, padx = 2, pady = 2, sticky = N)
            self.ents[param]=w
        return

    def applyit(self):

        self.result={}
        for n, param in enumerate(self.params):
            self.result[param] = self.ents[param].get()
            

if __name__ == "__main__":

    import json

    logging.basicConfig(level=logging.DEBUG)

    root=Tk()

    parameters = \
       {u'Modulation': \
                {u'QPSK': {u'OSNR target (dB/0.1nm)': 15, u'Bit Rate (Gb/s)': 100, u'Format': u'QPSK'}, \
                 u'8QAM': {u'OSNR target (dB/0.1nm)': 20.5, u'Bit Rate (Gb/s)': 150, u'Format': u'8QAM'}, \
                 u'16QAM': {u'OSNR target (dB/0.1nm)': 25, u'Bit Rate (Gb/s)': 200, u'Format': u'16QAM'} \
                 }, \
        u'Fibre': \
                {u'Standard': {u'Effective Area (um)': 80, u'Dispersion (ps/nm/km)': 18, u'Loss (dB/km)': 0.183}, \
                 u'Low Loss': {u'Effective Area (um)': 80, u'Dispersion (ps/nm/km)': 18, u'Loss (dB/km)': 0.17}, \
                 u'Ultra Low Loss': {u'Effective Area (um)': 110, u'Dispersion (ps/nm/km)': 18, u'Loss (dB/km)': 0.156} \
                 }, \
        u'Repeater':
                {u'R2.0 High Bandwidth': {u'Noise Figure (dB)': 4, u'Bandwidth (nm)': 63, u'Output Power (dBm)': 17, u'Max Gain (dB)': 14}, \
                 u'R1.0 High Bandwidth': {u'Noise Figure (dB)': 4, u'Bandwidth (nm)': 55, u'Output Power (dBm)': 16, u'Max Gain (dB)': 14}, \
                 u'R1.0 Low Noise': {u'Noise Figure (dB)': 2.5, u'Bandwidth (nm)': 35, u'Output Power (dBm)': 16, u'Max Gain (dB)': 24} \
                 }, \
        u'Grid': {u'100GHz': {u'Spacing (GHz)': 100}, \
                  u'37.5GHz': {u'Spacing (GHz)': 37.5}, \
                  u'50GHz': {u'Spacing (GHz)': 50} \
                  } \
        }

    w = ParamsWindow(root, parameters, cols=2)

    print json.dumps(w.result, indent=4)

    mainloop()
