import cv2
import serial
import time

# Initialize the serial connection to Arduino
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

# Load the face classifier
face_classifier = cv2.CascadeClassifier('/home/halldor/opencv/haarcascade_frontalface_default.xml')

# Initialize video capture
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set height

first_face_detected = None

def is_same_face(face1, face2):
   
    threshold = 50  
    center1 = (face1[0] + face1[2] // 2, face1[1] + face1[3] // 2)
    center2 = (face2[0] + face2[2] // 2, face2[1] + face2[3] // 2)
    return abs(center1[0] - center2[0]) < threshold and abs(center1[1] - center2[1]) < threshold

def detect_distance_and_direction(vid, frame_center, gray_image):
    global first_face_detected
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    
    if len(faces) > 0:
        if first_face_detected is not None:
            for (x, y, w, h) in faces:
                if is_same_face(first_face_detected, (x, y, w, h)):
                    return calculate_face_data(vid, x, y, w, h, frame_center)

        x, y, w, h = faces[0]
        first_face_detected = (x, y, w, h)
        return calculate_face_data(vid, x, y, w, h, frame_center)
    else:
        first_face_detected = None
        return False, None, None

def calculate_face_data(vid, x, y, w, h, frame_center):
    cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 255), 2)
    face_center_x = x + w // 2
    face_center_y = y + h // 2
    distance_x = face_center_x - frame_center[0]
    distance_y = frame_center[1] - face_center_y
    return True, distance_x, distance_y

while True:
    result, video_frame = video_capture.read()
    if not result:
        break

    frame_center = (video_frame.shape[1] // 2, video_frame.shape[0] // 2)
    gray_image = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
    face_detected, distance_x, distance_y = detect_distance_and_direction(video_frame, frame_center, gray_image)

    cv2.imshow("My Face Detection Project", video_frame)

    if face_detected:
        
        arduino.write(f'X{distance_x},Y{distance_y}\n'.encode())
        print(f'X{distance_x}, Y{distance_y}')

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
arduino.close()