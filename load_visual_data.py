from util.grabscreen import grab_screen
import utils
import time
import cv2

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    while True:
        screen = cv2.cvtColor(grab_screen(region=(0, 32, WINDOW_WIDTH, WINDOW_HEIGHT+32)), cv2.COLOR_BGR2RGB)
        screen = utils.extract_gameboard(screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen = utils.reduce_gameboard(screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen = utils.m_gameboard(screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen = utils.draw_search_areas(screen)
        screen = cv2.resize(screen, None, fx=0.75, fy=0.75)
        print('Frame took {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        cv2.imshow('window', screen)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


main()
