import cv2
import face_recognition
from services.db_service import DatabaseService
import numpy as np
from services.user_service import UserService

class FaceRecognizer:
    def __init__(self, db: DatabaseService, tolerance=0.45):
        self.db = db
        self.tolerance = tolerance
        self.load_known_encodings()

    def load_known_encodings(self):
        rows = self.db.fetchall("SELECT user_id, embedding FROM Faces")
        self.known_ids = [row[0] for row in rows]
        self.known_encodings = [np.frombuffer(row[1], dtype=np.float64) for row in rows]

    def recognize(self, frame, haar_boxes):
        # convert (x,y,w,h) -> (top,right,bottom,left), clamp vào ảnh
        h_img, w_img = frame.shape[:2]
        fr_boxes = [
            (max(0, int(y)), min(w_img, int(x + w)), min(h_img, int(y + h)), max(0, int(x)))
            for (x, y, w, h) in haar_boxes
        ]

        if not fr_boxes:
            return []

        rgb = frame[:, :, ::-1].astype("uint8")
        encodings = face_recognition.face_encodings(rgb, known_face_locations=fr_boxes)

        results = []
        users = UserService(self.db)

        for encoding in encodings:
            name = "Unknown"
            user_id = None

            if self.known_encodings:  # nếu có dữ liệu trong DB
                distances = face_recognition.face_distance(self.known_encodings, encoding)
                best_match_idx = np.argmin(distances)
                best_distance = distances[best_match_idx]

                # chỉ nhận diện nếu khoảng cách < tolerance
                if best_distance <= self.tolerance:
                    user_id = self.known_ids[best_match_idx]
                    name = users.get_user_name_by_id(user_id) or f"User {user_id}"

            results.append((user_id, name))

        return results


def main():
    from services.db_service import DatabaseService
    from models.detector import FaceDetector

    db = DatabaseService()
    recognizer = FaceRecognizer(db)
    detector = FaceDetector()

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        faces = detector.detect_faces(frame)
        results = recognizer.recognize(frame, faces)
        for (x, y, w, h), (uid, name) in zip(faces, results):
            label = name
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        cv2.imshow("Recognizer", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    db.close()

if __name__ == "__main__":
    main()
