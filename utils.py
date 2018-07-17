from cv2 import getRotationMatrix2D, Canny, line, bitwise_and, FILLED, rectangle, warpAffine
from numpy import ones, float32, uint8


# Extract only rhombus
def extract_gameboard(image, (window_width, window_height)):
    m = float32([[1, 0, -(window_width - window_height) / 2], [0, 1, 0]])
    image = warpAffine(image, m, (window_height, window_height))
    edges = Canny(image, 100, 200)
    image = bitwise_and(image, image, mask=edges)
    return image


# Extract the main square inside rhombus
def reduce_gameboard(image, window_height):
    m = float32([[1, 0, -window_height / 4], [0, 1, -window_height / 4]])
    image = warpAffine(image, m, (window_height / 2, window_height / 2))
    return image


# Hide unnecessary contours
def m_gameboard(image, window_height):
    width, height, _ = image.shape
    mask = ones(image.shape, uint8) * 255
    rectangle(mask, (width / 2 - width / 8, height / 2 - height / 8),
              (width / 2 + width / 8, height / 2 + height / 8), (0, 0, 0), FILLED)
    mask = warpAffine(mask, getRotationMatrix2D((width / 2, height / 2), 45, 1.0), (height, width))
    rectangle(mask, (0, 0), (window_height / 2, window_height / 2), (0, 0, 0), thickness=window_height / 24)
    image = bitwise_and(image, mask)
    return image


# Draw cross and search areas for alignment
def draw_search_areas(image):
    width, height, _ = image.shape
    rectangle(image, (width / 3, height / 8), (2 * width / 3, height / 4), (255, 0, 0))
    rectangle(image, (width / 3, 3 * height / 4), (2 * width / 3, 7 * height / 8), (255, 0, 0))
    rectangle(image, (width / 8, height / 3), (width / 4, 2 * height / 3), (255, 0, 0))
    rectangle(image, (3 * width / 4, height / 3), (7 * width / 8, 2 * height / 3), (255, 0, 0))
    line(image, (0, height / 2), (width, height / 2), (0, 255, 0))
    line(image, (width / 2, 0), (width / 2, height), (0, 255, 0))
    return image
