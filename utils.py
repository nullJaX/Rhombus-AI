import cv2
import numpy as np


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
    mask = np.zeros(image.shape[:2], np.uint8)
    mask[WINDOW_HEIGHT/8:3*WINDOW_HEIGHT/8, :] = 255
    mask[:, WINDOW_HEIGHT / 8:3 * WINDOW_HEIGHT / 8] = 255
    mask = 255 - mask
    images = cv2.bitwise_and(image,image, dst=image, mask=mask)
    return images
