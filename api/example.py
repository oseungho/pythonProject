from flask import request
from flask_restful import Resource

"""
1. Resource를 인자로 전달하는 이유?
    - Resource는 Flask-RESTful에서 제공하는 클래스로, RESTful API를 구현할 때 사용됩니다.
    - Resource 클래스를 상속받으면 HTTP 메서드(GET, POST, PUT, DELETE)를 쉽게 정의할 수 있습니다.
    - Resource를 상속받지 않으면, 추후 __init__.py에서 
        api.add_resource(youtubeCrawling, '/youtube')로 사용을 못하고
        
        api.add_url_rule('/youtube_crawling', view_func=YoutubeCrawling().get, methods=['GET'])
        이런 식으로 메서드를 호출하기 위해 인스턴스를 만들어야 합니다.
"""

class youtubeCrawling(Resource): # from flask_restful import Resource 추가
    def get(self): # HTTP GET 요청을 처리하는 메서드
        search = request.args.get('search') #
        return 0

    def post(self): # HTTP POST 요청을 처리하는 메서드
        return 0

"""
[설명 순서]
    1. 클래스 정의 하기
        -> Resource를 인자로 부여하는 이유
            + from flask_restful import Resource 
        -> 상속이란? 인자란? 메서드란? 인스턴스란?
    2. GET or POST 메서드 정의하기  
        -> GET 방식 / POST 방식
        -> request란?
            + from flask import request
    3. 받아올 값을 정하기
        get -> request.args.get('')
        post -> request.json['']
"""