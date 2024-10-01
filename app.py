"""
[패키지 호출을 위해 설치 - Terminal에서 아래 pip 코드 돌리기]
pip install Flask
pip install flask_restful
pip install flask_cors

애플리케이션 : 특정 작업이나 기능을 수행하기 위해 설계된 소프트웨어 프로그램
웹 애플리케이션 : 사용자가 웹 브라우저를 통해 상호작용하는 프로그램
               (백엔드{서버에서 데이터 처리&반환} + 프론트 엔드{사용자 인터페이스=UI 제공})
API 서버 : 애플리케이션 프러그래밍 인터페이스(API)를 제공하는 서버
          (UI를 제공하지 않고 데이터를 JSON, XML 등의 형식으로 주고 받음)
REST API : 라이언트와 서버 간의 상호작용을 단순하고 직관적으로 만들어주는 아키텍처 스타일 {REST 원칙을 준수하여 설계된 API}
          (고유한 URI로 식별하며 HTTP 메서드를 통해 정의 - GET, POST, PUT, DELETE)
모듈 : 파이썬 코드가 들어있는 하나의 파일 (변수, 함수, 클래스 등 정의 가능)
패키지 : 여러 모듈을 묶어놓은 디렉토리
CORS : 웹 애플리케이션이 다른 도메인, 프로토콜 또는 포트에서 리소스를 요청할 때 발생하는 보안 문제를 해결하기 위한 메커니즘(XSS, CSRF 등 잠재적인 보안 위협을 방지하기 위해 설계)
"""

from flask import Flask, render_template # Flask 패키지 호출
from flask_restful import Api # Flask 애플리케이션에서 RESTful API를 쉽게 구축할 수 있는 패키지
from flask_cors import CORS # Cross-Origin Resource Sharing을 처리하기 위해서 호출
from api.youtube_crawling import youtubeCrawling
from api.news_crawling import newsCrawling

# 플라스크 애플리케이션 생성
app = Flask(__name__) # __name__은 현재 모듈의 이름을 나타내는 특별한 변수로써 Flask는 이 값을 사용하여 애플리케이션의 위치를 파악

#CORS에러 처리
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
api.add_resource(youtubeCrawling, '/youtube')
api.add_resource(newsCrawling, '/news')

# 기본 경로('/')로 접속했을 때 index.html을 보여주는 라우트
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)


"""
# Flask란?
- Flask 패키지는 웹 애플리케이션을 쉽게 구성할 수 있는 프레임워크
-> Flask 내 Flask 함수를 활용하여 만든 app이 플라스크 앱인거고
-> flask_restful 패키지 내 Api 클래스를 활용한게 단순히 flask restful_api

"""
