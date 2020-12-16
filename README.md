# PYBERPUNK2077cli
Pyberpunk is a cli app with a single purpose, make self-drive cars in Cyberpunk2077 using Python.
Name explain itself!

[![Gif](/resources/usage.gif)]

## How-To
Soon

[![Usage on youtube](/video_thumb.jpg)](#)

## Games Pre-Requisites

Have sure that your game is in 1280x700 windowed mode

[![Screensize](/resources/screensize.png)]

Your key binding of vehicle movement must be:
* Forward = Mouse Middle Button
* Left = Mouse Left Button
* Right = Mouse Right Button

[![Keybindings](/resources/keybindings.png)]

Play on first person preferable on a bike

[![Firstperson](/resources/firstperson.png)]

## Instalation
1. `git clone https://github.com/andre250/pyberpunk2077.git`
2. `cd pyberpunk2077`
3. `pip install .`
4. `pyberpunkcli2077 [cmd]` Check [Functions](#Functions) section to understand usage.

## Environment variables
Strongly recomend to use [`env.py`](/pyberpunk2077cli/env.py) to play with the algorithm, maybe for another games.

# Functions

* [`pyberpunk2077cli selfdrive`](#Selfdrive) - Drive cars in Cyberpunk2077, but works better with bikes on first person mode.


## Selfdrive
`selfrive` app uses a lot of image processing.

Basically he first process a image with Canvy and HoughLinesP alghorithm

And then try to draw lines and lanes using mathematical functions

Finally based on the lines created it send commands to mouse click functions. Yes mouse, because actually the rebinding keys of Cyberpunk2077 is kind a mess.
```commandline
Usage: pyberpunk2077cli selfdrive [OPTIONS] COMMAND [ARGS]...

  Cyberpunk2077 self driving

Options:
  --help  Show this message and exit.

Commands:
  run  Run services
```

***`run`***

Runs the algorithm!

```commandline
Usage: pyberpunk2077cli selfdrive run [OPTIONS]

  Cyberpunk2077 self driving

Options:
  -t, --test BOOLEAN  Set True if you want to go Test-Mode, leave to go on Self-Drive.

  --help             Show this message and exit.
```

___options___
* `-t` `--test` - Set True if you want to go Test-Mode, leave to go on Self-Drive. Default: `False`.

```commandline
$ pyberpunk2077cli selfdrive run -t True
```
[![Usage](/resources/usage.png)]

# Credits and References
https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
https://towardsdatascience.com/finding-driving-lane-line-live-with-opencv-f17c266f15db
https://medium.com/@mrhwick/simple-lane-detection-with-opencv-bfeb6ae54ec0
https://github.com/PercyJaiswal/Find_Lane_Line_Live_OpenCV/blob/master/Live_Lane_Line_Find.py
https://github.com/Sentdex/pygta5/blob/master/LICENSE
