from base64 import b64decode
from io import BytesIO
import cv2
from PIL import Image
import pickle
import numpy
import face_recognition
import binascii


def bytestring_to_cv(buf):
    #buf = bytes(buf, 'ascii')
    #buf = buf.replace(b'data:image/jpeg;base64', b'')
    #print('buf:')
    #print(buf.decode('unicode'))
    #print('')
    image = BytesIO(buf)
    image.seek(0)
    #print("bytesIO:")
    #print(image.read())
    #print('')
    image.seek(0)
    pil_image = Image.open(image)
    opencvImage = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
    return opencvImage

def embedFaces(image_dict_list):
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    #imagePaths = list(paths.list_images(args["dataset"]))

    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []

    # loop over the image paths
    for i in range(len(image_dict_list)):
        # extract the person name from the image path
        print("[INFO] processing image {}".format(i + 1), len(image_dict_list))
        #name = imagePath.split(os.path.sep)[-2]

        name = image_dict_list[i].get('name')
        buf = image_dict_list[i].get('image_bytes')

        image = bytestring_to_cv(buf)

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        #image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model="cnn")

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)
	
    print("[INFO] serializing encodings...")
    data = {
        "status": 200,
        "message": "Success",
        "encodings": str(pickle.dumps(knownEncodings)), 
        "names": str(pickle.dumps(knownNames))
    }
    return data
