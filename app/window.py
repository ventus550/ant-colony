from tkinter import Canvas, Tk, NW
from params import palette, geometry, block, message
from mytypes import Coords


def coords(xy: Coords) -> Coords:
    "Calculate block coordinates from the pixel ones."
    x, y = xy
    return x * block, y * block


class Ctx(Canvas):
    "Tkinter UI element responsible to draw various shapes and objects."

    def __init__(self, parent, x, y, wh, ht):
        Canvas.__init__(self, parent, width=wh, height=ht, bd=5,
                        background=palette[1], highlightbackground=palette[1])
        self.place(x=x, y=y)
        self.update()
        self.side = self.winfo_width()
        self.parent = parent

    def box(self, xy: Coords, size: int = 1, color: str = "white", **kwargs) -> None:
        "Draw a box."
        x, y = coords(xy)
        size *= block
        self.create_rectangle(x, y, x+size, y+size, outline=color, **kwargs)

    def point(self, xy: Coords, color: str = "white") -> None:
        "Draw a point."
        x, y = coords(xy)
        s = block * 0.6
        self.create_rectangle(x, y, x+s, y+s, outline='',
                              fill=color, stipple='gray25')

    def circle(self, xy: Coords, r: int = 2, color: str = "white", **kwargs) -> None:
        "Draw a circle."
        x, y = coords(xy)
        r *= block
        self.create_oval(x-r, y-r, x+r, y+r, fill=color, outline='', **kwargs)
        self.create_oval(x-r-10, y-r-10, x+r+10, y+r+10, outline=color)

    def message(self) -> None:
        "Print a message."
        self.create_text(50, 20, anchor=NW, text=message,
                         fill=palette[2], font=('Helvetica 12 bold'))

    def clear(self) -> None:
        "Wipe the canvas clean."
        self.update()
        self.delete('all')


class Window(Tk):
    "Main application window"

    def __init__(self):
        Tk.__init__(self)
        size = geometry*block
        self.title("Ant Colony")
        self['bg'] = palette[0]
        self['width'] = size
        self['height'] = size
        self.ctx = Ctx(self, 0, 0, size, size)
        self.update()
