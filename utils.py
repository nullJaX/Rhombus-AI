from cv2 import getRotationMatrix2D, Canny, line, bitwise_and, FILLED, rectangle, warpAffine
from numpy import ones, float32, uint8, sqrt


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

    rect_x1 = int(width / 2 - (width / (1.5 * sqrt(2))))
    rect_x2 = int(width / 2 + (width / (1.5 * sqrt(2))))
    rect_y1 = int(height / 2 - (height / (1.5 * sqrt(2))))
    rect_y2 = int(height / 2 + (height / (1.5 * sqrt(2))))

    mask = ones(image.shape, uint8) * 255
    rectangle(mask, (width/4 + rect_x1/2, height/4 + rect_y1/2), (width/4 + rect_x2/2, height/4 + rect_y2/2), (0, 0, 0), FILLED)
    mask = warpAffine(mask, getRotationMatrix2D((width / 2, height / 2), 45, 1.0), (height, width))
    rectangle(mask, (0, 0), (window_height / 2, window_height / 2), (0, 0, 0), thickness=window_height / 24)
    image = bitwise_and(image, mask)
    return image


# Hide unnecessary contours (Alignment)
def m_gameboard_4_debug(image, window_height):
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
    rectangle(image, (width / 3, 0), (2 * width / 3, height / 6), (255, 0, 0))  # top
    rectangle(image, (width / 3, 5*height/6), (2 * width / 3, height), (255, 0, 0))  # bottom
    rectangle(image, (0, height / 3), (width / 6, 2 * height / 3), (255, 0, 0))  # left
    rectangle(image, (5 * width / 6, height / 3), ( width , 2 * height / 3), (255, 0, 0))  # right
    line(image, (0, height / 2), (width, height / 2), (0, 255, 0))
    line(image, (width / 2, 0), (width / 2, height), (0, 255, 0))
    return image
