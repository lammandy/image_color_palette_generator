# TODO upload image button
# TODO Display image onto website

# TODO For loop for different color swatches
# TODO identfy colors

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os

import numpy as np
from PIL import Image
import cv2 as cv


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__)
Bootstrap(app)

WTF_CSRF_SECRET_KEY = 'a random string'
app.config['SECRET_KEY'] = WTF_CSRF_SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        file_path = 'static/' + filename
        f.save(os.path.join(
            file_path))
    else:
        file_path = 'static/MG_7905.jpg'

    my_img = Image.open(file_path)

    centers = find_top_colors(my_img)

    rgb = []
    colors = []
    hex_color_codes =[]
    count = 0

    for i in range(10):
        for j in range(3):
            rgb.append(centers[i][j])
            count += 1
            if count % 3 == 0:
                color = int(rgb[count-3]), int(rgb[count-2]), int(rgb[count-1])
                colors.append(color)

    for idx, color in enumerate(colors):
        hex_color_codes.append((idx, rgb_to_hex(color[0], color[1], color[2])))
    for i in range(10):
        im = Image.new('RGB', (200,100), colors[i])
        im.save('static/' + str(i) + '.PNG')
    return render_template('index.html', form=form, file_path=file_path, hex_color_codes=hex_color_codes)

def find_top_colors(image):
    img_array = np.array(image)

    height, width, _ = np.shape(img_array)

    # cluster of the data
    data = np.reshape(img_array, (height * width, 3))
    data = np.float32(data)

    number_clusters = 10

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv.kmeans(data, number_clusters, None, criteria, 10, flags)
    return centers

def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)

if __name__ == '__main__':
    app.run(debug=True)