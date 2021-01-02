import urwid
from azsctl.ui import signals
from azsctl import current_config

class ActionBar(urwid.WidgetWrap):
    def __init__(self):
        urwid.WidgetWrap.__init__(self, None)
        self.clear()
        signals.status_message.connect(self.signal_message)

    def signal_message(self, sender, message, expire=1):
        widget = urwid.Text(message)
        self._w = widget

        if expire:

            def cb(*args):
                if self._w == widget:
                    self.clear()

            signals.delayed_signal.send(seconds=expire, callback=cb)

    def selectable(self):
        return True

    def clear(self):
        self._w = urwid.Text("")


class StatusBar(urwid.WidgetWrap):
    REFRESH_TIME = 0.5 

    def __init__(self):
        self.infobar = urwid.WidgetWrap(urwid.Text(""))
        self.actionbar = ActionBar()
        super().__init__(urwid.Pile([self.infobar, self.actionbar]))
        self.refresh()
    
    def refresh(self):
        self.redraw()
        signals.delayed_signal.send(seconds=self.REFRESH_TIME, callback=self.refresh)
    
    def redraw(self):
        workspace,_ = current_config.get_workspace()
        status = urwid.AttrWrap(urwid.Columns([
            urwid.Text(""),
            urwid.Text(workspace, align="right"),
        ]), "heading")
        self.infobar._w = status
