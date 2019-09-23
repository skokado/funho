from flask import Flask, request, render_template
from flask_login import LoginManager, current_user
from src.database import db, init_db
from src.models.models import *
from src.views.index import index_router
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SUPER_SECRET_KEY']
init_db(app)

# デフォルト処理の定義
@app.before_request
def before_request():
    if '/static' in request.path:
        # static 配下のファイルはそのまま表示する
        pass
    elif request.path.startswith('/signup') or request.path.startswith('/login'):
        # サインアップページ, ログインページはそのまま表示する
        pass
    elif not current_user.is_authenticated:
        # 非ログインユーザはログインページに誘導する
        return render_template('unauthorized.html'), 302

# ログイン処理における認証ユーザの呼び出し方法の定義
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

# 404エラーハンドラ
# @app.errorhandler(404)
# def page_not_found(error):
#   return render_template('404.html'), 404

# View(ルーティング)の呼び出し
index_router(app)