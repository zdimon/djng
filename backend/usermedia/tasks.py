from celery.decorators import task
import cv2
from backend.settings import DOMAIN, BASE_DIR
from django.core.files import File


@task
def take_pic_from_video(media):
    from .models import UserMedia
    cam = cv2.VideoCapture(media.video.path)
    ret,frame = cam.read()
    path = '%s/tmp/%s.jpg' % (BASE_DIR,media.id)
    print ('Creating...' + path)  
    cv2.imwrite(path, frame)
    try:
        with open(path, 'rb') as image:
            media.image.save('%s.jpg'% media.id, File(image), save=True)
            media.save()
    except Exception as ex:
        print(ex)
