import urwid

class TabItem:
    def __init__(self, label, widget):
        self.label = label
        self.widget = widget

class Tab(urwid.WidgetWrap):
    def __init__(self, offset, label, attr, onclick):
        w = urwid.Text(label, align="center")
        w = urwid.Padding(w, align="center")
        w = urwid.AttrMap(w, attr)
        urwid.WidgetWrap.__init__(self, w)
        self.tab_offset = offset
        self.onclick = onclick

    def mouse_event(self, size, event, button, col, row, focus):
        if event == "mouse" and button == 1:
            self.onclick(self.offset)
            return True


class TabPanel(urwid.WidgetWrap):
    def __init__(self, tabs, offset = 0):
        super().__init__("")
        self.tabs = tabs
        self.tab_offset = offset
        self.show()

    def keypress(self, size, key):
        num_tabs = len(self.tabs)
        if key == "left":
            self.set_active_tab((self.tab_offset - 1) % num_tabs)
        elif key == "right":
            self.set_active_tab((self.tab_offset + 1) % num_tabs)
        else:
            return self._w.keypress(size, key)

    def set_active_tab(self, offset):
        self.tab_offset = offset
        self.show()

    def show(self):
        if not self.tabs:
            return
        headers = []
        for idx in range(len(self.tabs)):
            label = self.tabs[idx].label
            if self.tab_offset == idx:
                headers.append(Tab(idx, label, "heading", self.set_active_tab))
            else:
                headers.append(Tab(idx, label, "heading inactive", self.set_active_tab))

        headers = urwid.Columns(headers, dividechars=1)
        body = self.tabs[self.tab_offset].widget
        self._w = urwid.Frame(body, header=headers)
        self._w.set_focus("body")