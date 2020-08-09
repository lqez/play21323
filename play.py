from gpiozero import Button
import pygame.mixer
from pygame.mixer import Sound
from signal import pause

# low buffer for shorter latency
pygame.mixer.init(22050, -8, 2, 256)

buttons = {
    Button("BOARD29", pull_up=False): {
        "name": "C3", "sound": Sound("assets/c3.wav"),
    },
    Button("BOARD31", pull_up=False): {
        "name": "C3#", "sound": Sound("assets/c3s.wav"),
    },
    Button("BOARD33", pull_up=False): {
        "name": "D3", "sound": Sound("assets/d3.wav"),
    },
    Button("BOARD35", pull_up=False): {
        "name": "D3#", "sound": Sound("assets/d3s.wav"),
    },
    Button("BOARD37", pull_up=False): {
        "name": "E3", "sound": Sound("assets/e3.wav"),
    },
}

def pressed(button):
    btn = buttons[button]
    print("Playing", btn["name"])
    btn["sound"].play()


def released(button):
    btn = buttons[button]
    btn["sound"].fadeout(250)  # stop() sounds weird, so fading them out...

def main():
    for button in buttons.keys():
        button.when_pressed = pressed
        button.when_released = released

    print("Now you can play the piano...")
    pause()

if __name__ == "__main__":
    main()
