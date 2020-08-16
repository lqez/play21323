from gpiozero import DigitalOutputDevice, DigitalInputDevice
from gpiozero import Button, LED
from time import sleep
import pygame.mixer
from pygame.mixer import Sound

# low buffer for shorter latency
pygame.mixer.init(22050, -8, 2, 256)

signal = [
    LED('BOARD11'),
    LED('BOARD13'),
    LED('BOARD15'),
]

mux = [
    Button('BOARD35', pull_up=False),
    Button('BOARD33', pull_up=False),
    Button('BOARD31', pull_up=False),
    Button('BOARD29', pull_up=False),
]

print("Loading sounds...")
soundmap = [
    # MUX 0
    {"name": "F3", "sound": Sound("assets/f3.wav"), },
    {"name": "C3", "sound": Sound("assets/c3.wav"), },
    {"name": "G3", "sound": Sound("assets/g3.wav"), },
    {"name": "C#3", "sound": Sound("assets/c3s.wav"), },
    {"name": "F#3", "sound": Sound("assets/f3s.wav"), },
    {"name": "D#3", "sound": Sound("assets/d3s.wav"), },
    {"name": "E3", "sound": Sound("assets/e3.wav"), },
    {"name": "D3", "sound": Sound("assets/d3.wav"), },

    # MUX 1
    {},
    {"name": "G#3", "sound": Sound("assets/g3s.wav"), },
    {"name": "C#4", "sound": Sound("assets/c4s.wav"), },
    {"name": "A3", "sound": Sound("assets/a3.wav"), },
    {"name": "C4", "sound": Sound("assets/c4.wav"), },
    {"name": "B3", "sound": Sound("assets/b3.wav"), },
    {},
    {"name": "A#3", "sound": Sound("assets/a3s.wav"), },

    # MUX 2
    {"name": "F#4", "sound": Sound("assets/f4s.wav"), },
    {"name": "D4", "sound": Sound("assets/d4.wav"), },
    {"name": "G#4", "sound": Sound("assets/g4s.wav"), },
    {"name": "D#4", "sound": Sound("assets/d4s.wav"), },
    {"name": "G4", "sound": Sound("assets/g4.wav"), },
    {},
    {"name": "F4", "sound": Sound("assets/f4.wav"), },
    {"name": "E4", "sound": Sound("assets/e4.wav"), },

    # MUX 3
    {},
    {"name": "A4", "sound": Sound("assets/a4.wav"), },
    {},
    {"name": "A#4", "sound": Sound("assets/a4s.wav"), },
    {},
    {"name": "C5", "sound": Sound("assets/c5.wav"), },
    {},
    {"name": "B4", "sound": Sound("assets/b4.wav"), },
]

print("Running...")

bs = [0] * 32
while True:
    for s in range(0, 8):
        b = '{0:03b}'.format(s)
        for i in range(3):
            if b[i] == '1':
                signal[i].on()
            else:
                signal[i].off()

        for i in range(4):
            idx = i * 8 + s

            if mux[i].is_pressed:
                if bs[idx] == 0:
                    bs[idx] = 1
                    soundmap[idx]["sound"].play()
            else:
                if bs[idx] == 1:
                    bs[idx] = 0
                    soundmap[idx]["sound"].fadeout(250)  # stop() sounds weird, so fading them out...

    print(bs, end='\r')
