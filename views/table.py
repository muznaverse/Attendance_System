import streamlit as st
import cv2
import pandas as pd
from datetime import datetime
import os
import pickle

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {}
try:
    with open("labels.pkl", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}
except FileNotFoundError:
    print("Error: labels.pkl not found!")

attendance_file = "attendance.csv"

if not os.path.exists(attendance_file):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_csv(attendance_file, index=False)


def capture_and_mark_attendance():
    cap = cv2.VideoCapture(0)  #
    ret, frame = cap.read()  
    cap.release()  

    if not ret:
        st.error("Failed to capture image from webcam")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        id_, conf = recognizer.predict(roi_gray)

        if conf >= 45 and conf <= 85:
            name = labels.get(id_, "Unknown")

            # Log attendance
            current_time = datetime.now()
            date_str = current_time.strftime("%Y-%m-%d")
            time_str = current_time.strftime("%H:%M:%S")

            # Update attendance table
            df = pd.read_csv(attendance_file)
            new_row = {"Name": name, "Date": date_str, "Time": time_str}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(attendance_file, index=False)

            # Display the name on the frame
            cv2.putText(frame, f"Name: {name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    st.image(frame_rgb, channels="RGB", use_container_width=True)

# Streamlit UI
st.title("Real-Time Face Recognition Attendance System")

# Show video and handle attendance logging
if st.button("Capture Face and Mark Attendance"):
    capture_and_mark_attendance()

# Display the attendance table
if st.button("View Attendance"):
    df = pd.read_csv(attendance_file)
    st.write(df)
