import urwid
from azsctl.ui.controller import RefreshableItems

class SentinelItemList(urwid.ListBox):

    def keypress(self, size, key):
        if key == 'enter':
            pass
        return urwid.ListBox.keypress(self, size, key)

class SentinelItemListWalker(urwid.ListWalker):
    def __init__(self, retriever : RefreshableItems):
        self.retriever = retriever
        self.items = retriever.items
        self.focus = 0

    def get_focus(self):
        return self._get_at_pos(self.focus)

    def set_focus(self, focus):
        self.focus = focus
        self._modified()

    def get_next(self, start_from):
        return self._get_at_pos(start_from + 1)

    def get_prev(self, start_from):

        return self._get_at_pos(start_from - 1)

    def _get_at_pos(self, pos):
        if pos < 0:
            return None, None

        if len(self.items) > pos:
            return self.items[pos], pos

        return None, None
    
        
        
        
