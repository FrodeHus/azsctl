import urwid
from typing import Callable,List

   
class SentinelItemList(urwid.ListBox):
    def __init__(self, item_retriever : Callable[[], List[urwid.Widget]]):
        self.walker = SentinelItemListWalker(item_retriever)
        super().__init__(self.walker)
        urwid.register_signal(self.__class__, ['item_selected'])

    def keypress(self, size, key):
        if key == 'enter':
            urwid.emit_signal(self, 'item_selected', self, self.walker.selected_item())
        elif key == 'r':
            self.walker.refresh()
        return super().keypress(size, key)

class SentinelItemListWalker(urwid.ListWalker):
    def __init__(self, item_retriever : Callable[[], List[urwid.Widget]]):
        self.retriever = item_retriever
        self.items = item_retriever()
        self.focus = 0
    
    def refresh(self):
        self.items = self.retriever()
        self._modified()

    def selected_item(self):
        if self.items[self.focus]:
            return self.items[self.focus].base_widget.get_data()

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