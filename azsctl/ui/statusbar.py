import urwid
from azsctl.ui import signals

class ActionBar(urwid.WidgetWrap):
    def __init__(self):
        urwid.WidgetWrap.__init__(self, None)
        self.clear()
        signals.status_message.connect(self.signal_message)
        self.prompting = None

    def signal_message(self, sender, message, expire=1):
        self._w = urwid.Text(message)
    
    def selectable(self):
        return True
    
    def clear(self):
        self._w = urwid.Text("")
        self.prompting = None
class StatusBar(urwid.WidgetWrap):
    def __init__(self):
        self.infobar = urwid.WidgetWrap(urwid.Text(""))
        self.actionbar = ActionBar()
        super().__init__(urwid.Pile([self.infobar, self.actionbar]))
        