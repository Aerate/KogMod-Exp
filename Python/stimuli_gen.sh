#For fast Stimuli Generation

#Triangle for all distortion levels:
#1
python stimuluserzeuger.py -dl 1 -f "svg" -dir "./examples/triangle1" -o "triangle" -nd 10
#2
python stimuluserzeuger.py -dl 2 -f "svg" -dir "./examples/triangle2" -o "triangle" -nd 10
#3
python stimuluserzeuger.py -dl 3 -f "svg" -dir "./examples/triangle3" -o "triangle" -nd 10
#...
python stimuluserzeuger.py -dl 4 -f "svg" -dir "./examples/triangle4" -o "triangle" -nd 10
python stimuluserzeuger.py -dl 5 -f "svg" -dir "./examples/triangle5" -o "triangle" -nd 10
python stimuluserzeuger.py -dl 6 -f "svg" -dir "./examples/triangle6" -o "triangle" -nd 10
python stimuluserzeuger.py -dl 7 -f "svg" -dir "./examples/triangle7" -o "triangle" -nd 10
python stimuluserzeuger.py -dl 8 -f "svg" -dir "./examples/triangle8" -o "triangle" -nd 10
python stimuluserzeuger.py -dl 9 -f "svg" -dir "./examples/triangle9" -o "triangle" -nd 10

#other shapes (only distortion level 5)
#Diamonds
python stimuluserzeuger.py -dl 5 -f "svg" -dir "./examples/diamond" -o "diamond" -nd 10

#Ms
python stimuluserzeuger.py -dl 5 -f "svg" -dir "./examples/M" -o "M" -nd 10

#Fs
python stimuluserzeuger.py -dl 5 -f "svg" -dir "./examples/F" -o "F" -nd 10

#Randoms
python stimuluserzeuger.py -dl 5 -f "svg" -dir "./examples/random" -o "random" -nd 10

