import face_recognition
import cv2

class Utils:
    @staticmethod
    def process_frame(frame, assistant):
        frame_rgb = frame

        known_face_encodings = assistant.known_face_encodings
        known_face_names = assistant.known_face_names

        face_locations = face_recognition.face_locations(frame_rgb)
        face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = 'Unknown'
                assistant.visible_known_face_names.append(name)
                if True in matches:
                    index = matches.index(True)
                    name = known_face_names[index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        return frame
    @staticmethod
    def video_capture_loop(face_recognizer, frame_queue):
        video_capture = cv2.VideoCapture(0)
        frame_count = 0
        frame_modulus = 5  # Change this to 3 if you want to add every 3rd frame

        while True:
            ret, frame = video_capture.read()
            frame_count += 1
            if not ret:
                break

            if frame_count % frame_modulus == 0:
                frame_queue.put(frame)

        video_capture.release()

    @staticmethod
    def face_recognition_loop(assistant, frame_queue, result_queue):
        while True:
            frame = frame_queue.get()
            if frame is None:
                break

            # Process the frame using the face_recognizer object
            Utils.process_frame(frame, assistant)

            result_queue.put(frame)
