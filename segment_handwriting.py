import cv2
import os
import numpy as np

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to your image (relative to script directory)
image_path = os.path.join(script_dir, 'Input Images', 'sample.jpg')  # Change to your file name

# Load the image
image = cv2.imread(image_path)

# Check if the image loaded successfully
if image is None:
    print("Error: Image file not found or couldn't be opened.")
else:
    # Convert to grayscale (removes color, only intensity stays)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarize image using Otsu's method (automatically finds best threshold)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # (THRESH_BINARY_INV makes handwriting white, background black—good for finding contours)

    # Show result
    cv2.imshow('Grayscale', gray)
    cv2.imshow('Binarized', binary)
    print("Press any key to close.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Optional: Save for inspection
    out_path = os.path.join(script_dir, 'Output Glyphs', 'binarized_preview.png')
    cv2.imwrite(out_path, binary)
    print(f'Binarized image saved to {out_path}')

    kernel = np.ones((3, 3), np.uint8)

    # Apply morphological closing to fill small gaps
    binary_fixed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Now use binary_fixed in place of binary for the rest of the steps!
    contours, _ = cv2.findContours(binary_fixed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left-to-right, top-to-bottom for natural order
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
    contours_sorted = [cnt for _, cnt in sorted(zip(bounding_boxes, contours), key=lambda b: (b[0][1], b[0][0]))]

    # Loop through contours and extract each character as a separate image
    output_dir = os.path.join(script_dir, "output_glyphs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    for i, cnt in enumerate(contours_sorted):
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 and h > 10:  # Filter out very small noise
            char_img = binary_fixed[y:y+h, x:x+w]
            output_file = os.path.join(output_dir, f'char_{i+1}.png')
            cv2.imwrite(output_file, char_img)
            print(f'Saved {output_file}')


    # Optional: Draw rectangles and show result for visualization
    image_copy = image.copy()
    for cnt in contours_sorted:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 and h > 10:
            cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0,255,0), 2)
            
    cv2.imshow('Segmented Letters', image_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


