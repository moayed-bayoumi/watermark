import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        watermark_file = request.files['watermark']
        if watermark_file and allowed_file(watermark_file.filename):
            watermark_filename = secure_filename(watermark_file.filename)
            watermark_file.save(os.path.join(app.config['UPLOAD_FOLDER'], watermark_filename))

        files = request.files.getlist('files')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('preview'))

    return render_template('index.html')

@app.route('/preview')
def preview():
    watermark_filename = request.args.get('watermark')
    if not watermark_filename:
        return redirect(url_for('index'))

    images = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            watermark = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], watermark_filename)).convert('RGBA')
            width, height = image.size
            watermark_width, watermark_height = watermark.size
            if watermark_width > width or watermark_height > height:
                watermark = watermark.resize((int(watermark_width / 2), int(watermark_height / 2)))

            position = request.args.get(f'position-{filename}', 'center')
            if position == 'center':
                x = int((width - watermark_width) / 2)
                y = int((height - watermark_height) / 2)
            elif position == 'top-left':
                x = 0
                y = 0
            elif position == 'top-right':
                x = width - watermark_width
                y = 0
            elif position == 'bottom-left':
                x = 0
                y = height - watermark_height
            elif position == 'bottom-right':
                x = width - watermark_width
                y = height - watermark_height
            else:
                x = int((width - watermark_width) / 2)
                y = int((height - watermark_height) / 2)

            image.paste(watermark, (x, y), mask=watermark)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], f'watermarked_{filename}'))

            images.append({
                'filename': f'watermarked_{filename}',
                'url': url_for('static', filename=f'uploads/watermarked_{filename}'),
                'position': position
            })

    return render_template('preview.html', watermark=watermark_filename, images=images)

if __name__ == '__main__':
    app.run(debug=True)
