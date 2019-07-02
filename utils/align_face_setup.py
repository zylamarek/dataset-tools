import dlib
import os
import urllib.request
import bz2

FACE_PREDICTOR_FILE = 'shape_predictor_68_face_landmarks.dat'
FACE_PREDICTOR_URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'

predictor_path = os.path.join(os.path.dirname(__file__), FACE_PREDICTOR_FILE)


def predictor_setup():
    get_predictor()

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)

    return detector, predictor


def get_predictor():
    if os.path.isfile(predictor_path):
        return

    print('Downloading %s...' % FACE_PREDICTOR_URL)
    bz2_path, _ = urllib.request.urlretrieve(FACE_PREDICTOR_URL)

    print('Extracting %s...' % FACE_PREDICTOR_FILE)
    with bz2.open(bz2_path, 'rb') as bz2_file:
        with open(predictor_path, 'wb') as f:
            f.write(bz2_file.read())
