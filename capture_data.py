from os import path
from time import sleep
from numpy import load, save
from cv2 import cvtColor, COLOR_BGR2GRAY, resize
from bot import WINDOW_HEIGHT, WINDOW_WIDTH, recognize_frame
from util.directkeys import UP, DOWN, LEFT, RIGHT, SPACE
from util.getkeys import key_check
from util.grabscreen import grab_screen
from utils import extract_gameboard, reduce_gameboard, m_gameboard

LEVEL = "EASY"
FILENAME = "./data/capture/training_data_{}.npy".format(LEVEL)


def obtain_result_array(result):
    output = [0] * 5
    if result == UP:
        output[0] = 1
        return output
    elif result == LEFT:
        output[1] = 1
        return output
    elif result == DOWN:
        output[2] = 1
        return output
    elif result == RIGHT:
        output[3] = 1
        return output
    elif result == SPACE:
        output[4] = 1
        return output


def main():
    # Check if file present
    if path.isfile(FILENAME):
        print("File exists, loading and appending previous data.")
        training_data = list(load(FILENAME))
    else:
        print("Creating new file!")
        training_data = []

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
                reduce_gameboard(extract_gameboard(screen, (WINDOW_WIDTH, WINDOW_HEIGHT)), WINDOW_HEIGHT),
                WINDOW_HEIGHT)
            screen = cvtColor(screen, COLOR_BGR2GRAY)
            # Perform bot routine
            output = obtain_result_array(recognize_frame(screen))
            screen = resize(screen, None, fx=0.5, fy=0.5)
            training_data.append([screen, output])
            if len(training_data) % 1000 == 0:
                print("Captured data: " + str(len(training_data)) + ". Saving data!")
                save(FILENAME, training_data)

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


if __name__ == '__main__':
    main()
