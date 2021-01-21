import urwid

class TableCell(urwid.Text):
    def __init__(self, content, width = 10, separator=True,align='left'):
        self.separator = separator
        self._content = content
        self._align = align
        self._width = width
        self._content = self._render_content()
        super().__init__(self._content, align, 'clip')

    def _render_content(self):
        content = str(self._content)
        max_length = len(content)
        if self.separator:
            max_length = self._width - 1

        if len(content) > max_length:
            content = content[0:max_length - 1]
            content += chr(187)

        if self._align == 'left':
            content = content.ljust(max_length)
        else:
            content = content.rjust(max_length)

        if self.separator:
            content += chr(124)

        return content

    def resize(self, width):
        self._width = width
        content = self._render_content()
        self.set_text(content)

class TableRow(urwid.Columns):
    def __init__(self, data, selectable = True):
        self.data = data
        self._selectable = selectable
        columns = self._create_columns(data)
        super().__init__(columns, dividechars=1)

    def selectable(self):
        return True

    def _create_columns(self, data):
        columns = []
        for value in data:
            columns.append(TableCell(str(value)))
        return columns

class TableHeader(TableRow):
    def __init__(self, headers):
        super().__init__(headers, False)

class TableView(urwid.ListBox):
    def __init__(self, rows=[]):
        super().__init__(urwid.SimpleFocusListWalker(rows))

    def __iter__(self):
        for row in self.body:
            yield row

    def keypress(self, size, key):
        if key in ('up', 'down'):
            super().keypress(size, key)
        return key

    @property
    def focused_row(self):
        row, index = self.body.get_focus()
        return row.original_widget

    def add_row(self, data):
        row = urwid.AttrMap(TableRow(data.values()), None, focus_map='heading inactive')
        self.body.append(row)

class Table(urwid.Frame):
    def __init__(self,result):
        self._result = result
        self._rows = len(self._result)
        self.headers = []
        if self._rows > 0:
            item = self._result[0]
            self.headers = item.keys()
        self._header = TableHeader(self.headers)
        self._body = TableView()
        
        self._build_rows(self._result)
        urwid.register_signal(self.__class__, ['keypress','item_selected'])
        super().__init__(self._body, header=urwid.AttrMap(self._header, 'heading'), focus_part='body')

    def _build_rows(self, data):
        for item in data:
            self._body.add_row(item)

    def keypress(self, size, key):
        if key == 'enter':
            values = self.focus.focused_row.data
            item = zip(self.headers, values)
            urwid.emit_signal(self, 'item_selected', self, dict(item))
        urwid.emit_signal(self, 'keypress', self, key)
        return super().keypress(size, key)