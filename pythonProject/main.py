# 1. 패키지 호출하기
from app import create_app

# 2. 플라스크 앱 생성하기
app = create_app()

# 3. 애플리케이션 실행하기
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


