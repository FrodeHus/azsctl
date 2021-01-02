import urwid
from azsctl.ui import signals


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
    def __init__(self):
        self.infobar = urwid.WidgetWrap(urwid.Text(""))
        self.actionbar = ActionBar()
        super().__init__(urwid.Pile([self.infobar, self.actionbar]))
