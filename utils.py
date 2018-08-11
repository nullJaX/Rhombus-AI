from cv2 import getRotationMatrix2D, Canny, line, bitwise_and, FILLED, rectangle, warpAffine
from numpy import ones, float32, uint8
from numpy.ma import sqrt


# Extract only rhombus
def extract_gameboard(image, window_width, window_height):
    m = float32([[1, 0, -(window_width - window_height) / 2], [0, 1, 0]])
    image = warpAffine(image, m, (window_height, window_height))
    edges = Canny(image, 100, 200)
    image = bitwise_and(image, image, mask=edges)
    return image


# Extract the main square inside rhombus
def reduce_gameboard(image, window_height):
    m = float32([[1, 0, -window_height / 4], [0, 1, -window_height / 4]])
    image = warpAffine(image, m, (int(window_height / 2), int(window_height / 2)))
    return image


# Hide unnecessary contours
def m_gameboard(image, window_height):
    height, width, _ = image.shape

    rect_x1 = int(width / 2 - (width / (1.5 * sqrt(2))))
    rect_x2 = int(width / 2 + (width / (1.5 * sqrt(2))))
    rect_y1 = int(height / 2 - (height / (1.5 * sqrt(2))))
    rect_y2 = int(height / 2 + (height / (1.5 * sqrt(2))))

    mask = ones(image.shape, uint8) * 255
    rectangle(mask, (int(width/4 + rect_x1/2), int(height/4 + rect_y1/2)), (int(width/4 + rect_x2/2), int(height/4 + rect_y2/2)), (0, 0, 0), FILLED)
    mask = warpAffine(mask, getRotationMatrix2D((int(width / 2), int(height / 2)), 45, 1.0), (height, width))
    rectangle(mask, (0, 0), (int(window_height / 2), int(window_height / 2)), (0, 0, 0), thickness=int(window_height / 24))
    image = bitwise_and(image, mask)
    return image


# Hide unnecessary contours (Alignment)
def m_gameboard_4_debug(image, window_height):
    height, width, _ = image.shape
    mask = ones(image.shape, uint8) * 255
    rectangle(mask, (int(width / 2) - int(width / 8), int(height / 2) - int(height / 8)),
              (int(width / 2) + int(width / 8), int(height / 2) + int(height / 8)), (0, 0, 0), FILLED)
    mask = warpAffine(mask, getRotationMatrix2D((int(width / 2), int(height / 2)), 45, 1.0), (height, width))
    rectangle(mask, (0, 0), (int(window_height / 2), int(window_height / 2)), (0, 0, 0), thickness=int(window_height / 24))
    image = bitwise_and(image, mask)
    return image


# Draw cross and search areas for alignment
def draw_search_areas(image):
    height, width, _ = image.shape
    rectangle(image, (int(width / 3), 0), (int(2 * width / 3), int(height / 6)), (255, 0, 0))  # top
    rectangle(image, (int(width / 3), int(5*height/6)), (int(2 * width / 3), height), (255, 0, 0))  # bottom
    rectangle(image, (0, int(height / 3)), (int(width / 6), int(2 * height / 3)), (255, 0, 0))  # left
    rectangle(image, (int(5 * width / 6), int(height / 3)), ( width , int(2 * height / 3)), (255, 0, 0))  # right
    line(image, (0, int(height / 2)), (width, int(height / 2)), (0, 255, 0))
    line(image, (int(width / 2), 0), (int(width / 2), height), (0, 255, 0))
    return image
