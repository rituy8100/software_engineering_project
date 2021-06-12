from flask import Blueprint, url_for
from werkzeug.utils import redirect
import sys
import os

sys.path.append(os.getcwd() + '/..')
from projects.models import Diary
bp = Blueprint('main', __name__, url_prefix='/')


# --------------------------------- [edit] ---------------------------------- #
@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return redirect(url_for('diary._list'))