from google.cloud import vision
from PIL import Image, ImageDraw
import cv2

client = vision.ImageAnnotatorClient()
# Names of likelihood from google.cloud.vision.enums
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

class Facedetection(object):

    def __init__(self, max_results=4, ifprint=False):
        self.client = vision.ImageAnnotatorClient()
        self.likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
        self.max_results = max_results
        self.ifprint = ifprint
        self.faces = None

    def detect_face(content):
        """Uses the Vision API to detect faces in the given file.

        Args:
            face_file: A file-like object containing an image with faces.

        Returns:
            An array of Face objects with information about the picture.
        """
        # client = vision.ImageAnnotatorClient()

        # content = face_file.read()
        # print content
        image = vision.types.Image(content=content)
        # print type(image)
        response = self.client.face_detection(image=image)
        self.faces = response.face_annotations


        if self.ifprint:
            print('Faces:')

            for face in self.faces:
                print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
                print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
                print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

                vertices = (['({},{})'.format(vertex.x, vertex.y)
                            for vertex in face.bounding_poly.vertices])

                print('face bounds: {}'.format(','.join(vertices)))
        

        # return client.face_detection(image=image).face_annotations
        return self.faces

    def highlight_faces(image, faces):
        """Draws a polygon around the faces, then saves to output_filename.

        Args:
          image: a file containing the image with the faces.
          faces: a list of faces found in the file. This should be in the format
              returned by the Vision API.
          output_filename: the name of the image file to be created, where the
              faces have polygons drawn around them.
        """
        if self.faces == None:
            self.faces = faces
            
        # im = Image.open(image)
        draw = ImageDraw.Draw(image)

        for face in self.faces:
            box = [(vertex.x, vertex.y)
                   for vertex in face.bounding_poly.vertices]
            draw.line(box + [box[0]], width=5, fill='#00ff00')

        # im.save(output_filename)
        return image


def detect_face(content, max_results=4, ifprint=False):
    """Uses the Vision API to detect faces in the given file.
     Args:
        face_file: A file-like object containing an image with faces.

     Returns:
        An array of Face objects with information about the picture.
    """
    # client = vision.ImageAnnotatorClient()

    # content = face_file.read()
    # print content
    image = vision.types.Image(content=content)
    # print type(image)
    response = client.face_detection(image=image)
    faces = response.face_annotations


    if ifprint:
        print('Faces:')
        for face in faces:
            print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
            print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
            print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
            # print('smile: {}'.format(likelihood_name[face.surprise_likelihood]))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                            for vertex in face.bounding_poly.vertices])

            print('face bounds: {}'.format(','.join(vertices)))
        

    # return client.face_detection(image=image).face_annotations
    return faces

def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
        image: a file containing the image with the faces.
        faces: a list of faces found in the file. This should be in the format
              returned by the Vision API.
        output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    im.save(output_filename)

def main(input_filename, output_filename, max_results):
    image = cv2.imread(input_filename)
    img_bytes = cv2.imencode('.jpg', image)[1].tostring()
    # print img_bytes
    faces = detect_face(img_bytes, max_results)
    print('Found {} face{}'.format(
        len(faces), '' if len(faces) == 1 else 's'))
    
    #with open(input_filename, 'rb') as image:
    #    faces = detect_face(image, max_results)
    #    print('Found {} face{}'.format(
    #        len(faces), '' if len(faces) == 1 else 's'))

    #   print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
    #    image.seek(0)
    #    highlight_faces(image, faces, output_filename)

if __name__ == "__main__":
    main("human.jpg", "test.jpg", 1)
