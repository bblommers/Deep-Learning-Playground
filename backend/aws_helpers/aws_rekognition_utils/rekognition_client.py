import os
import boto3
from botocore.exceptions import ClientError
from PIL import Image, ImageDraw
import io

class RekognitionImage():
    def __init__ (self, image, image_name, rekognition_client):
        self.image = image
        self.image_name = image_name
        self.rekognition_client = rekognition_client

    @classmethod
    def from_file(cls, file_name, rekognition_client):
        image = {'Bytes': open(file_name, 'rb').read()}
        return cls(image, file_name, rekognition_client)

    def detect_labels(self, max_labels):
        try:
            response = self.rekognition_client.detect_labels(
                Image=self.image, MaxLabels=max_labels)
        except ClientError:
            print("AWS client error")
        else:
            return response['Labels']

def show_bounding_boxes(image_bytes, box_sets, colors):
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)
    for boxes, color in zip(box_sets, colors):
        for box in boxes:
            left = image.width * box['Left']
            top = image.height * box['Top']
            right = (image.width * box['Width']) + left
            bottom = (image.height * box['Height']) + top
            draw.rectangle([left, top, right, bottom], outline=color, width=3)
    image.show()
    im_b64 = base64.b64encode(image_bytes)
    return im_b64

def detect_labels_from_file(file_name):
    rekognition_client = boto3.client('rekognition')
    image = RekognitionImage.from_file(file_name, rekognition_client)
    labels = image.detect_labels(100)
    names = []
    box_sets = []
    for label in labels:
        print("Label" + label.get('Name'))
        if(label.get('Instances')):
            names.append(label.get('Name'))
            box_sets.append([inst['BoundingBox'] for inst in label.get('Instances')])
    colors = ['aqua', 'red', 'white', 'blue', 'yellow', 'green']
    im_b64 = show_bounding_boxes(image.image['Bytes'], box_sets, colors[:len(names)])
    return im_b64



def demo():
    file_name = "C:/Users/austi/Downloads/download.jpg"
    detect_labels_from_file(file_name)


def rekognition_img_drive(IMAGE_UPLOAD_FOLDER):
    for x in os.listdir(IMAGE_UPLOAD_FOLDER):
        print("hello")
        if x != ".gitkeep":
            img_file = os.path.join(
                os.path.abspath(IMAGE_UPLOAD_FOLDER), x)
            break
    im_b64 = detect_labels_from_file(img_file)
    return {"image_data" : im_b64 }

