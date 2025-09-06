import cv2
import time
import os

# Make sure output folder exists
output_folder = "imgs/"
os.makedirs(output_folder, exist_ok=True)

# Open camera (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

frame_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Build filename
        filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(filename, frame)  # Save frame
        print(f"Saved {filename}")

        frame_count += 1

        # Optional: capture every 0.5 seconds
        time.sleep(1.0)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    cap.release()
    print("Camera released")
