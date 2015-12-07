from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

def resize_image(image, full_size, thumb_size, filename, region=None):

	image = Image.open(BytesIO(image.read()))

	if region:
		cropped = image.crop(region)
	else:
		cropped = image

	PIL_TYPE = 'jpeg'
	CONTENT = 'image/jpeg'

	image_storage = BytesIO()
	cropped = cropped.resize(full_size)
	cropped.save(image_storage, PIL_TYPE, quality=100)
	image_storage.seek(0)

	thumb_storage = BytesIO()
	cropped.thumbnail(thumb_size, Image.ANTIALIAS)
	cropped.save(thumb_storage, PIL_TYPE, quality=100)
	thumb_storage.seek(0)

	image_file = SimpleUploadedFile(filename, image_storage.read(), content_type=CONTENT)
	thumb_file = SimpleUploadedFile(filename, thumb_storage.read(), content_type=CONTENT)

	return image_file, thumb_file
