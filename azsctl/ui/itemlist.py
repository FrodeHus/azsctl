import urwid


class ItemWidget(urwid.TreeWidget):
    def __init__(self, node):
        self.__super.__init__(node)
        self._w = urwid.AttrWrap(self._w, None)
        self._w.attr = 'body'
        self._w.focus_attr = 'focus'
    
    def get_display_text(self):
        return self.get_node().get_key()
    
    def selectable(self):
        return True


class Item(urwid.TreeNode):
    def __init__(self, displayName: str, item, parent=None):
        urwid.TreeNode.__init__(self, item, key=displayName, parent=parent)

    def load_widget(self):
        return ItemWidget(self)


class ItemParentWidget(urwid.TreeWidget):
    def get_display_text(self):
        return "Alert rules"

class ItemParent(urwid.ParentNode):
    def __init__(self, items: list, parent=None):
        key = "Items"
        urwid.ParentNode.__init__(self, items, key=key, parent=parent)

    def load_child_keys(self):
        items = self.get_value()
        keys = []
        for item in items:
            keys.append(item["properties"]["displayName"])
        return keys

    def load_child_node(self, key):
        index = self.get_child_index(key)
        return Item(key, None, self)

    def load_widget(self):
        return ItemParentWidget(self)

class ItemList:
    def __init__(self, items: list):
        self.header = urwid.Text("")
        self.listbox = urwid.TreeListBox(urwid.TreeWalker(ItemParent(items)))
        self.listbox.offset_rows = 1
        self.palette = [
            ("body", "light gray", "black"),
            ("flagged", "black", "dark green", ("bold", "underline")),
            ("focus", "light cyan", "black", "standout"),
            ("flagged focus", "yellow", "dark cyan", ("bold", "standout", "underline")),
            ("head", "yellow", "black", "standout"),
            ("foot", "light gray", "black"),
            ("key", "light cyan", "black", "underline"),
            ("title", "white", "black", "bold"),
            ("dirmark", "black", "dark cyan", "bold"),
            ("flag", "dark gray", "light gray"),
            ("error", "dark red", "light gray"),
        ]
        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, "body"),
            header=urwid.AttrWrap(self.header, "head"),
        )

    def display(self):
        self.loop = urwid.MainLoop(
            self.view, unhandled_input=self.unhandled_input, palette=self.palette
        )
        self.loop.run()

    def add_item(display_name: str, item):
        se

    def unhandled_input(self, k):
        if k in ("q", "Q"):
            raise urwid.ExitMainLoop()