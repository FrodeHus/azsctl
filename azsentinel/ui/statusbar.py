import urwid
from azsentinel.ui import signals
from azsentinel import current_config
from azsentinel.auth import TokenRequester

class CommandPrompt(urwid.Edit):
    def keypress(self, size, key):
        if key == "enter":
            signals.focus.send(section="body")
            signals.execute.send(command=self.text)
        super().keypress(size, key)
class ActionBar(urwid.WidgetWrap):
    def __init__(self):
        urwid.WidgetWrap.__init__(self, None)
        self.clear()
        self.active_prompt = False
        signals.status_message.connect(self.signal_message)
        signals.action_command.connect(self.signal_command)
        signals.execute.connect(self.signal_execute)        

    def signal_command(self, sender, cmd):
        self.active_prompt = True
        signals.focus.send(section="footer")
        widget = CommandPrompt(': ')
        self._w = widget

    def signal_execute(self, sender, command):
        self.active_prompt = False
        signals.status_message.send(message="executing: " + command, expire=4)

    def signal_message(self, sender, message, expire=1):
        if self.active_prompt:
            return
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

    def __init__(self, actions = []):
        self.infobar = urwid.WidgetWrap(urwid.Text(""))
        self.actionbar = ActionBar()
        self.build_action_widgets(actions)
        self.current_user, _ = TokenRequester().get_current_user()
        super().__init__(urwid.Pile([self.infobar, self.actionbar]))
        self.refresh()
    
    def refresh(self):
        self.redraw()
        signals.delayed_signal.send(seconds=self.REFRESH_TIME, callback=self.refresh)
    
    def redraw(self):
        workspace,_ = current_config.get_workspace()
        status = urwid.AttrWrap(urwid.Columns([
            self.actions,
            urwid.Text(workspace, align="right"),
        ]), "heading")
        self.infobar._w = status

    def build_action_widgets(self, actions):
        action_widgets = []
        for action in actions:
            w = urwid.Text([('important',action[0])," ", action[1]])
            w = urwid.Padding(w, align="center")
            w = urwid.AttrMap(w, 'actionbar:action')
            action_widgets.append(w)
        
        self.actions = urwid.Columns(action_widgets, dividechars=1)