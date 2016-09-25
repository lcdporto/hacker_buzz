import settings

from exceptions import MissingFile

def save_image(request):
    """
    Save image to filesystem
    """
    upload = request.files.get('image')
    if upload is None:
        raise MissingFile
    upload.save(settings.UPLOADS, True)
    return upload
