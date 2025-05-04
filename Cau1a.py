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
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
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
KHOI PHUC PHOI CANH
'''

def get_perspective_transform(image, contour):
    epsilon = 0.05 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    if len(approx) != 4:
        raise ValueError('Cannot find QR code corners')

    pts_src = np.array([point[0] for point in approx], dtype='float32')
    
    width = max(np.linalg.norm(pts_src[0] - pts_src[1]), np.linalg.norm(pts_src[2] - pts_src[3]))
    height = max(np.linalg.norm(pts_src[0] - pts_src[3]), np.linalg.norm(pts_src[1] - pts_src[2]))
    
    pts_dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype='float32')
    
    M = cv2.getPerspectiveTransform(pts_src, pts_dst)
    warped_image = cv2.warpPerspective(image, M, (int(width), int(height)))
    
    return warped_image

# -------------------------------------------------------------------
'''
GHI ANH
'''
def write_image(filepath, image):
    cv2.imwrite(filepath, image)

# -------------------------------------------------------------------

if __name__ == "__main__":
    distorted_image_path = r"E:\Computer Vision\CuoiKyProject\21200274\distorted_qrcode1.png"
    recovered_image_path = r"E:\Computer Vision\CuoiKyProject\21200274\recovered_qrcode1.png"
    image = read_image(distorted_image_path)
    binary_image = preprocess_image(image)
    largest_contour = find_largest_contour(binary_image)
    recovered_qr = get_perspective_transform(image, largest_contour)
    write_image(recovered_image_path, recovered_qr)
    cv2.imshow("Distorted Image", image)
    cv2.imshow("Recovered Image", recovered_qr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()