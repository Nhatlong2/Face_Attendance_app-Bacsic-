import cv2

class FaceDetector:
    def __init__(self, cascade_path=None):
        self.cascade = cv2.CascadeClassifier(
            cascade_path or cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect_faces(self, frame, scale_factor=1.1, min_neighbors=5, min_size=(30,30)):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_size
        )
        return faces  # list of (x, y, w, h)

def main():
    detector = FaceDetector()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không mở được camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        faces = detector.detect_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Face Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
