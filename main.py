import cv2
import numpy as np
import os
import glob
import face_recognition

class faceRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        print("We detected {} dataset images..".format(len(images_path)))

        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
            name = "Face Not Found"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names

video = cv2.VideoCapture(0)

faceRec = faceRecognition()
faceRec.load_encoding_images("images/")

while True:
    ret, frame = video.read()

    face_locations, face_names = faceRec.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        
        cv2.putText(frame,name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (204, 153, 255), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (204, 153, 255), 4)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()