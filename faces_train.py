import cv2
import os
from PIL import Image
import numpy as np
import pickle

# Load Haarcascade
face_cascade = cv2.CascadeClassifier("Data/haarcascade_frontalface_default.xml")

# Walking through directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "Images") 

# Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Label management
current_id = 0
label_ids = {}
y_labels = []
x_train = []

# Resize and augment function
def resize_and_augment_image(image):
    # Resize to a fixed size (e.g., 300x300)
    size = (300, 300)
    image = image.resize(size)
    
    # Convert to numpy array
    image_array = np.array(image, "uint8")
    
    # Augment the image with horizontal flip
    flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    flipped_image_array = np.array(flipped_image, "uint8")
    
    # Augment the image with slight rotation (15 degrees)
    rotated_image = image.rotate(15)
    rotated_image_array = np.array(rotated_image, "uint8")
    
    return image_array, flipped_image_array, rotated_image_array

# Iterate through images
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()

            # Add label to label_ids
            if label not in label_ids:
                label_ids[label] = current_id
                current_id += 1
            
            id_ = label_ids[label]

            # Convert image to grayscale and resize
            pil_image = Image.open(path).convert("L")  # Convert to grayscale

            # Resize and augment the image
            image_array, flipped_image_array, rotated_image_array = resize_and_augment_image(pil_image)

            # Detect faces in the original image
            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.3, minNeighbors=7)
            for (x, y, w, h) in faces:
                roi = image_array[y:y+h, x:x+w]  # Region of Interest (face)
                x_train.append(roi)
                y_labels.append(id_)

            # Detect faces in the flipped image
            faces = face_cascade.detectMultiScale(flipped_image_array, scaleFactor=1.3, minNeighbors=7)
            for (x, y, w, h) in faces:
                roi = flipped_image_array[y:y+h, x:x+w]  # Region of Interest (face)
                x_train.append(roi)
                y_labels.append(id_)

            # Detect faces in the rotated image
            faces = face_cascade.detectMultiScale(rotated_image_array, scaleFactor=1.3, minNeighbors=7)
            for (x, y, w, h) in faces:
                roi = rotated_image_array[y:y+h, x:x+w]  # Region of Interest (face)
                x_train.append(roi)
                y_labels.append(id_)

# Save label IDs to a pickle file
with open("labels.pkl", "wb") as f:
    pickle.dump(label_ids, f)

# Train the recognizer
recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainer.yml")

print("Training completed")
