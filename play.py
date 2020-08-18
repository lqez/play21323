from gpiozero import DigitalOutputDevice, DigitalInputDevice
from gpiozero import Button, LED
from time import sleep
import pygame.mixer
from pygame.mixer import Sound

# low buffer for shorter latency
pygame.mixer.init(22050, -8, 2, 256)

# Mux selector
signal = [
    LED('BOARD11'),
    LED('BOARD13'),
    LED('BOARD15'),
]

# Muxes are connected to each touch sensor
mux = [
    Button('BOARD35', pull_up=False),
    Button('BOARD33', pull_up=False),
    Button('BOARD31', pull_up=False),
    Button('BOARD29', pull_up=False),
]

print("Loading sounds...")

sounds = {
    "C2": Sound("assets/c2.wav"),
    "C#2": Sound("assets/c2s.wav"),
    "D2": Sound("assets/d2.wav"),
    "D#2": Sound("assets/d2s.wav"),
    "E2": Sound("assets/e2.wav"),
    "F2": Sound("assets/f2.wav"),
    "F#2": Sound("assets/f2s.wav"),
    "G2": Sound("assets/g2.wav"),
    "G#2": Sound("assets/g2s.wav"),
    "A2": Sound("assets/a2.wav"),
    "A#2": Sound("assets/a2s.wav"),
    "B2": Sound("assets/b2.wav"),

    "C3": Sound("assets/c3.wav"),
    "C#3": Sound("assets/c3s.wav"),
    "D3": Sound("assets/d3.wav"),
    "D#3": Sound("assets/d3s.wav"),
    "E3": Sound("assets/e3.wav"),
    "F3": Sound("assets/f3.wav"),
    "F#3": Sound("assets/f3s.wav"),
    "G3": Sound("assets/g3.wav"),
    "G#3": Sound("assets/g3s.wav"),
    "A3": Sound("assets/a3.wav"),
    "A#3": Sound("assets/a3s.wav"),
    "B3": Sound("assets/b3.wav"),

    "C4": Sound("assets/c4.wav"),
    "C#4": Sound("assets/c4s.wav"),
    "D4": Sound("assets/d4.wav"),
    "D#4": Sound("assets/d4s.wav"),
    "E4": Sound("assets/e4.wav"),
    "F4": Sound("assets/f4.wav"),
    "F#4": Sound("assets/f4s.wav"),
    "G4": Sound("assets/g4.wav"),
    "G#4": Sound("assets/g4s.wav"),
    "A4": Sound("assets/a4.wav"),
    "A#4": Sound("assets/a4s.wav"),
    "B4": Sound("assets/b4.wav"),

    "C5": Sound("assets/c5.wav"),
}

muxmap = [
    #  0      1      2       3      4      5     6      7
    "F2",  "C2",  "G2",  "C#2", "F#2", "D#2", "E2",  "D2",  # MUX 0
    "",    "G#2", "C#3", "A2",  "C3",  "B2",  "",    "A#2", # MUX 1
    "F#3", "D3",  "G#3", "D#3", "G3",  "",    "F3",  "E3",  # MUX 2
    "",    "A3",  "",    "A#3", "",    "C4",  "",    "B3",  # MUX 2
]

# Opening sound
def play_opening_sounds():
    sounds["C3"].play()
    sleep(0.25)
    sounds["E3"].play()
    sleep(0.25)
    sounds["G3"].play()
    sleep(0.25)
    sounds["C4"].play()

play_opening_sounds()

print("Piano is ready.")

# Main loop
bs = [0] * 32
while True:
    for s in range(8):
        b = '{0:03b}'.format(s)
        for i in range(3):
            if b[i] == '1':
                signal[i].on()
            else:
                signal[i].off()

        for i in range(4):
            idx = i * 8 + s

            if mux[i].is_pressed:
                if bs[idx] < 20:
                    bs[idx] = 50
                    sounds[muxmap[idx]].stop()
                    sounds[muxmap[idx]].play()
            else:
                if bs[idx] > 0:
                    bs[idx] -= 1
                    if bs[idx] == 0:
                        sounds[muxmap[idx]].fadeout(250)  # stop() sounds weird, so fading them out...

    print(bs, end='\r')
