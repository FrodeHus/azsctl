import urwid

class TableCell(urwid.Text):
    def __init__(self, content, width = 10, separator=True,align='left'):
        self.separator = separator
        self._content = content
        self._align = align
        self._width = width
        self._content = self._render_content()
        super().__init__(self._content, align, 'ellipsis')

    def _render_content(self):
        content = str(self._content)
        max_length = len(content)
        if self.separator:
            max_length = self._width - 1

        if len(content) > max_length:
            content = content[0:max_length - 1]

        if self.separator:
            content = content + "|"

        return content

    def resize(self, width):
        self._width = width
        content = self._render_content()
        self.set_text(content)

class TableRow(urwid.Columns):
    def __init__(self, fields):
        super().__init__(fields, dividechars=1)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

    # def render(self, size, focus=False):
    #     for field in self.contents:
    #         if not isinstance(field[0], TableCell):
    #             continue

    #         text, attr = field[0].get_text()
    #     return super().render(size, focus=focus)

class TableHeader(TableRow):
    def __init__(self, headers):
        columns = self._create_columns(headers)
        super().__init__(columns)

    def _create_columns(self, headers):
        return [TableCell(text) for text in headers]


class TableView(urwid.ListBox):
    def __init__(self, rows=[]):
        super().__init__(urwid.SimpleFocusListWalker(rows))

    def __iter__(self):
        for row in self.body:
            yield row

    @property
    def focused_row(self):
        row, index = self.body.get_focus()
        return row.original_widget

    def add_row(self, data):
        columns = []
        for value in data.values():
            columns.append(TableCell(str(value)))

        row = urwid.AttrMap(TableRow(columns), None, focus_map='heading')
        self.body.append(row)

class AnalyticsResultTable(urwid.Frame):
    def __init__(self,result):
        self._result = result
        self._rows = len(self._result)
        headers = []
        if self._rows > 0:
            item = self._result[0]
            headers = item.keys()
        self._header = TableHeader(headers)
        self._body = TableView()
        self._build_rows(self._result)
        super().__init__(self._body, header=urwid.AttrMap(self._header, 'heading'))

    def _build_rows(self, data):
        for item in data:
            self._body.add_row(item)