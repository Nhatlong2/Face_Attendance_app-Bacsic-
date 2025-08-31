import cv2
import numpy as np
from models.detector import FaceDetector
from models.recognizer import FaceRecognizer
from services.db_service import DatabaseService

def test_detector_on_blank_image():
    detector = FaceDetector()
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    faces = detector.detect_faces(img)
    assert faces == () or faces == []  # không phát hiện gì trên ảnh trắng

def test_recognizer_empty_db():
    db = DatabaseService()
    rec = FaceRecognizer(db)
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    results = rec.recognize(img, [])
    assert results == []
    db.close()
