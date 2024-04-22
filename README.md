# UDC Voting System

학부생자회의 전자표결 시스템입니다.  
장고와 uvicorn을 이용하여 구현되어 있으며, 아래의 기능들이 구현되어 있습니다.

1. 관리자 계정을 통한 안건 관리 및 계정 관리
2. 메인 화면에서의 채팅 기능
3. 안건별 결과 확인

기본적으로 특정 단체에서 사용하는 것을 상정하고 개발하였기에 해당 단체에 맞추어 모든 명칭이 작성되어 있습니다.  
기본적으로 설정된 관리자 계정은 다음과 같습니다.  
username : UDC_president  
PW : !todwkghl1234  
관리자 페이지는 "기본페이지/admin"입니다.  
채팅 기능이 없는 기존의 버전을 확인하실 분은 아래의 링크를 참조해주세요.  
https://github.com/yangdongyeon/pythonanywhere  
  
필요한 package  
  
pip install django djangoframework  
pip install channels  
pip install channels_redis  
pip install uvicorn==0.11.3  
pip install "uvloop>=0.14.0"  
pip install whitenoise  

실행 단계
1. 필요한 package 전부 설치  
2. sudo apt install uvicorn  
3. sudo systemctl start redis  
4. python manage.py collectstatic  
5. uvicorn mysite.asgi:application --host 0.0.0.0 --port 8000  
6. http://외부IP:8000으로 접속
