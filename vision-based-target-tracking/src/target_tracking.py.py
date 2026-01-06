import cv2
import numpy as np

# Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get frame dimensions
    h, w, _ = frame.shape
    screen_center_x = w // 2

    # Convert BGR image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color range in HSV
    lower_red = (0, 120, 70)
    upper_red = (10, 255, 255)

    # Create binary mask for red color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Noise removal using morphological opening
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Find contours from the mask
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    largest_contour = None
    max_area = 0

    # Select the largest contour (target)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            largest_contour = cnt

    # Check if a valid target exists
    if largest_contour is not None and max_area > 100:
        x, y, w_box, h_box = cv2.boundingRect(largest_contour)

        # Target center coordinates
        cx = x + w_box // 2
        cy = y + h_box // 2

        # Draw bounding box and target center
        cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        # Horizontal error calculation
        error = cx - screen_center_x
        tolerance = 20

        # Decision logic based on error
        if error > tolerance:
            decision = "Yaw Right"
            color = (0, 0, 255)
        elif error < -tolerance:
            decision = "Yaw Left"
            color = (255, 0, 0)
        else:
            decision = "Centered"
            color = (0, 255, 0)

        # Display decision on screen
        cv2.putText(
            frame,
            decision,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2
        )

        # Display error value
        cv2.putText(
            frame,
            f"Error: {error}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # Draw reference center line
    cv2.line(
        frame,
        (screen_center_x, 0),
        (screen_center_x, h),
        (255, 255, 0),
        2
    )

    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

        