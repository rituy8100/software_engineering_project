from flask import Blueprint, render_template ,request,url_for,session
from werkzeug.utils import redirect
from datetime import datetime
import sys
import os

sys.path.append(os.getcwd() + '/..')
from projects.models import Diary
from projects.forms import DiaryForm
from projects.views.auth_views import login_required
from projects.models import User
bp = Blueprint('diary', __name__, url_prefix='/diary')
from projects.app import db

# --------------------------------- [edit] ---------------------------------- #

@bp.route('/list/')
@login_required
def _list():
    page = request.args.get('page', type=int, default=1)
    diary_list = Diary.query.filter(Diary.user_id==session.get('user_id')).order_by(Diary.create_date.desc())
    diary_list = diary_list.paginate(page, per_page=10)
    return render_template('diary/diary_list.html', diary_list=diary_list)

@bp.route('/detail/<int:diary_id>/')
@login_required
def detail(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    return render_template('diary/diary_detail.html', diary=diary)

@bp.route('/create/',methods=('GET','POST'))
@login_required
def create():
    form = DiaryForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_id = session.get('user_id')
        question = Diary(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user_id=user_id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('diary/diary_form.html', form=form)

@bp.route('/modify/<int:diary_id>', methods=('GET', 'POST'))
@login_required
def modify(diary_id):
    diary = Diary.query.get(diary_id)
    form = DiaryForm(obj=diary)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(diary)
        diary.modify_date = datetime.now()  # 수정일시 저장
        db.session.commit()
        return redirect(url_for('diary.detail', diary_id=diary_id))
    # else:
    #     form = DiaryForm(obj=diary)
    return render_template('diary/diary_form.html', form=form)

@bp.route('/delete/<int:diary_id>')
@login_required
def delete(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    db.session.delete(diary)
    db.session.commit()
    return redirect(url_for('diary._list'))