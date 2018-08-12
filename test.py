from time import sleep

from util.getkeys import key_check
from util.grabscreen import grab_screen
from utils import m_gameboard, reduce_gameboard, extract_gameboard
from cv2 import cvtColor, COLOR_BGR2GRAY, resize
from util.directkeys import PressNRealese
from bot import WINDOW_WIDTH, WINDOW_HEIGHT
from util.directkeys import SPACE, RIGHT, LEFT, UP, DOWN
import numpy

from keras.models import load_model

MODEL_FILE_PATH = "./data/checkpoints/model_01_0.98.hdf5"


def resolve_key_2_press(results):
    index = numpy.argmax(results)
    if index == 0:
        return UP
    elif index == 1:
        return LEFT
    elif index == 2:
        return DOWN
    elif index == 3:
        return RIGHT
    elif index == 4:
        return SPACE


def main():
    model = load_model(MODEL_FILE_PATH)
    # Countdown
    for i in list(range(4))[::-1]:
        print(i + 1)
        sleep(1)
    paused = False
    # Main loop
    while True:
        if not paused:
            # Grab screen
            screen = grab_screen(region=(0, 32, WINDOW_WIDTH, WINDOW_HEIGHT + 32))
            screen = m_gameboard(
                reduce_gameboard(extract_gameboard(screen, WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_HEIGHT),
                WINDOW_HEIGHT)
            screen = cvtColor(screen, COLOR_BGR2GRAY)
            screen = resize(screen, None, fx=0.5, fy=0.5)
            screen = screen.reshape((1,) + screen.shape + (1,))
            # Perform AI routine
            results = model.predict(screen, verbose=0)
            PressNRealese(resolve_key_2_press(results))
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('Unpaused!')
                sleep(1)
            else:
                print('Pausing!')
                paused = True
                sleep(1)


if __name__ == "__main__":
    main()
