'''

    Driver for autonomous vehicle image assistance.

'''

from lib.object_detection import ObjectDetector
from sys import argv
from os import listdir
from os.path import exists, isfile, isdir
from PIL import Image
import json

'''

    RUN TIME ARGUMENTS:
        - 1: Input type
            - 1: Single image (JPG/PNG)
            - 2: Directory of images (JPG/PNG)
            - 3: Video (mp4)
            - 4. Training
        - 2: Path to directory or file

    ex. single image, directory, video
        - python run.py 1 path/to/image.jpg
        - python run.py 2 path/to/images
        - python run.py 3 path/to/video.mp4
        - python run.py 4

'''

INPUT_TYPES = 4

IMAGE_TYPES = ('.jpg', '.png', '.jpeg')
VIDEO_TYPES = ('.mp4')

TRAIN_OBSTACLES = True
TRAIN_LANES = False
TRAIN_SIGNS = False

TEST_OBSTACLES = True
TEST_LANES = False
TEST_SIGNS = False

TRAINING_SIZE = 5

object_detector = ObjectDetector(training_size=TRAINING_SIZE)

def main():

    global object_detector
    
    # parse arguments
    assert int(argv[1])
    assert int(argv[1]) >= 1 and int(argv[1]) <= INPUT_TYPES
    input_type = int(argv[1])
    path = ''

    # validate input data
    if input_type == 1 or input_type == 3:
        path = argv[2]
        assert isfile(path)
        assert len(argv) == 3
        assert exists(path)
        if (input_type == 1):
            assert path.lower().endswith(IMAGE_TYPES)
        else:
            assert path.lower().endswith(VIDEO_TYPES)
    elif input_type == 2:
        assert isdir(path)
        # directory is not empty
        assert len(listdir(path)) != 0
        # all files are images
        for file_name in listdir(path):
            assert file_name.lower().endswith(IMAGE_TYPES)
    elif input_type == 4:
        assert exists('data/train')
        assert len(listdir('data/train')) != 0
        assert exists('data/labels')
        assert len(listdir('data/labels')) != 0
    else:
        raise InvalidInput
    
    # perform action
    if input_type == 1:

        # SINGLE IMAGE

        object_detector.predict(path)

        # open image and convert to grayscale

        
        '''
        rgb_image = Image.open(path)
        grayscale_image = ImageOps.grayscale(rgb_image)
        grayscale_image.show()

        # test image on obstacle detecting network
        result = rgb_image
        if TEST_OBSTACLES:
            result = object_detector.test(original=rgb_image, grayscale=grayscale_image)

        # save image
        index = len(listdir('output'))
        path = f'output/{index}'
        mkdir(path)
        result.save(f'{path}/result.jpg')
        '''

    elif input_type == 4:

        # TRAINING

        # load labels
        label_path = 'data/labels/bdd100k_labels_images_train.json'
        labels = load_labels(label_path)
    
        # load images from labels
        images = load_training_images(labels)

        if TRAIN_OBSTACLES:
            object_detector.load_training_data(images=images, labels=labels)
            object_detector.train()

def load_labels(path):

    ''' Load labels from file '''

    labels = None
    with open(path) as file:
        labels = json.load(file)
    return labels

def load_training_images(labels):

    ''' Create dictionary mapping file names to images '''

    images = {}
    for index, label in enumerate(labels): 
        file_name = label['name']
        path = f'data/train/{file_name}'
        if exists(path):
            image = Image.open(path)
            images[path] = image
        else:
            print(f'Cant find: {path}')
        if index >= TRAINING_SIZE-1:
            break
    return images

if __name__ == '__main__':
    main()

class InvalidInput(Exception):
    def __init__(self):
        self.message = "ERROR: Invalid input"
        super(message=self.message)