from flask import Flask
from Controller.user_controller import user_bp
from config.database import db, init_db

app = Flask(__name__)

# 데이터베이스 설정 적용
init_db(app)

# 애플리케이션 시작 시 DB 초기화
with app.app_context():
    db.create_all()


# 블루프린트 등록
app.register_blueprint(user_bp, url_prefix='/user')  # user_bp 블루프린트를 등록하여 메모 관련 요청을 처리


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)