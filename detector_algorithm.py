
import time
import cv2 as cv
import mediapipe as mp
import numpy as np
import serial

mp_face_detection = mp.solutions.face_detection
arduino = serial.Serial(port='COM4', baudrate=460800, timeout=0.1)
cap = cv.VideoCapture(0)
counterSend = 0
counter2 = 0
send = False

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detector:
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        results = face_detector.process(rgb_frame)
        frame_height, frame_width, _ = frame.shape
        
        
        if results.detections:
            # Prendi solo il primo volto rilevato
            face = results.detections[0]
            

            face_react = np.multiply(
                [
                    face.location_data.relative_bounding_box.xmin,
                    face.location_data.relative_bounding_box.ymin,
                    face.location_data.relative_bounding_box.width,
                    face.location_data.relative_bounding_box.height,
                ],
                [frame_width, frame_height, frame_width, frame_height]).astype(int)

            cv.rectangle(frame, face_react, color=(255, 255, 255), thickness=2)
            key_points = np.array([(p.x, p.y) for p in face.location_data.relative_keypoints])
            key_points_coords = np.multiply(key_points, [frame_width, frame_height]).astype(int)
            for p in key_points_coords:
                cv.circle(frame, p, 4, (255, 255, 255), 2)
                cv.circle(frame, p, 2, (0, 0, 0), -1)
            posy = round(face.location_data.relative_bounding_box.ymin*100+(face.location_data.relative_bounding_box.height*100)/2)
            posx = round(face.location_data.relative_bounding_box.xmin*100+(face.location_data.relative_bounding_box.width*100)/2)
            
            if posx<0:
                posx*=-1
            if posy<0:
                posy*=-1
            pos = str(posx)+","+str(posy)+"\n"

            if counterSend % 2 == 0:
                send = True
            
            
            if send:
                arduino.write(bytes(pos, 'utf-8'))
                send = False
                print(posx)
                print(posy)
                print("------")
                
                
            
            counterSend += 1
        else:
            if counter2 % 2==0:
                arduino.write(bytes("-1,-1\n", 'utf-8'))
            counter2+=1
        
        cv.imshow("frame", frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
