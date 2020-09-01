from gpiozero import DigitalOutputDevice, DigitalInputDevice
from gpiozero import Button, LED
from time import sleep
import pygame.mixer
from pygame.mixer import Sound
from enum import Enum


PRESS_DELAY = 8
PRESS_THRESHOLD = 2

class STATE(Enum):
    NORMAL = 0
    RECORDING = 1
    PLAYING = 2

state = STATE.NORMAL
tick = 0
note = 0
record = []

# low buffer for shorter latency
pygame.mixer.init(44100, -8, 1, 256)

# Mux selector
signals = [
    LED('BOARD15'),
    LED('BOARD13'),
    LED('BOARD11'),
]

# Muxes are connected to each touch sensor
muxes = [
    Button('BOARD29', pull_up=False),
    Button('BOARD31', pull_up=False),
    Button('BOARD33', pull_up=False),
    Button('BOARD35', pull_up=False),
]

buttons = {
    "play": Button('BOARD38', pull_up=False),
    "sound": Button('BOARD36', pull_up=False),
    "record": Button('BOARD32', pull_up=False),
}

leds = {
    "playing": LED('BOARD37'),
    "recording": LED('BOARD40'),
}

voices = {
    "piano": Sound("assets/piano.wav"),
    "vibraphone": Sound("assets/vibraphone.wav"),
    "organ": Sound("assets/organ.wav"),
    "rec_start": Sound("assets/rec_start.wav"),
    "rec_end": Sound("assets/rec_end.wav"),
}

instruments = ["piano", "vibraphone", "organ"]
ins_current = 0

notemap = {
    "": None,

    "C2": "c2", "C#2": "c2s", "D2": "d2", "D#2": "d2s", "E2": "e2",
    "F2": "f2", "F#2": "f2s", "G2": "g2", "G#2": "g2s", "A2": "a2", "A#2": "a2s", "B2": "b2",

    "C3": "c3", "C#3": "c3s", "D3": "d3", "D#3": "d3s", "E3": "e3",
    "F3": "f3", "F#3": "f3s", "G3": "g3", "G#3": "g3s", "A3": "a3", "A#3": "a3s", "B3": "b3",

    "C4": "c4",
}

muxmap = [
    #  0      1      2       3      4      5     6      7
    "F2",  "C2",  "G2",  "C#2", "F#2", "D#2", "E2",  "D2",  # MUX 0
    "",    "G#2", "C#3", "A2",  "C3",  "B2",  "",    "A#2", # MUX 1
    "F#3", "D3",  "G#3", "D#3", "G3",  "",    "F3",  "E3",  # MUX 2
    "",    "A3",  "",    "A#3", "",    "C4",  "",    "B3",  # MUX 2
]

print("Loading sounds...")

sounds = {
    ins: {k: Sound(f"assets/{ins}/{v}.wav") if v else None for (k, v) in notemap.items()}
        for ins in instruments
}


def get_instrument(ins):
    voices[instruments[ins]].play()
    return [sounds[instruments[ins]][_] for _ in muxmap]

def reset():
    # turn off leds
    [led.off() for (name, led) in leds.items()]

    # reset mux signal
    for s in range(8):
        b = '{0:03b}'.format(s)
        for i in range(3):
            if b[i] == '1':
                signals[i].on()
            else:
                signals[i].off()

        for i in range(4):
            if muxes[i].is_pressed:
                print("mux", i, "pressed at", b)

def btn_sound_pressed():
    global sndmuxmap, ins_current
    ins_current = (ins_current + 1) % len(instruments)
    print("Change sound to", instruments[ins_current])
    sndmuxmap = get_instrument(ins_current)

def btn_play_pressed():
    if state == STATE.PLAYING:
        stop_playing()
    else:
        start_playing()

def btn_record_pressed():
    if state == STATE.RECORDING:
        stop_recording()
    else:
        start_recording()

def start_recording():
    global state
    if state == STATE.PLAYING:
        stop_playing()

    voices["rec_start"].play()
    print("> start recording")
    state = STATE.RECORDING
    leds['recording'].on()

    global record, tick
    record = []
    tick = 0

def stop_recording():
    global state
    voices["rec_end"].play()
    print("> stop recording")
    if len(record) > 0:
        print(">", len(record), "notes were recorded")
    state = STATE.NORMAL
    leds['recording'].off()

def start_playing():
    global state
    if state == STATE.RECORDING:
        stop_recording()

    print("> start playing")
    state = STATE.PLAYING
    leds['playing'].on()

    global tick, note
    tick = note = 0
    # move to the first note tick with a bit delay
    if len(record) > 0:
        tick = record[0][0] - 24

def stop_playing():
    global state, vs
    print("> stop playing")
    state = STATE.NORMAL
    leds['playing'].off()
    vs = [0] * 32


# Prepare
sndmuxmap = get_instrument(ins_current)
reset()
buttons["sound"].when_pressed = btn_sound_pressed
buttons["play"].when_pressed = btn_play_pressed
buttons["record"].when_pressed = btn_record_pressed

print("Piano is ready.")

# Main loop
bs = [0] * 32
vs = [0] * 32

while True:
    on = []
    off = []

    # piano keys
    for s in range(8):
        b = '{0:03b}'.format(s)
        for i in range(3):
            if b[i] == '1':
                signals[i].on()
            else:
                signals[i].off()

        for i in range(4):
            idx = i * 8 + s
            sound = sndmuxmap[idx]

            if not sound:
                continue

            if muxes[i].is_pressed or vs[idx] == 1:
                if bs[idx] < PRESS_THRESHOLD:
                    bs[idx] = PRESS_DELAY
                    sound.stop()
                    sound.play()
                    on.append(idx)
            else:
                if bs[idx] > 0:
                    bs[idx] -= 1
                    if bs[idx] == 0:
                        sound.fadeout(250)  # stop() sounds weird, so fading them out...
                        off.append(idx)

    print(tick, bs, end='\r')

    if state == STATE.RECORDING:
        if len(on) + len(off) > 0:
            record.append([tick, on, off])
        tick += 1
    elif state == STATE.PLAYING:
        if len(record) <= note:
            stop_playing()
        else:
            if record[note][0] <= tick:
                # on
                for idx in record[note][1]:
                    vs[idx] = 1
                # off
                for idx in record[note][2]:
                    vs[idx] = 0
                note += 1
        tick += 1
