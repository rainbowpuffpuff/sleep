# Sleep Early Web App

A minimal Flask web app for uploading an image, extracting EXIF metadata, and classifying if the image contains a bed or couch using HuggingFace transformers. No user accounts or history. Includes basic tests for upload, metadata extraction, and classification logic.

## Features
- Upload an image via web form
- Extract EXIF metadata (timestamp)
- Classify image for bed/couch using HuggingFace transformers
- Award points if criteria met
- No login or persistent storage

## Setup
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   flask run
   ```
4. Run tests:
   ```bash
   pytest
   ```

## Project Structure
- `app.py` - Main Flask app
- `utils.py` - Helper functions for metadata and classification
- `templates/` - HTML templates
- `tests/` - Test cases

---
