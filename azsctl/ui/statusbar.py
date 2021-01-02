import urwid

class StatusBar(urwid.WidgetWrap):
    def __init__(self):
        self.infobar = urwid.WidgetWrap(urwid.Text(""))
        super().__init__(urwid.Pile([self.infobar]))
        