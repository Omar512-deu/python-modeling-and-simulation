import cv2
import numpy as np

WINDOW_NAME = 'Select Plate '

def select_roi_with_mouse_local(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return None

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    print(f"Draw a box around the plate in the new window.")
    print(f"  - Press ENTER or SPACE to confirm selection.")
    print(f"  - Press ESC to cancel selection.")

    box = cv2.selectROI(WINDOW_NAME, img, showCrosshair=False, fromCenter=False)
    cv2.destroyWindow(WINDOW_NAME)

    x, y, w, h = box

    if w > 0 and h > 0:
        return [int(x), int(y), int(w), int(h)]
    else:
        print("Selection cancelled or invalid.")
        return None


def analyze_plate(image_path):
    rect = select_roi_with_mouse_local(image_path)

    if rect is None:
        return

    x, y, w, h = rect

    if w < 5 or h < 5:
        print("Selection is too small! Please draw a larger bounding box.")
        return

    print(f"Selected Region: x={x}, y={y}, w={w}, h={h}")

    img = cv2.imread(image_path)

    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return

    y = max(0, y)
    x = max(0, x)
    h = min(h, img.shape[0] - y)
    w = min(w, img.shape[1] - x)

    plate_img = img[y:y + h, x:x + w]

    p_height, p_width, _ = plate_img.shape

    if p_height < 3:
        print("Error: Plate height is too small for header analysis.")
        return

    header_img = plate_img[0:int(p_height / 3), :]

    avg_color = np.average(np.average(header_img, axis=0), axis=0)

    if avg_color.size == 0:
        print("Error: Header image is empty.")
        return

    blue, green, red = avg_color[0], avg_color[1], avg_color[2]

    plate_type = "Unknown, please try again."

    if blue > red and blue > green:
        plate_type = "Malaaky (Private)"
    elif red > blue and green > 90:
        plate_type = "Ogra (Taxi/Hire)"
    elif red > blue and green < 90:
        plate_type = "Naql (Transport)"

    print(f"----------------------------------------")
    print(f"Final Result: {plate_type}")
    print(f"Color Avg: B={int(blue)}, G={int(green)}, R={int(red)}")
    print(f"----------------------------------------")

analyze_plate('m1.png')