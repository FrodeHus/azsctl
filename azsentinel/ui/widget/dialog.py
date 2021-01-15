import urwid


class Dialog(urwid.Overlay):
    SIGNAL_DIALOG_CLOSED = "dialog_closed"

    def __init__(self, dialog_widget, parent_widget):
        urwid.register_signal(self.__class__, [Dialog.SIGNAL_DIALOG_CLOSED])
        super().__init__(
            dialog_widget, parent_widget, "center", width=('relative', 60), valign="middle", height=('relative', 60)
        )

    def keypress(self, size, key):
        if key in ('esc', 'q'):
            urwid.emit_signal(self, Dialog.SIGNAL_DIALOG_CLOSED)
        else:
            return super().keypress(size, key)
