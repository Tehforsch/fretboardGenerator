# Fretboard Generator

A small script to quickly generate semi-good looking diagrams of fretboard patterns (scales, chords) using gnuplot.

Takes a pattern string and converts it into a picture. A pattern string looks like
(All frets on first string separated by a space), (All frets on second string separated by a space), ...
Optionally, one can signify the root note by placing a "!" behind the fret.

This is just something I needed quickly, but maybe I will extend the functionality to "understand" music theory so that Arpeggios and Scales can be generated automatically.

# Examples

6th Chord voicing with Root on E string:

**2!,,1,3,2**

![6th Chord voicing with Root on E string](../samplePictures/pics/ERoot6.png?raw=true)

Standard Major Scale starting with the Root on the E string

**1! 3 5, 1 3 5, 2 3! 5, 2 3 5, 3 5, 1! 3 5**

![Standard Major Scale starting with the Root on the E string](../samplePictures/pics/1PosMajorScale.png?raw=true)
