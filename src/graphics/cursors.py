class Cursor:
  def __init__(self):
        self.stringcursor = ""
        self.black = 'X'
        self.white = '.'

class CircleCursor_white(Cursor):
    def __init__(self):
        Cursor.__init__(self)
        self.stringcursor = (
            "  ....  ",
            " .XXXX. ",
            ".XXXXXX.",
            ".XXXXXX.",
            ".XXXXXX.",
            ".XXXXXX.",
            " .XXXX. ",
            "  ....  ")
class CircleCursor_black(Cursor):
    def __init__(self):
        Cursor.__init__(self)
        self.stringcursor = (
            "  XXXX  ",
            " X....X ",
            "X......X",
            "X......X",
            "X......X",
            "X......X",
            " X....X ",
            "  XXXX  ")
class ClassicCursor_black(Cursor):
    def __init__(self):
        Cursor.__init__(self)
        self.stringcursor = (
            "XX                      ",
            "XXX                     ",
            "XXXX                    ",
            "XX.XX                   ",
            "XX..XX                  ",
            "XX...XX                 ",
            "XX....XX                ",
            "XX.....XX               ",
            "XX......XX              ",
            "XX.......XX             ",
            "XX........XX            ",
            "XX........XXX           ",
            "XX......XXXXX           ",
            "XX.XXX..XX              ",
            "XXXX XX..XX             ",
            "XX   XX..XX             ",
            "     XX..XX             ",
            "      XX..XX            ",
            "      XX..XX            ",
            "       XXXX             ",
            "       XX               ",
            "                        ",
            "                        ",
            "                        ")
