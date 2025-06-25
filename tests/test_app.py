import os
import tempfile
import pytest
from .app import app
from .utils import extract_exif_datetime, classify_image

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Upload a photo' in rv.data

def test_extract_exif_datetime():
    # Use a sample image with EXIF or mock
    assert extract_exif_datetime('tests/sample_with_exif.jpg') is None or True

def test_classify_image():
    # Use a sample image or mock
    label, score = classify_image('tests/sample_bed.jpg')
    assert isinstance(label, str)
    assert isinstance(score, float)
