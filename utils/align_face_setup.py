import dlib
import os

FACE_PREDICTOR_FILE = 'shape_predictor_68_face_landmarks.dat'


def predictor_setup():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(os.path.join(os.path.dirname(__file__), FACE_PREDICTOR_FILE))

    return detector, predictor
