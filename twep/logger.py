import os


class Logger:
    dir = 'log/'
    screen_name = None
    file_format = None
    path = None

    def __init__(self, screen_name, file_format=".txt"):
        self.screen_name = screen_name
        self.file_format = file_format
        self.path = self.dir + self.screen_name + "_log" + self.file_format

    def log(self, msg):
        os.makedirs(os.path.dirname(self.dir), exist_ok=True)
        f = open(self.path, 'a+')
        f.write(msg)  # python will convert \n to os.linesep
        f.close()
