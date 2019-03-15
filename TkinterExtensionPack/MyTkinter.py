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

# Class for scrollable, zoomable canvas
# based on https://stackoverflow.com/questions/25787523/move-and-zoom-a-tkinter-canvas-with-mouse
#
class MyCanvas(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent=parent
        
        self.canvas = Canvas(self, width=400, height=400, background="bisque", closeenough=5)
        self.xsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
#        self.canvas.configure(scrollregion=(0,0,1000,1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # mousewheel only binds to the parent window,
        # which is bad if there are other widgets in the parent window
        # and we only want the mousewheel to work in the canvas.
        # So bind and unbind as mouse goes in and out of the canvas widget.
        #
        # May as well do same for the other mouse events (i.e. bind to parent)
        # so one can bind canvas events to these mousekeys elsewhere without conflict.
        self.canvas.bind("<Enter>", self._bind_events)
        self.canvas.bind("<Leave>", self._unbind_events)

        self.select_mark = None
        self.selectbox = None
        self.selectlist = []
        
        self.clear()        

    def trans(self, (x, y)):
        """ Transform from 'real' coords to 'canvas' coords """
        x1 = x*self.xscale + self.xoffset
        y1 = -y*self.yscale + self.yoffset
        return (x1, y1)

    def rtrans(self, (x, y)):
        """ Transform from 'canvas' coords to 'real' coords """
        x1 = (x-self.xoffset)/self.xscale
        y1 = -(y-self.yoffset)/self.yscale
        return (x1, y1)

    def _bind_events(self,event):
        self.parent.bind("<Control-MouseWheel>",self.zoomer)
        self.parent.bind("<Control-ButtonPress-1>", self.drag_start)
        self.parent.bind("<Control-B1-Motion>", self.drag_drag)
        self.parent.bind("<Control-ButtonRelease-1>", self.drag_stop)

        self.parent.bind("<Motion>", self.motion)

        self.parent.bind("<ButtonPress-1>", self.select_start)
        self.parent.bind("<Shift-ButtonPress-1>", self.shift_select_start)
        self.parent.bind("<B1-Motion>", self.select_drag)
        self.parent.bind("<ButtonRelease-1>", self.select_stop)

        
    def _unbind_events(self,event):
        self.parent.unbind("<Control-MouseWheel>")
        self.parent.unbind("<ButtonPress-1>")
        self.parent.unbind("<B1-Motion>")
        self.parent.unbind("<ButtonRelease-1>")
        self.parent.unbind("<Motion>")

        self.parent.unbind("<Control-ButtonPress-1>")
        self.parent.unbind("<Control-B1-Motion>")
        self.parent.unbind("<Control-ButtonRelease-1>")
    

    def motion(self,event):
        self.mousex = (self.canvas.canvasx(event.x)-self.xoffset)/self.xscale
        self.mousey = -(self.canvas.canvasy(event.y)-self.yoffset)/self.yscale
        p = ("Mouse position: (%s %s)" ) % (self.mousex, self.mousey)
        self.canvas.delete(self.coord)
        self.coord=self.canvas.create_text(self.canvas.canvasx(0),self.canvas.canvasy(0),anchor=NW, text=p)

    def drag_start(self, event):
        self.canvas.delete(self.coord)
        self.canvas.scan_mark(event.x, event.y)
        self.canvas.config(cursor="hand1")

    def drag_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def drag_stop(self, event):
        self.mousex = (self.canvas.canvasx(event.x)-self.xoffset)/self.xscale
        self.mousey = -(self.canvas.canvasy(event.y)-self.yoffset)/self.yscale
        p = ("Mouse position: (%s %s)" ) % (self.mousex, self.mousey)
        self.coord=self.canvas.create_text(self.canvas.canvasx(0),self.canvas.canvasy(0),anchor=NW, text=p)
        self.canvas.config(cursor="") 

    def shift_select_start(self, event):
        log.debug("Starting Selection")
        self.selectlist.extend(self.canvas.find_withtag(CURRENT))
        log.debug(self.selectlist)
        self.select_mark=(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        (x0,y0)=self.select_mark
        self.selectbox = self.canvas.create_rectangle(x0,y0,self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def select_start(self, event):
        self.selectlist=[]
        log.debug("Starting Selection")
        self.selectlist.extend(self.canvas.find_withtag(CURRENT))
        log.debug(self.selectlist)
        self.select_mark=(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        (x0,y0)=self.select_mark
        self.selectbox = self.canvas.create_rectangle(x0,y0,self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def select_drag(self, event):
        (x0,y0)=self.select_mark
        self.canvas.coords(self.selectbox, x0,y0,self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        
    def select_stop(self, event):
        log.debug("Finished Selection")
        a=self.canvas.coords(self.selectbox)
        if not a == []:
            (x0,y0,x1,y1) = self.canvas.coords(self.selectbox)
            self.selectlist.extend(self.canvas.find_enclosed(x0,y0,x1,y1))
            self.canvas.delete(self.selectbox)
        log.debug(self.selectlist)
        self.event_generate("<<Selection_Change>>")

    def zoomer(self,event):
        self.canvas.delete(self.coord)
        if (event.delta > 0):
            self.canvas.scale("all", self.canvas.canvasx(event.x), self.canvas.canvasy(event.y), 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", self.canvas.canvasx(event.x), self.canvas.canvasy(event.y), 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

        (x0,y0,x1,y1)= self.canvas.coords(self.scalebox)

        self.xoffset=x0
        self.yoffset=y0
        self.xscale=(x1-x0)/10
        self.yscale=(y1-y0)/10

    def autozoom(self,tag):

        old_w = self.canvas.winfo_width()
        old_h = self.canvas.winfo_height()

        (x0,y0,x1,y1)= self.canvas.bbox(tag)

        new_w = x1-x0
        new_h = y1-y0

        orig_x = self.canvas.canvasx(0)
        orig_y = self.canvas.canvasy(0)

        x_off = orig_x-x0
        y_off = orig_y-y0

        self.canvas.move("all", x_off, y_off)
       
        scaleh = old_h/new_h
        scalew = old_w/new_w
        scale = min(scaleh, scalew)

        self.canvas.scale("all", orig_x, orig_y, scale, scale)

#        self.canvas.configure(scrollregion = self.canvas.bbox(tag))

        (x0,y0,x1,y1)= self.canvas.coords(self.scalebox)

        self.xoffset=x0
        self.yoffset=y0
        self.xscale=(x1-x0)/10
        self.yscale=(y1-y0)/10


    def clear(self):
        self.canvas.delete(ALL)
        
        self.xoffset=0.0
        self.yoffset=0.0
        self.xscale=1
        self.yscale=1
        self.mousex = (self.canvas.canvasx(0)-self.xoffset)/self.xscale
        self.mousey = -(self.canvas.canvasy(0)-self.yoffset)/self.yscale
        p = ("Mouse position: (%s %s)" ) % (self.mousex, self.mousey)
        self.coord=self.canvas.create_text(self.canvas.canvasx(0),self.canvas.canvasy(0),anchor=NW, text=p)
        self.scalebox=self.canvas.create_rectangle(0,0,10,10, outline="black", fill="black", tags="scalebox", state=HIDDEN)

    def create_arc(self, x0, y0, x1, y1, *args, **kwargs):
        (x0, y0) = self.trans((x0,y0))
        (x1, y1) = self.trans((x1,y1))
        return self.canvas.create_arc(x0, y0, x1, y1, *args, **kwargs)

    def create_bitmap(self, x0, y0, *args, **kwargs):
        (x0, y0) = self.trans((x0,y0))
        return self.canvas.create_bitmap(x0, y0, *args, **kwargs)
    
    def create_image(self, x0, y0, *args, **kwargs):
        (x0, y0) = self.trans((x0,y0))
        return self.canvas.create_image(x0, y0, *args, **kwargs)
    
    def create_line(self, x0, y0, x1, y1, *args, **kwargs):
        (x0, y0) = self.trans((x0,y0))
        (x1, y1) = self.trans((x1,y1))
        return self.canvas.create_line(x0, y0, x1, y1, *args, **kwargs)

    def create_oval(self, x0, y0, x1, y1, *args, **kwargs):
        (x0, y0) = self.trans((x0,y0))
        (x1, y1) = self.trans((x1,y1))
        return self.canvas.create_oval(x0, y0, x1, y1, *args, **kwargs)

    def create_rectangle(self, x0, y0, x1, y1, *args, **kwargs):
        (x0, y0) = self.trans((x0,y0))
        (x1, y1) = self.trans((x1,y1))
        return self.canvas.create_rectangle((x0, y0, x1, y1), *args, **kwargs)

    def create_text(self, x0, y0, *args, **kwargs):
        (x0, y0) = self.trans((x0,y0))
        return self.canvas.create_text(x0, y0, *args, **kwargs)
    
    def create_window(self, x0, y0, *args, **kwargs):
        (x0, y0) = self.trans((x0,y0))
        return self.canvas.create_window(x0, y0, *args, **kwargs)

    def coords(self, *args):
        (x,y) = self.canvas.coords(*args)       
        (x1, y1) = self.rtrans((x,y))
        return (x1, y1)


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
#        self.widget.config(state='normal')
        # Append message (record) to the widget
        self.widget.insert(END, self.format(record) + '\n', record.levelname)
        self.widget.see(END)  # Scroll to the bottom
#        self.widget.config(state='disabled') 
        self.widget.update() # Refresh the widget

if __name__ == "__main__":

    import random
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG)

    root = Tk()

    GUI = MyCanvas(root)

    GUI.pack(side=LEFT, fill=BOTH, expand=1)

    #Need an update() after pack so that window size is recognised for autozoom() to work
    GUI.update()

    minsize, maxsize = 5, 20
    for n in range(5):
        x0 = random.randint(0, maxsize)
        y0 = random.randint(0, maxsize)
        x1 = x0 + random.randint(minsize, maxsize)
        y1 = y0 + random.randint(minsize, maxsize)

        print n, ": ", x0, y0, x1, y1

        color = ('red', 'orange', 'yellow', 'green', 'blue')[random.randint(0, 4)]
        GUI.create_rectangle(x0, y0, x1, y1, outline='black', fill=color,
                                     activefill='black', tags="squares")

    GUI.autozoom("squares")

    for n in range(5):
        x0 = random.randint(0, maxsize)
        y0 = random.randint(0, maxsize)
        x1 = x0 + random.randint(minsize, maxsize)
        y1 = y0 + random.randint(minsize, maxsize)

        print n, ": ", x0, y0, x1, y1

        color = ('red', 'orange', 'yellow', 'green', 'blue')[random.randint(0, 4)]
        GUI.create_rectangle(x0, y0, x1, y1, outline='black', fill=color,
                                     activefill='black', tags="squares")

        
    GUI.autozoom("squares")

    mainloop()


    
