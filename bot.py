from time import sleep, time
from cv2 import imshow, waitKey, destroyAllWindows, cvtColor, COLOR_BGR2GRAY, resize
from numpy import count_nonzero, max
from util.grabscreen import grab_screen
from utils import extract_gameboard, reduce_gameboard, m_gameboard
from util.directkeys import PressNRealese, UP, DOWN, LEFT, RIGHT, SPACE

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


# Convert index to keys, even numbers are vertical sections, odd horizontal
def convert_index_2_key(index):
    if index == 0:
        return UP
    if index == 1:
        return LEFT
    if index == 2:
        return DOWN
    if index == 3:
        return RIGHT


# Recurrent searching of the winner section
def recu_winner(boxes, top_box, bottom_box, left_box, right_box, boxes_history):
    boxes_history.append(boxes)

    # If more than one box has non zero count value
    if count_nonzero(boxes) > 1:

        # Divide all sections and consider the half of their area (nearer the center)
        top_box = top_box[:len(top_box[:, 0]) / 2, :]
        bottom_box = bottom_box[len(bottom_box[:, 0]) / 2:, :]
        left_box = left_box[:, len(left_box[0, :]) / 2:]
        right_box = right_box[:, :len(right_box[0, :]) / 2]
        boxes = [count_nonzero(top_box), count_nonzero(left_box), count_nonzero(bottom_box),
                 count_nonzero(right_box)]
        return recu_winner(boxes, top_box, bottom_box, left_box, right_box, boxes_history)
    else:
        # Return the box index with the best last score
        return boxes_history[-1].index(max(boxes_history[-1]))


def recognize_frame(frame):
    height, width = frame.shape

    # Obtain section boxes
    top_box = frame[0:(height / 6), (width / 3):(2 * width / 3)]
    bottom_box = frame[(5 * height / 6):height, (width / 3):(2 * width / 3)]
    left_box = frame[(height / 3):(2 * height / 3), 0:(width / 6)]
    right_box = frame[(height / 3):(2 * height / 3), (5 * width / 6):width]

    # Count how many pixels are not black in each section
    boxes = [count_nonzero(top_box), count_nonzero(left_box), count_nonzero(bottom_box),
             count_nonzero(right_box)]
    winner = max(boxes)

    # If sections are clear, probably we should start the game (space in during playing do nothing)
    if winner <= 0:
        return SPACE
    else:
        boxes_history = []
        return convert_index_2_key(recu_winner(boxes, top_box, bottom_box, left_box, right_box, boxes_history))


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
        screen = cvtColor(screen, COLOR_BGR2GRAY)
        # Perform bot routine
        PressNRealese(recognize_frame(screen))

        print('Frame took {} seconds'.format(time() - last_time))
        last_time = time()

        # View frame
        # screen = resize(screen, None, fx=0.75, fy=0.75)
        # imshow('window', screen)
        #
        # if waitKey(1) & 0xFF == ord('q'):
        #     destroyAllWindows()
        #     break


if __name__ == '__main__':
    main()
