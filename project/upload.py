from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db

upload = Blueprint('upload', __name__)

@upload.route('/')
def upload():
    pass
