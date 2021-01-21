import urwid


class Dialog(urwid.Overlay):
    SIGNAL_DIALOG_CLOSED = "dialog_closed"    

    def __init__(self, dialog_widget, parent_widget, signals : list):
        _signals = [Dialog.SIGNAL_DIALOG_CLOSED]
        if signals:
            _signals.extend(signals)
        urwid.register_signal(self.__class__, _signals)
        super().__init__(
            dialog_widget, parent_widget, "center", width=('relative', 60), valign="middle", height=('relative', 60)
        )

    def keypress(self, size, key):
        if key == 'esc' or key == 'q':
            urwid.emit_signal(self, Dialog.SIGNAL_DIALOG_CLOSED)
        else:
            return super().keypress(size, key)

class OptionsDialog(Dialog):
    SIGNAL_OPTION_SELECTED = "option_selected"
    def __init__(self, title, options, parent_widget):
        
        super().__init__(dialog_widget, parent_widget, [OptionsDialog.SIGNAL_OPTION_SELECTED])

class QueryEditor(Dialog):
    SIGNAL_EXECUTE = "query_execute"

    def __init__(self, query : str, parent_widget):
        self._edit = urwid.Edit(edit_text=query, multiline=True)
        view = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker([self._edit])),title="Edit rule query")
        super().__init__(view, parent_widget, [QueryEditor.SIGNAL_EXECUTE])

    def keypress(self, size, key):
        if key == "f10":
            urwid.emit_signal(self, QueryEditor.SIGNAL_EXECUTE, self._edit.get_edit_text())
        else:
            return super().keypress(size, key)