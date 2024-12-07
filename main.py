import cv2
import numpy as np
import pickle
import pandas as pd
from datetime import datetime
import os
import time

# Load Haarcascade Classifier
face_cascade = cv2.CascadeClassifier("Data/haarcascade_frontalface_default.xml")

# Load the trained recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")  # Ensure this file is available

# Load labels from pickle file
labels = {}
try:
    with open("labels.pkl", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}
except FileNotFoundError:
    print("Error: labels.pkl not found!")

# Initialize the attendance file (either CSV or Excel)
attendance_file = "attendance.csv"

# Check if the file exists, if not create a new one
if not os.path.exists(attendance_file):
    # Create a new CSV file with columns for Name, Date, and Time
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_csv(attendance_file, index=False)
    print(f"Created new attendance file: {attendance_file}")

# Start video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam not accessible!")
    exit()

# HashMap for storing today's attendance (in-memory)
attendance_hashmap = {}
# Store the last time a person's attendance was marked
last_attendance_time = {}

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        print(f"Face detected at: x={x}, y={y}, w={w}, h={h}")
        roi_gray = gray[y:y+h, x:x+w]  # Region of interest (grayscale)

        # Recognize the face
        id_, conf = recognizer.predict(roi_gray)
        print(f"Prediction: ID={id_}, Confidence={conf}")

        # Adjust confidence threshold based on testing
        if conf >= 45 and conf <= 85:
            person_name = labels.get(id_, "Unknown")
            print(f"Recognized: {person_name}")

            # Draw rectangle around the face and display name
            color = (255, 0, 0)  # BGR (Blue rectangle)
            stroke = 3  # Rectangle border thickness
            end_cord_x, end_cord_y = x + w, y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            cv2.putText(frame, person_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('a'): 
                current_time = datetime.now()
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%H:%M:%S")

                
                current_time_in_seconds = time.time()

              
                if person_name not in attendance_hashmap or attendance_hashmap[person_name][0] != date_str:
                  
                    if person_name not in last_attendance_time or (current_time_in_seconds - last_attendance_time[person_name] >= 30):
                       
                        attendance_hashmap[person_name] = (date_str, time_str)

                        # Save to CSV file
                        df = pd.read_csv(attendance_file)
                        new_row = {"Name": person_name, "Date": date_str, "Time": time_str}
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                        df.to_csv(attendance_file, index=False)
                        print(f"Attendance recorded for {person_name} at {time_str}")

                        # Store the last attendance time for the person
                        last_attendance_time[person_name] = current_time_in_seconds

                        # Display "Attendance Marked!" and turn the screen green
                        cv2.putText(frame, "Attendance Marked!", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        # Create green background
                        green_screen = np.full_like(frame, (0, 255, 0), dtype=np.uint8)
                        # Show the green screen for 1 second
                        cv2.imshow('Face Recognition', green_screen)
                        cv2.waitKey(1000)  # Wait for 1 second
                        cv2.imshow('Face Recognition', frame)  # Show the original frame again

                    else:
                        # Calculate remaining time
                        remaining_time = 30 - (current_time_in_seconds - last_attendance_time[person_name])
                        remaining_time = int(remaining_time)

                        # Display countdown timer
                        cv2.putText(frame, f"Wait: {remaining_time}s", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                else:
                    # If attendance is already marked, just show "Attendance already marked"
                    cv2.putText(frame, "Attendance already marked", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Press 'q' to quit
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()
