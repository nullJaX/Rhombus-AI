from time import sleep, time
import cv2
import numpy as np
from util.grabscreen import grab_screen
from utils import extract_gameboard, reduce_gameboard, m_gameboard
from util.directkeys import PressNRealese, UP, DOWN, LEFT, RIGHT, SPACE

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def recognize_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = frame.shape
    top_box = np.count_nonzero(frame[0:(height / 6), (width / 3):(2 * width / 3)])
    bottom_box = np.count_nonzero(frame[(5 * height / 6):height, (width / 3):(2 * width / 3)])
    left_box = np.count_nonzero(frame[(height / 3):(2 * height / 3), 0:(width / 6)])
    right_box = np.count_nonzero(frame[(height / 3):(2 * height / 3), (5 * width / 6):width])
    winner = np.max([top_box, bottom_box, left_box, right_box])

    if winner <= 0:
        return SPACE
    else:
        index = [top_box, bottom_box, left_box, right_box].index(winner)
        if index == 0:
            return UP
        if index == 1:
            return DOWN
        if index == 2:
            return LEFT
        if index == 3:
            return RIGHT


def main():
    # Countdown
    for i in list(range(4))[::-1]:
        print(i + 1)
        sleep(1)
    last_time = time()

    # Main loop
    while True:
        # Grab screen
        screen = grab_screen(region=(0, 32, WINDOW_WIDTH, WINDOW_HEIGHT + 32))
        screen = m_gameboard(reduce_gameboard(extract_gameboard(screen, (WINDOW_WIDTH, WINDOW_HEIGHT)), WINDOW_HEIGHT),
                             WINDOW_HEIGHT)

        # Perform bot routine
        key = recognize_frame(screen)
        PressNRealese(key)

        # View frame
        screen = cv2.resize(screen, None, fx=0.75, fy=0.75)
        print('Frame took {} seconds'.format(time() - last_time))
        last_time = time()
        cv2.imshow('window', screen)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
