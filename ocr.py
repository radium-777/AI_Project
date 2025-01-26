import numpy as np
import cv2
import easyocr

reader = easyocr.Reader(["en"])

def calculate_centroid(bbox):
    x_coords = [point[0] for point in bbox]
    y_coords = [point[1] for point in bbox]
    return np.mean(x_coords), np.mean(y_coords)

def do_ocr(file):
    try:
        file_bytes = file.read()

        #if not file_bytes:
         #   raise Exception("File is empty.")

        #if not file.content_type.startswith("image/"):
         #   raise Exception("Not an image.")

        # Decode image bytes to a Numpy array
        nparr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise Exception("Failed to decode image.")
        
        # Process the image directly from bytes
        results = reader.readtext(file_bytes)

        # Filter out unconfident results
        results = [(bbox, text, conf) for (bbox, text, conf) in results if conf > 0.6]

        # Add centroids to the results for sorting
        results_with_centroids = []
        for result in results:
            bbox, text, confidence = result
            centroid = calculate_centroid(bbox)
            results_with_centroids.append((centroid, text, confidence, bbox))

        # Sort by top-to-bottom and left-to-right
        sorted_results = sorted(
            results_with_centroids,
            key=lambda x: (
                x[0][1],
                x[0][0],
            ),  # First sort by y (top-to-bottom), then by x (left-to-right)
        )

        extracted_text = [result[1] for result in sorted_results]
        text = " ".join(extracted_text)
    except Exception as e:
        print(f"Error during OCR: {str(e)}")
        raise Exception(f"Error during OCR: {str(e)}")

    # Parse OCR result
    return {"text": text}