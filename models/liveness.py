import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance as dist

class LivenessDetector:
    def __init__(self, shape_predictor_path, ear_threshold=0.25, consec_frames=2):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_predictor_path)
        self.ear_threshold = ear_threshold
        self.consec_frames = consec_frames
        self.frame_counter = 0

    @staticmethod
    def eye_aspect_ratio(eye):
        # Tính EAR theo công thức
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        return (A + B) / (2.0 * C)

    def is_blinking(self, gray):
        rects = self.detector(gray, 0)
        for rect in rects:
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            left = shape[42:48]
            right = shape[36:42]
            left_ear = self.eye_aspect_ratio(left)
            right_ear = self.eye_aspect_ratio(right)
            ear = (left_ear + right_ear) / 2.0
            if ear < self.ear_threshold:
                self.frame_counter += 1
                if self.frame_counter >= self.consec_frames:
                    self.frame_counter = 0
                    return True
            else:
                self.frame_counter = 0
        return False

def main():
    detector = LivenessDetector("shape_predictor_68_face_landmarks.dat")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không mở được camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if detector.is_blinking(gray):
            cv2.putText(frame, "Live (blink detected)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Not Live", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow("Liveness Checker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
