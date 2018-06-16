import io
import time
import picamera
from google.cloud import vision

IMG_PATH = 'image.jpg'


def take_photo(img_path):
    with picamera.PiCamera() as cam:
        cam.resolution = (640, 480)
        cam.capture(img_path)


def detect_faces(img):
    """Detects faces in an image."""

    client = vision.ImageAnnotatorClient()

    with io.open(img, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    for face in faces:
        joy_deg = face.joy_likelihood
        surprise_deg = face.surprise_likelihood
        is_happy = any([joy_deg >= 3, surprise_deg >= 5])
        print('joy: {}\n'
              'surprise: {}\n'
              'Smiled?: {}'.format(likelihood_name[joy_deg], likelihood_name[surprise_deg], is_happy))


if __name__ == '__main__':
    time.sleep(0.5)
    take_photo(IMG_PATH)
    detect_faces(IMG_PATH)
