import cv2
import numpy as np

CROSS_SIZE = 128


def extract_gameboard(image, (WINDOW_WIDTH, WINDOW_HEIGHT)):
    M = np.float32([[1, 0, -(WINDOW_WIDTH - WINDOW_HEIGHT) / 2], [0, 1, 0]])
    image = cv2.warpAffine(image, M, (WINDOW_HEIGHT, WINDOW_HEIGHT))
    edges = cv2.Canny(image, 100, 200)
    image = cv2.bitwise_and(image, image, mask=edges)
    return image


def reduce_gameboard(image, (WINDOW_WIDTH, WINDOW_HEIGHT)):
    M = np.float32([[1, 0, -WINDOW_HEIGHT / 4], [0, 1, -WINDOW_HEIGHT / 4]])
    image = cv2.warpAffine(image, M, (WINDOW_HEIGHT / 2, WINDOW_HEIGHT / 2))
    return image


def m_gameboard(image, (WINDOW_WIDTH, WINDOW_HEIGHT)):
    width, height, _ = image.shape
    mask = np.ones(image.shape, np.uint8) * 255
    cv2.rectangle(mask, (width / 2 - width / 8, height / 2 - height / 8),
                  (width / 2 + width / 8, height / 2 + height / 8), (0, 0, 0), cv2.FILLED)
    mask = cv2.warpAffine(mask, cv2.getRotationMatrix2D((width / 2, height / 2), 45, 1.0), (height, width))
    cv2.rectangle(mask, (0, 0), (WINDOW_HEIGHT / 2, WINDOW_HEIGHT / 2), (0, 0, 0), thickness=WINDOW_HEIGHT / 24)
    image = cv2.bitwise_and(image, mask)
    return image

def draw_search_areas(image):
    width, height, _ = image.shape
    cv2.rectangle(image, (width / 3, height/8), (2 * width / 3, height / 4), (255, 0, 0))
    cv2.rectangle(image, (width / 3, 3 * height / 4), (2 * width / 3, 7*height/8), (255, 0, 0))
    cv2.rectangle(image, (width / 8, height / 3), (width / 4, 2 * height / 3), (255, 0, 0))
    cv2.rectangle(image, (3 * width / 4, height / 3), (7*width/8, 2 * height / 3), (255, 0, 0))
    cv2.line(image, (0, height / 2), (width, height / 2), (0, 255, 0))
    cv2.line(image, (width / 2, 0), (width / 2, height), (0, 255, 0))
    return image