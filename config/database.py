from flask_sqlalchemy import SQLAlchemy
import json

# SQLAlchemy 객체 생성 (Flask 인스턴스는 app.py에서 설정)
db = SQLAlchemy()

def open_json(file_path:str) -> json:
    with open(file_path, "r", encoding="utf-8") as f:
        # JSON 파일을 읽어서 파싱하여 반환
        return json.load(f)

# 데이터베이스 설정 함수
def init_db(app):
    # 하드코딩을 방지를 위해 분리
    db_login = open_json(r"config\db_login.json")
    # 여기서 직접 연결 정보 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_login["id"]}:{db_login["password"]}@localhost:3306/{db_login["db_name"]}' # DB URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # SQL 쿼리 로그 출력 (디버깅용)
    db.init_app(app)
