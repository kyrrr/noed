from collections import defaultdict


class InnerDescriptor(object):
    def __init__(self, cls):
        self.cls = cls

    def __get__(self, instance, owner):
        class Wrapper(self.cls):
            owner = instance
        Wrapper.__name__ = self.cls.__name__
        return Wrapper


class MarkDown:

    lines = []
    variables = "\n"  # place at end
    md_str = "\n"
    dict_lines = {}
    filename = None
    extension = ".md"

    def __init__(self, filename=None):
        if filename:
            self.filename = filename + self.extension

    def header_1(self, header):
        self.md_str += "# " + header + "\n"
        return self

    def header_2(self, header):
        self.md_str += "## " + header + "\n"
        return self

    def header_3(self, header):
        self.md_str += "### " + header + "\n"
        return self

    def header_4(self, header):
        self.md_str += "#### " + header + "\n"
        return self

    def header_5(self, header):
        self.md_str += "##### " + header + "\n"
        return self

    def text(self, text, bold=False, italic=False, strikethrough=False):
        if bold:
            text = "__" + text + "__"
        if italic:
            text = "*" + text + "*"
        if strikethrough:
            text = "~~" + text + "~~"

        self.md_str += text + "\n"
        return self

    def variable(self, name, value):
        pass

    def __str__(self):
        return self.md_str

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(self.md_str)

    @InnerDescriptor
    class Table:
        table = defaultdict(list)
        md_str = "\n"

        def header(self, text):
            self.table['headers'].append(text)
            return self

        def entry(self, key, values):
            self.table['entries'].append({key: values})
            return self

        def make(self):
            self.md_str += "| "
            i = 0
            for i, header in enumerate(self.table['headers']):
                self.md_str += header + " | "
            self.md_str += "\n"
            self.md_str += "|"
            for j in range(0, i + 1):
                self.md_str += " ----- |"
            for entry in self.table['entries']:
                self.md_str += "\n"
                self.md_str += "| "
                for key, values in entry.items():
                    self.md_str += key + " |"
                    for value in values:
                        self.md_str += " " + value + " |"
            self.owner.md_str += self.md_str + "\n \n"
            return self.owner

    @InnerDescriptor
    class Code:
        md_str = "\n"

        def __init__(self, language, display_language_name=True):
            if display_language_name:
                self.md_str += language.title() + "\n"
            self.md_str += "```" + language + "\n"

        def add_line(self, line, indentation=0):
            indent = ""
            for i in range(0, indentation):
                indent += "    "
            self.md_str += indent + line + "\n"
            return self

        def make(self):
            self.md_str += "```" + "\n \n"
            self.owner.md_str += self.md_str
            return self.owner

    @InnerDescriptor
    class List:
        md_str = "\n"

        def __init__(self, title=None):
            if title:
                self.md_str += "__" + title + "__" + "\n \n"

        def unordered_entry(self, text, indentation=0):
            indent = ""
            for i in range(0, indentation):
                indent += "    "
            self.md_str += indent + "- " + text + "\n"
            return self

        def make(self):
            self.owner.md_str += "\n" + self.md_str + "\n"
            print(self.owner.md_str)
            return self.owner
