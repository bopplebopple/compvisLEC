import cv2
from face_recognition.api import face_locations
from simple_facerec import SimpleFacerec

cap = cv2.VideoCapture(0)

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")



while True:
    ret, frame = cap.read()

    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        
        cv2.putText(frame,name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (204, 153, 255), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (204, 153, 255), 4)

    cv2.imshow("Frame", frame)

#Use 'esc' to close window
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()