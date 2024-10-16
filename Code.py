import cv2
import pygame
import tkinter as tk
from tkinter import filedialog
import threading
import time

# Initialize pygame and load sound
pygame.init()
sound = pygame.mixer.Sound('alarm_alert.mp3')

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize Tkinter
root = tk.Tk()
root.title("Crowd Monitoring")

# Initialize variables for face count and alarm state
face_count = 0
alarm_active = False
cap = None  # Video capture object

def run_video_capture(source):
    global cap, face_count, alarm_active
    if cap is not None:
        cap.release()  # Release previous capture if it exists
    cap = cv2.VideoCapture(source)
    width = 6400
    height = 4800
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    start_time = time.time()  # Record the start time
    duration = 15  # Set duration for automatic stop (e.g., 15 seconds)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        face_count = len(faces)
        cv2.putText(frame, f'Count: {face_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Play sound if count exceeds threshold (e.g., 3)
        if face_count >3 :
            if not alarm_active:
                sound.play(-1)  # Loop the sound
                alarm_active = True
        else:
            if alarm_active:
                sound.stop()
                alarm_active = False

        cv2.imshow('Crowd Monitoring', frame)

        # Check for automatic stop
        if time.time() - start_time > duration:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_video_capture_thread(source):
    thread = threading.Thread(target=run_video_capture, args=(source,))
    thread.start()

def start_webcam():
    start_video_capture_thread(0)

def start_video_file():
    video_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv;*.flv")]
    )
    if video_path:  # Ensure a file was selected
        start_video_capture_thread(video_path)


 # Create a frame to hold the buttons and center them
button_frame = tk.Frame(root)
button_frame.pack(pady=50)  # Add vertical padding to center the buttons in the window

# Create buttons for selecting input source
webcam_button = tk.Button(button_frame, text="Start Webcam", command=start_webcam,
                          bg="#4CAF50", fg="white", font=("Helvetica", 16),
                          width=15, height=2)
webcam_button.pack(padx=20, pady=10)  # Add padding for spacing between buttons

video_button = tk.Button(button_frame, text="Select Video File", command=start_video_file,
                         bg="#2196F3", fg="white", font=("Helvetica", 16),
                         width=15, height=2)
video_button.pack(padx=20, pady=10)  # Same padding to ensure consistent spacing

# Start the Tkinter main loop
root.mainloop()