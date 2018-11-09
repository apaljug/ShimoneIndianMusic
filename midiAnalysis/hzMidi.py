import music21

import numpy as np
import matplotlib.pylab as plt




#method that takes values across octaves and consolidates
def pitchfrequencies(arr, midiStart, canPrint, canPlot):
    #frequency based on notes/octave for sorting
    #NOT USED CURRENRTLY
    notes = []

    #frequency based on notes (w/o octave) for sorting
    octave = []
    #create octave arr
    for i in range(12):
        p = music21.pitch.Pitch()
        p.midi = i + 60
        octave.append([p, 0])

    for i, num in enumerate(arr):
        p = music21.pitch.Pitch()
        p.midi = i + midiStart
        #notes.append([p, num])
        p2 = music21.pitch.Pitch()
        p2.name = p.name
        p2.octave = 4
        octave[p2.midi - 60][1] += num
        #print(p.midi , "  " , p, " frequency: " , num , "\n")
    """
    notes.sort(key=take2)
    for p in notes:
        print(p[0].midi , "  " , p[0], " frequency: " , p[1], "\n")
    """
    if canPrint:

        for p in sorted(octave, key=take2):
            print(p[0].name, " appeared: " , p[1], " times\n")

        if canPlot:
            plot = []
            label = []
            for p in octave:
                plot.append(p[1])
                label.append(p[0].name)

             # this is for plotting purpose
            index = np.arange(len(label))
            plt.bar(index, plot)
            plt.xlabel('note', fontsize=5)
            plt.ylabel('times counted', fontsize=5)
            plt.xticks(index, label, fontsize=5, rotation=30)
            plt.title('Frequency of notes in raga')
            plt.show()





    return octave

def take2(elem):
    return elem[1]

#normalize a list of frequencies
def normalize(arr2):
    arr = arr2.copy()
    tot = 0.0
    for num in arr:
        tot = tot + num
    for i, num in enumerate(arr):
        arr[i] = arr[i] / tot
    return arr


def findIntervalPatterns(intervals, midiStart,canPrint,canPlot):

    patterns = []
    for i in range(12):
        p = music21.pitch.Pitch()
        p.midi = i + 60
        octave = [p]
        #create octave arr
        for i in range(12):
            p = music21.pitch.Pitch()
            p.midi = i + 60
            octave.append([p, 0])
        patterns.append(octave)

    for first in range(len(intervals)):
        arr = intervals[first]
        p = music21.pitch.Pitch()
        p.midi = first + midiStart
        #notes.append([p, num])
        p2 = music21.pitch.Pitch()
        p2.name = p.name
        p2.octave = 4
        #edit = patterns[p2.midi - 60]
        for second in range(len(arr)):
            val = intervals[first][second]
            p3 = music21.pitch.Pitch()
            p3.midi = second + midiStart
            #notes.append([p, num])
            p4 = music21.pitch.Pitch()
            p4.name = p3.name
            p4.octave = 4
            patterns[p2.midi - 60][p4.midi - 60 + 1][1] += val


    if canPrint:
        labels = []
        plot = []
        size = 10
        print("{:10}".format(" "), end='')
        for i in range(12):
            p = music21.pitch.Pitch()
            p.midi = i + 60
            print("{:11}".format(p.name), end='')
            labels.append(p.name)
        print()
        for p in range(len(patterns)):
            pit = music21.pitch.Pitch()
            pit.midi = p + 60
            print( "{:10}".format(pit.name) , end='')
            arr4plot = []
            for val in range(1,len(patterns[0])):
                print("{:10}".format(str(patterns[p][val][1])),  end=' ')
                arr4plot.append(patterns[p][val][1])
            print()
            plot.append(arr4plot)

        if canPlot:
            plt.imshow(np.array(plot), cmap='hot', interpolation='nearest')
            plt.show()


        """
        for p in range(len(intervals)):
            pit = music21.pitch.Pitch()
            pit.midi = p + 60
            print( pit.name , end='')
            for val in range(len(intervals[0])):
                print(str(intervals[p][val]),  end=' ')
            print()
        """



    return patterns


##file creation
#input
input = "raga.pitch"
hertzFile = open(input, "r")

#output (NOT USED currently)
#midiFile = open("midi.txt","w")


#stream1 = music21.stream.Stream()
arr = hertzFile.readlines()
#print( "arr is " ,  arr)

#find this before hand (CURRENTLY HARDCODED)
lowestval = 40
highestval = 81
if '2' in input:
    lowestval = 46
    highestval = 78




dif = highestval - lowestval

frequency = [0.0] * dif


rows = dif
cols = dif

noteintervalcounts = [ ([0.0] * cols) for row in range(rows) ]

last = -1
for line in arr:
    i = float(line.split()[1])
    if  i != 0.0 :
        p = music21.pitch.Pitch()
        p.frequency = i
        midiVal = p.midi
        #midiFile.write(str(midiVal) + "\n")
        print(midiVal , "  " , p, (last + lowestval + 1))
        #stream1.append(music21.note.Note(p))

        frequency[midiVal - lowestval - 1 ] += 1

        if last != -1:
            noteintervalcounts[midiVal - lowestval - 1][last] += 1

        last = midiVal - lowestval - 1

        ##somehow do this before hand REMOVE HARDCODE
        if midiVal < lowestval:
            lowestval = midiVal
        if midiVal > highestval:
            highestval = midiVal



#print(frequency)
#normal = normalize(frequency)

pitchfrequencies(frequency, lowestval, True, True)


findIntervalPatterns(noteintervalcounts, lowestval , True, True)
#print(normal
print("lowest: " , lowestval)
print("highest: " , highestval)




#stream1.show('midi')
