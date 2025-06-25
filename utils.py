from PIL import Image
from PIL.ExifTags import TAGS
from transformers import pipeline
from datetime import datetime

# Load classifier once
classifier = pipeline('image-classification', model='google/vit-base-patch16-224')

def extract_exif_datetime(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            return None
        date_fields = ['DateTimeOriginal', 'DateTimeDigitized', 'DateTime']
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag in date_fields:
                try:
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                except Exception:
                    continue
    except Exception:
        return None
    return None

def classify_image(image_path):
    results = classifier(image_path)
    # Find first label that is 'bed' or 'couch', else return top label
    for r in results:
        label = r['label'].lower()
        if 'bed' in label:
            return 'bed', r['score']
        if 'couch' in label or 'sofa' in label:
            return 'couch', r['score']
    return results[0]['label'].lower(), results[0]['score']
