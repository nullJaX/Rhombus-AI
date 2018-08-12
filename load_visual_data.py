from time import sleep, time
from cv2 import imshow, waitKey, destroyAllWindows, resize
from util.grabscreen import grab_screen
from utils import extract_gameboard, reduce_gameboard, draw_search_areas, m_gameboard_4_debug

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():
    # Countdown
    for i in list(range(4))[::-1]:
        print(i + 1)
        sleep(1)
    last_time = time()

    # Main loop
    while True:
        screen = grab_screen(region=(0, 32, WINDOW_WIDTH, WINDOW_HEIGHT + 32))
        screen = extract_gameboard(screen, WINDOW_WIDTH, WINDOW_HEIGHT)
        screen = reduce_gameboard(screen, WINDOW_HEIGHT)
        screen = m_gameboard_4_debug(screen, WINDOW_HEIGHT)

        # For alignment purposes
        screen = draw_search_areas(screen)

        screen = resize(screen, None, fx=0.75, fy=0.75)

        print('Frame took {} seconds'.format(time() - last_time))
        last_time = time()
        imshow('window', screen)

        if waitKey(1) & 0xFF == ord('q'):
            destroyAllWindows()
            break


if __name__ == '__main__':
    main()
