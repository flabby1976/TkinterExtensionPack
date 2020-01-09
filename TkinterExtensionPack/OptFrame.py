from tkinter import *

import logging

log = logging.getLogger(__name__)


class OptFrame(Frame):

    def __init__(self, parent, choices, title=None, default=None):

        Frame.__init__(self, parent)

        choices['Custom'] = {}

        self.default = default

        def _on_sel_change(*_):

            sel = self.selected.get()
            selected_choice = choices[sel]

            for my_parameter in self.all_parameters:
                self.ents[my_parameter].config(state=NORMAL)
                if not sel == 'Custom':
                    self.ents[my_parameter].delete(0, END)

            if not sel == 'Custom':
                self.types = {}
                for my_parameter in selected_choice:
                    self.ents[my_parameter].insert(0, selected_choice[my_parameter])
                    self.types[my_parameter] = type(selected_choice[my_parameter])
                    self.ents[my_parameter].config(state='readonly')

        chooser = Frame(self)
        chooser.pack()

        selectable_options = []
        self.all_parameters = []
        for choice in choices:
            selectable_options.append(choice)
            for parameter in choices[choice]:
                if parameter not in self.all_parameters:
                    self.all_parameters.append(parameter)

        self.selected = StringVar(chooser)
        self.selected.trace("w", _on_sel_change)

        Label(chooser, text=title, font="bold", bg="grey").grid(row=1, column=1, sticky=E)
        OptionMenu(chooser, self.selected, *selectable_options).grid(row=1, column=2, padx=2, pady=2, sticky=W)

        self.ents = {}
        self.types = {}
        for grid_row, parameter in enumerate(self.all_parameters):
            Label(chooser, text=str(parameter), anchor=E).grid(row=grid_row + 2, column=1, padx=2, pady=2, sticky=E)
            e = Entry(chooser)
            e.config(state='readonly')
            e.grid(row=grid_row + 2, column=2, padx=2, pady=2, sticky=W)
            self.ents[parameter] = e

        self.selected.set(selectable_options[0])  # initial value if we weren't given a default
        if default:
            found = False
            for test in choices:
                if not test == 'Custom':
                    mismatch = False
                    for par in choices[test]:
                        if not choices[test][par] == default[par]:
                            mismatch = True
                            break  # stop looking at this test in choices
                    if mismatch:
                        continue  # go to next test in choices
                    else:
                        self.selected.set(test)  # if all par in choices[test] matched then this is the default
                        found = True
                        break  # if found stop looking through tests in choices

            if not found:  # if not found after going through all selectable_options, must be 'Custom'
                for parameter in default:
                    e = self.ents[parameter]
                    v = default[parameter]
                    e.config(state=NORMAL)
                    e.delete(0, END)
                    e.insert(0, v)
                    self.types[parameter] = type(v)
                self.selected.set('Custom')

    def get(self):

        vals = {}
        for parameter in self.all_parameters:
            v = self.ents[parameter].get()
            if self.types[parameter]:
                if self.types[parameter] == int:
                    vals[parameter] = int(v)
                    continue
                if self.types[parameter] == float:
                    vals[parameter] = float(v)
                    continue
                vals[parameter] = v

        return vals

    def choice(self):

        vals = {}
        if self.selected.get() == "Custom":
            for parameter in self.all_parameters:
                v = self.ents[parameter].get()
                if self.types[parameter]:
                    if self.types[parameter] == int:
                        vals[parameter] = int(v)
                        continue
                    if self.types[parameter] == float:
                        vals[parameter] = float(v)
                        continue
                    vals[parameter] = v

        return self.selected.get(), vals


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    root = Tk()

    my_choices = {
        'QPSK': {'OSNR target (dB/0.1nm)': 15, 'Bit Rate (Gb/s)': 100, 'Format': 'QPSK'},
        '8QAM': {'OSNR target (dB/0.1nm)': 20.5, 'Bit Rate (Gb/s)': 150, 'Format': '8QAM'},
        '16QAM': {'OSNR target (dB/0.1nm)': 25, 'Bit Rate (Gb/s)': 200, 'Format': '16QAM'}
        }

    w = OptFrame(root, my_choices, title="Modulation")
    w.pack()

    mainloop()
