

import cv2
import numpy as np
from cvzone.FaceMeshModule import FaceMeshDetector
import time
import os

def calculate_ear(eye_points):
    """Calculates the Eye Aspect Ratio (EAR) from eye landmarks."""
    vertical = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[1]))
    horizontal = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[3]))
    ear = vertical / horizontal if horizontal != 0 else 0
    return ear

def draw_eye_overlay(image, points, color=(0, 255, 0)):
    """Draws a line between two key points to visualize EAR tracking."""
    cv2.line(image, points[0], points[1], color, 2)
    for pt in points:
        cv2.circle(image, pt, 2, color, -1)

def detect_blink_rate(video_path):
    """Detects the number of blinks in a video using Eye Aspect Ratio (EAR)."""
    # Initialize detector and video
    detector = FaceMeshDetector(maxFaces=1)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Could not open video file: {video_path}")
        return 0, "Video loading failed."

    # Constants
    LEFT_EYE = [159, 145, 33, 133]
    RIGHT_EYE = [386, 374, 362, 263]
    EAR_THRESHOLD = 0.2
    MIN_FRAMES_FOR_BLINK = 3
    BLINK_THRESHOLD = 15

    # Tracking variables
    blink_frame_count = 0
    total_blinks = 0
    frame_number = 0
    start_time = time.time()

    print(f"[INFO] Starting blink detection for: {video_path}")

    while True:
        success, img = cap.read()
        if not success:
            break

        frame_number += 1
        img, faces = detector.findFaceMesh(img)

        if faces:
            face = faces[0]

            if len(face) > max(max(LEFT_EYE), max(RIGHT_EYE)):
                left_eye = [face[i] for i in LEFT_EYE]
                right_eye = [face[i] for i in RIGHT_EYE]

                left_ear = calculate_ear(left_eye)
                right_ear = calculate_ear(right_eye)

                avg_ear = (left_ear + right_ear) / 2

                # Draw overlays
                draw_eye_overlay(img, left_eye, color=(0, 255, 0))
                draw_eye_overlay(img, right_eye, color=(255, 0, 0))

                # Display EAR on frame
                cv2.putText(img, f'EAR: {avg_ear:.2f}', (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 255), 2)

                # Blink detection logic
                if avg_ear < EAR_THRESHOLD:
                    blink_frame_count += 1
                else:
                    if blink_frame_count >= MIN_FRAMES_FOR_BLINK:
                        total_blinks += 1
                        print(f"[DEBUG] Blink #{total_blinks} at frame {frame_number}")
                    blink_frame_count = 0

        # Resize and display
        img = cv2.resize(img, (640, 360))
        cv2.imshow("Blink Detection", img)

        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Manual exit triggered.")
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

    elapsed = time.time() - start_time
    print(f"[INFO] Processing complete in {elapsed:.2f} seconds.")
    print(f"[INFO] Total Blinks Detected: {total_blinks}")

    # Final result message
    if total_blinks < BLINK_THRESHOLD:
        return total_blinks, " Blink rate is below threshold! Possible fatigue or drowsiness."
    else:
        return total_blinks, " Blink rate is normal. Eyes are doing great!"
