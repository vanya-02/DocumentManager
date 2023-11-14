# the non-auth routes for the app

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

