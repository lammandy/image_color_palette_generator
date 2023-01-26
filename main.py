# TODO upload image button

# TODO Display image onto website
# TODO For loop for different color swatches
# TODO numpy identfy colors
# TODO create chart for displaying Color and Color code

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os

import numpy as np
from PIL import Image


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
        file_path = 'static/drivers_license_front.jpeg'

    my_img = Image.open(file_path)
    img_array = np.array(my_img)
    print(img_array.shape)
    return render_template('index.html', form=form, file_path=file_path)

if __name__ == '__main__':
    app.run(debug=True)