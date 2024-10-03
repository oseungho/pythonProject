"""
블루프린트는 Flask 애플리케이션의 구조를 더 모듈화하고, 라우트와 핸들러를 조직화하는데 도움을 주는 Flask의 기능입니다.
"""
# 1. 패키지 호출하기
from flask import Blueprint, render_template

# 2. 블루프린트 정의하기
bp = Blueprint('index', __name__, template_folder='../templates', static_folder='../static')

# 3. 특정 경로에 대한 라우트 정의하기
@bp.route('/')
def index():
    return render_template('index.html')



