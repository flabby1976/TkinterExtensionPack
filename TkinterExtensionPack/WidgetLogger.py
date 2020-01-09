#    My module of tkinter based stuff
#
#    This file is part of TkinterExtensionPack
#    Copyright (C) 2017,2018, 2019 Andrew Robinson
#
#    TkinterExtensionPack is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TkinterExtensionPack is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TkinterExtensionPack.  If not, see <https://www.gnu.org/licenses/>.
#


from tkinter import *

import logging
log = logging.getLogger(__name__)


class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
#        self.setLevel(logging.INFO)
        self.widget = widget
#        self.widget.config(state='disabled')

        self.widget.tag_config("INFO", foreground="black")
        self.widget.tag_config("DEBUG", foreground="grey")
        self.widget.tag_config("WARNING", foreground="orange")
        self.widget.tag_config("ERROR", foreground="red")
        self.widget.tag_config("CRITICAL", foreground="red", underline=1)

    def emit(self, record):
        # self.widget.config(state='normal')
        # Append message (record) to the widget
        self.widget.insert(END, self.format(record) + '\n', record.levelname)
        self.widget.see(END)  # Scroll to the bottom
#        self.widget.config(state='disabled') 
        self.widget.update()  # Refresh the widget


if __name__ == "__main__":

    debug = Tk()

    debug.title("Logging window")
    t1 = Text(debug)
    t1.pack(side=LEFT, fill=Y)
    
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    # create handler
    logging_handler = WidgetLogger(t1)

    # create formatter
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")

    # add formatter to handler
    logging_handler.setFormatter(formatter)

    # Add the handler to logger
    log.addHandler(logging_handler)

    # Go for it!
    log.info("Hello")  # will print a message to the logger
    log.debug('Go for it!')

    mainloop()
