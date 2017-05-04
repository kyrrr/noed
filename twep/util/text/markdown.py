class MarkDown:

    lines = []
    dict_lines = {}
    filename = None
    extension = ".md"

    def __init__(self, filename=None):
        if filename:
            self.filename = filename + self.extension

    def header_1(self, header):
        self.lines.append("# " + header)
        return self

    def header_2(self, header):
        self.lines.append("## " + header)
        return self

    def header_3(self, header):
        self.lines.append("### " + header)
        return self

    def header_4(self, header):
        self.lines.append("#### " + header)
        return self

    def header_5(self, header):
        self.lines.append("##### " + header)
        return self

    def text(self, text):
        self.lines.append(text)
        return self

    def doc(self):
        foo = "\n"
        for l in self.lines:
            foo += (l + "\n")
        return foo

    def save(self):
        with open(self.filename, 'w') as f:
            for l in self.lines:
                f.write(l + "\n")
