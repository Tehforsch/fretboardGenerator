# from fretboardGenerator import modulename
from pyUtils import fileUtils
from pyUtils import osUtils
import os

class Pattern:
    def __init__(self, string):
        spl = string.split(",")
        spl = [s.strip() for s in spl]
        self.frets = []
        for s in spl:
            numbers = s.split(" ")
            if numbers[0] == "":
                self.frets.append([])
            else:
                self.frets.append([int(n) for n in numbers])
        self.numStrings = len(self.frets)
        self.shift = min(map(lambda x : 999 if len(x) == 0 else min(x), self.frets)) 
        self.numFrets = max(map(lambda x : 0 if len(x) == 0 else max(x), self.frets)) - self.shift + 1
        self.frets = [[f - self.shift for f in s] for s in self.frets]
        

def outputConfiguration(name):
    return "set terminal pngcairo\nset output \"../pics/" + name + ".png\"\n\n"

    s = ""

def initialConfiguration(numStrings, numFrets):
    width = numFrets * fretWidth
    height = (numStrings-1) * stringHeight
    # Ranges, disable all grids etc.
    s = ""
    s = s + "# Ranges, disable all grids etc.\n"
    s = s + "set xrange [" + str(-excessSpace) + ":" + str(width+excessSpace) + "]\n"
    s = s + "set yrange [" + str(-excessSpace) + ":" + str(height+excessSpace) + "]\n"
    s = s + "unset grid\n"
    s = s + "unset border\n"
    s = s + "unset xtics\n"
    s = s + "unset ytics\n"
    return s

def drawFretboard(numStrings, numFrets):
    width = numFrets * fretWidth
    height = (numStrings-1) * stringHeight
    s = ""
    # Vertical lines
    s = s + "#Vertical Lines\n"
    for i in range(numFrets + 1):
        s = s + drawLine(i * fretWidth, 0, i * fretWidth, height)
    # Horizontal lines
    s = s + "#Horizontal Lines\n"
    for i in range(numStrings):
        s = s + drawLine(0, i * stringHeight, width, i * stringHeight)

    return s

def drawPattern(pattern):
    s = ""
    for (string, frets) in enumerate(pattern.frets):
        for fret in frets:
            x = fretWidth * (fret + 0.5)
            y = stringHeight * (string)
            s = s + drawCircle(x, y, dotRadius)
    return s

def endConfiguration():
    s = ""
    # Plot something empty so gnuplot does something
    s = s + "# Plot something empty so gnuplot does something\n"
    s = s + "plot 1/0 title \"\""
    return s

def drawLine(x1, y1, x2, y2):
    return "set arrow from " + str(x1) + "," + str(y1) + " to " + str(x2) + "," + str(y2) + " nohead lc rgb \'black\'\n"

def drawCircle(x, y, radius):
    return "set object circle at first " + str(x) + "," + str(y) + " size first " + str(radius) + " fillstyle solid fc rgb \"blue\"\n"

def createPic(name, patternString):
    s = ""
    pattern = Pattern(patternString)
    s = s + outputConfiguration(name)
    s = s + initialConfiguration(pattern.numStrings, pattern.numFrets)
    s = s + drawFretboard(pattern.numStrings, pattern.numFrets)
    s = s + drawPattern(pattern)
    s = s + endConfiguration()
    fileUtils.writeFile("plots/plot.gpi", s)
    path = os.path.abspath(".")
    print("Output:", osUtils.executeStandardCommand(path, "plots/plot.gpi", "gnuplot"))

fretWidth = 50
stringHeight = 50
dotRadius = 5
excessSpace = 50
createPic("ERootMinorScale", "1 3 4,1 3 4,1 3 5,1 3,1 2 4, 1 3 4")
createPic("ERoot6", "2,,1,3,2")
