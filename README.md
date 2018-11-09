# ShimoneIndianMusic
Overal Goal:Work on the robotic marimbe player Shimone, to develop an algorithm for performing live improvised Indian music.
Subprojects: ShimonePathPlanning, BeatDetect & midiAnalysis


### ShimonePathPlanning
Basic path planning algorithm that would move the hypothetical mallet arms of shimone in order to play the correct notes on time.

### BeatDetect
Using a variety of python libraries, can detect beats per minute (bpm) of musical audio files (mp3 or wav)
(specifically tailered to india classical music with a rhythmic instrument) 
Algorithm relies on a variety of filters that enable isolation of the rhythmic undertones and therefore the beats.
Flow of code:
Audio => Low & high pass filters => click/bpm detection algorithm => output bpm



### midiAnalysis
From files containing frequency of indian music (.pitch files) determine important characteristics of the music, 
like the most frequent notes, and frequent note intervals leaped. And store that information.  
Can be used to classify ragas, and develop a way to generate the music.




