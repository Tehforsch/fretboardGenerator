import os
import subprocess

class Fret:
    def __init__(self, string):
        self.position = int(string.replace("!", ""))
        self.root = "!" in string

class Pattern:
    def __init__(self, string):
        spl = string.split(",")
        spl = [s.strip() for s in spl]
        self.frets = []
        for s in spl:
            numbers = s.split(" ")
            if numbers == [""]:
                self.frets.append([])
                continue
            self.frets.append([Fret(s) for s in numbers])
        self.numStrings = len(self.frets)
        key = lambda fret : fret.position
        minFretPos = min([min(string, key=key) for string in self.frets if string != []], key = key).position
        maxFretPos = max([max(string, key=key) for string in self.frets if string != []], key = key).position
        self.numFrets = maxFretPos - minFretPos + 1
        # Shift, such that the lowest fret is always 0
        for string in self.frets:
            for fret in string:
                fret.position = fret.position - minFretPos

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
            color = "red" if fret.root else "blue"
            x = fretWidth * (fret.position + 0.5)
            y = stringHeight * (string)
            s = s + drawCircle(x, y, dotRadius, color)
    return s

def endConfiguration():
    s = ""
    # Plot something empty so gnuplot does something
    s = s + "# Plot something empty so gnuplot does something\n"
    s = s + "plot 1/0 title \"\""
    return s

def drawLine(x1, y1, x2, y2):
    return "set arrow from " + str(x1) + "," + str(y1) + " to " + str(x2) + "," + str(y2) + " nohead lc rgb \'black\'\n"

def drawCircle(x, y, radius, color = "blue"):
    return "set object circle at first " + str(x) + "," + str(y) + " size first " + str(radius) + " fillstyle solid fc rgb \"" + color + "\"\n"

def createPic(name, patternString):
    s = ""
    pattern = Pattern(patternString)
    s = s + outputConfiguration(name)
    s = s + initialConfiguration(pattern.numStrings, pattern.numFrets)
    s = s + drawFretboard(pattern.numStrings, pattern.numFrets)
    s = s + drawPattern(pattern)
    s = s + endConfiguration()
    writeFile("plots/plot.gpi", s)
    path = os.path.abspath(".")
    output = runCommand("gnuplot plot.gpi", path="plots")

def writeFile(filename, content):
    print(filename)
    with open(filename, "w") as f:
        f.write(content)

def runCommand(command, path = None):
    """Runs the system command and returns output and errors"""
    if path is not None:
        mainPath = os.getcwd()
        os.chdir(path)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # I think this properly waits for the process to finish and therefore
    # gets the correct return code which can be useful to check if something failed
    stdout, stderr = p.communicate() 
    if path is not None:
        os.chdir(mainPath)
    return p.returncode, stdout, stderr

def ensureExists(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)

ensureExists("plots")
ensureExists("pics")

fretWidth = 50
stringHeight = 50
dotRadius = 5
excessSpace = 50
# createPic("ERootMinorScale", "1! 3 4,1 3 4,1 3! 5,1 3,1 2 4, 1! 3 4")
# createPic("ARootMinorScale", "1 2 4,1! 3 4,1 3 5,1 3!,1 2 4, 1 3 4")
# createPic("ERoot6", "2!,,1,3,2")
createPic("7b9", ",2!,1,2,1,")
createPic("minorb5", "2!,,2,2,1,")
