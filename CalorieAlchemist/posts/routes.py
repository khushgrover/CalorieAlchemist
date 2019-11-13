from flask import render_template, url_for, flash, redirect, Blueprint, current_app
from flask_login import login_required, current_user
from CalorieAlchemist import db
from CalorieAlchemist.models import Post
from CalorieAlchemist.posts.forms import PostForm
from CalorieAlchemist.posts.utils import save_image
import keras
from keras.models import load_model
from PIL import Image
import numpy as np
import pandas as pd
from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
import tensorflow as tf
import cv2
import os

posts = Blueprint('posts', __name__)

def get_model():
    global model
    model = load_model('C:/Users/Rajesh Sharma/Desktop/CalorieAlchemist/CalorieAlchemist/models/model_keras.h5')

get_model()

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_image(form.picture.data)
        img = Image.open(form.picture.data)
        img = img_to_array(img)
        img = cv2.resize(img,(150,150))
        img = np.reshape(img,[1,150,150,3])
        pred=model.predict(img)
        if pred>0.5:
            label = 'Pizza'
            calories = '310'
        else:
            label = 'Samosa'
            calories = '240'
        post = Post(title=form.title.data, image_file=picture_file, author=current_user, label=label, calories=calories)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Image', form=form)