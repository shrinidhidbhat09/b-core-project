import cv2
import os

def record_video(filename='uploads/output.mp4', duration=10):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    frame_count = 0
    while cap.isOpened() and frame_count < duration * 20:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        frame_count += 1
        cv2.imshow('Recording...', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Delete the video after recording ends
    if os.path.exists(filename):
        os.remove(filename)
        print(f"{filename} deleted successfully.")
    else:
        print(f"{filename} not found!")

if __name__ == "__main__":
    record_video()
