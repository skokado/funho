from uuid import uuid4
from datetime import datetime
from flask import Flask
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.models import *
from src.database import db

def index_router(app):
    ## index
    @app.route('/')
    def index():
        topics = Topic.query.filter_by(owner=current_user.name, is_archived = False).all()
        return render_template('index.html', topics=topics)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            name = request.form['name']
            password = request.form['password']

            # エラーチェック
            error_message = ''
            if not name:
                error_message = 'ユーザ名を入力してください'
            elif User.query.filter_by(name=name).first():
                error_message = 'ユーザ名は既に使われています'
            elif not password:
                error_message = 'パスワードを入力してください'
            if error_message:
                flash(error_message, category='alert alert-danger')
                return render_template('signup.html')
            # データベースへの登録とログイン
            with app.app_context():
                user = User(
                    name = name,
                    password = generate_password_hash(password),
                    last_loggedin_at = datetime.now()
                )
                db.session.add(user)
                db.session.commit()
                login_user(user)
            return redirect('/')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            next_path = request.args.get('next')
            return render_template('login.html', next_path=next_path)
        elif request.method == 'POST':
            input_name = request.form['name']
            input_password = request.form['password']
            user = User.query.filter_by(name=input_name).first()
            # 認証
            if check_password_hash(user.password, input_password):
                login_user(user)
                # 最終ログイン日時を上書きする
                with app.app_context():
                    user.last_loggedin_at = datetime.now()
                    db.session.add(user)
                    db.session.commit()
                return redirect('/')
            else:
                flash('ログインに失敗しました。', category='alert alert-danger')
                redirect_path = request.args.get('next') if request.args.get('next') != 'None' else '/'
                return redirect(redirect_path)

    @app.route('/logout')
    def logout():
        # クッキーを削除した上でログアウトする
        logout_user()
        return redirect('/')

    @app.route('/createTopic', methods=['POST'])
    def create_topic():
        name = request.form['name']
        uuid = uuid4()
        topic = Topic(
            name = name,
            owner = current_user.name,
            uuid = uuid
        )
        with app.app_context():
            db.session.add(topic)
            db.session.commit()
        return redirect('/')

    @app.route('/topic/<uuid>')
    def topic(uuid):
        topic = Topic.query.filter_by(uuid=uuid).first()
        print(topic)
        # UUIDが正しいかチェック
        if not topic:
            return redirect('/'), 302
        posts = Post.query.filter_by(topic=uuid).all()
        return render_template('topic.html', topic=topic, posts=posts)

    @app.route('/post/<uuid>', methods=['POST'])
    def post(uuid):
        content = request.form['content']
        post = Post(
            topic = uuid,
            content = content
        )
        with app.app_context():
            db.session.add(post)
            db.session.commit()
        topic = Topic.query.filter_by(uuid=uuid).first()
        posts = Post.query.filter_by(topic=uuid).all()
        return redirect(f'/topic/{uuid}')

    @app.route('/topic/<uuid>/archive')
    def archive(uuid):
        topic = Topic.query.filter_by(uuid=uuid).first()
        with app.app_context():
            topic.is_archived = True
            db.session.commit()
        return redirect('/')