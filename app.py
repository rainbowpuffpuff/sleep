import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils import extract_exif_datetime, classify_image  # Fixed: use absolute import
from datetime import datetime

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
BEDTIME_HOUR = 22  # 10 PM

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_points(photo_time):
    # More points for earlier sleep, max 100 for 8pm, min 0 for after 2am
    if not photo_time:
        return 0
    hour = photo_time.hour + photo_time.minute / 60
    if hour < 20:
        hour = 20  # Clamp earliest
    if hour > 26:
        hour = 26  # Clamp latest (2am)
    points = int((26 - hour) / 6 * 100)  # 8pm=100, 2am=0
    return max(0, min(100, points))

def longevity_fact(hours_slept):
    # Simple fun fact: every hour of sleep above 6h adds X days to life expectancy
    if hours_slept >= 8:
        return "Optimal sleep! You could add years to your life."
    elif hours_slept >= 7:
        return "Pretty good! Consistent 7h+ sleep is linked to longevity."
    elif hours_slept >= 6:
        return "Try for 7-8h for best health and longevity."
    else:
        return "Less than 6h sleep is linked to higher health risks."

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result = None
    label = None
    score = None
    photo_time = None
    points = 0
    bar_width = 0
    fact = None
    sleep_time_str = None
    custom_message = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Extract EXIF datetime
            photo_time = extract_exif_datetime(filepath)
            # Classify image
            label, score = classify_image(filepath)
            print(f"Detected: {label} (confidence: {score:.2f})")
            # Dashboard logic
            if not photo_time and (label == 'bed' or label == 'couch'):
                custom_message = "\U0001F6CF\uFE0F I see you have a bed, but I can't tell when you went to sleep! \U0001F575\uFE0F\U0001F50D"
            elif not photo_time:
                custom_message = "\U0001F575\uFE0F\U0001F50D I can't really know when you went to sleep. Try another photo!"
            elif label != 'bed' and label != 'couch':
                custom_message = "\U0001F914 Hmm... are you sure that's a bed or couch?"
            elif photo_time.hour < BEDTIME_HOUR:
                custom_message = "\U0001F31F Sleep champion! You went to bed early!"
                print("i love you albina")  # Secret message in console
            else:
                custom_message = f"Photo taken at {photo_time.strftime('%H:%M')}, try to sleep earlier!"
            # Points and bar
            points = calculate_points(photo_time)
            bar_width = points
            # Sleep time string
            if photo_time:
                sleep_time_str = photo_time.strftime('%H:%M')
                # Assume wake up at 6:30am
                hours_slept = 6.5 + (24 - photo_time.hour - photo_time.minute/60) if photo_time.hour > 12 else 6.5 + (22 - photo_time.hour - photo_time.minute/60)
                fact = longevity_fact(hours_slept)
            return render_template('dashboard.html', result=custom_message, label=label, score=score, photo_time=photo_time, points=points, bar_width=bar_width, fact=fact, sleep_time_str=sleep_time_str)
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
