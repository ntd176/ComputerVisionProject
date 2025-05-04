import cv2
import numpy as np

def read_image(filepath):
    image = cv2.imread(filepath)
    return image

# -------------------------------------------------------------------
'''
TIEN XU LY ANH
'''
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
    return binary

# -------------------------------------------------------------------
'''
TIM DUONG VIEN LON NHAT ANH NHI PHAN
'''
def find_largest_contour(binary_image):
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    return largest_contour

# -------------------------------------------------------------------
'''
XAC DINH GOC TU DUONG VIEN
'''
def get_corners_from_contour(contour):
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    corners = np.squeeze(approx)
    return corners

# -------------------------------------------------------------------
'''
SAP XEP LAI THU TU GOC
'''
def sort_corners(corners):
    rect = np.zeros((4, 2), dtype="float32")
    s = corners.sum(axis=1)
    diff = np.diff(corners, axis=1)
    rect[0] = corners[np.argmin(s)]     # Top-left
    rect[2] = corners[np.argmax(s)]     # Bottom-right
    rect[1] = corners[np.argmin(diff)]  # Top-right
    rect[3] = corners[np.argmax(diff)]  # Bottom-left
    return rect

# -------------------------------------------------------------------
'''
BIEN DOI PHOI CANH
'''
def perform_perspective_transform(image, corners):
    rect = sort_corners(corners)
    width_a = np.linalg.norm(rect[2] - rect[3])
    width_b = np.linalg.norm(rect[1] - rect[0])
    max_width = max(int(width_a), int(width_b))
    height_a = np.linalg.norm(rect[1] - rect[2])
    height_b = np.linalg.norm(rect[0] - rect[3])
    max_height = max(int(height_a), int(height_b))

    dst_corners = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")

    homography_matrix = cv2.getPerspectiveTransform(rect, dst_corners)
    warped = cv2.warpPerspective(image, homography_matrix, (max_width, max_height))
    return warped

# -------------------------------------------------------------------
'''
LAM SAC NET ANH
'''
def sharpen_image(image):
    sharpen_kernel = np.array([[0, -1, 0],
                                [-1, 8, -1],
                                [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, sharpen_kernel)
    return sharpened

# -------------------------------------------------------------------

if __name__ == "__main__":
    distorted_image_path = r"E:\Computer Vision\CuoiKyProject\21200274\distorted_qrcode2.png"
    recovered_image_path = r"E:\Computer Vision\CuoiKyProject\21200274\recovered_qrcode2.png"
    image = read_image(distorted_image_path)
    binary_image = preprocess_image(image)
    largest_contour = find_largest_contour(binary_image)
    corners = get_corners_from_contour(largest_contour)
    straightened_image = perform_perspective_transform(image, corners)
    straightened_gray = cv2.cvtColor(straightened_image, cv2.COLOR_BGR2GRAY)
    sharpened_image = sharpen_image(straightened_gray)
    _, binary_output = cv2.threshold(sharpened_image, 180, 255, cv2.THRESH_BINARY)
    cv2.imwrite(recovered_image_path, binary_output)
    cv2.imshow("Distorted Image", image)
    cv2.imshow("Recovered Image", binary_output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()