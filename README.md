---

## 프로젝트 소개
Selenium 기반 웹 자동화와 JSON 데이터 관리 기능을 제공하는 Python 프로젝트입니다.  

---

# Git & GitHub 사용법 가이드

## 각자의 브랜치에서 코드를 수정하고 커밋할때 주의점
## master 브랜치로 병합하기 전에 꼭 팀원들에게 알려줘야 합니다! 

1. 개인 브랜치에서 작업
2. commit 
3. push
4. Merge Request -> 저희 깃랩 사이트에 머지 리퀘스트 버튼이 생성되더라구요
5. 리뷰 후 merge 버튼 클릭
   * 옵션에 delete branch 머시기 해제하기!!!
6. 머지 완료

7. 다른 사람이 머지 한것을 항상 업데이트!
   * 개인 브랜치에서 pull 
   * git hub desktop 쓰시는 분들 fetch -> pull 

8. 12/15 commit JIRA 프로젝트 키 업데이트<br>
git commit -m "QHCQ-37 <message>" <br>


# git사용시 유용한 것들
1. git checkout master <br>
2. 최근 커밋 확인 <br>
git log --oneline <br>
3. 변경 사항 비교 <br>
git diff <br>
4. 특정 커밋 되돌리기 <br>
git revert <commit_id>

## coverage 사용 간단 가이드
## report에서 
### Stmts 명령문 수, Miss는 실행 X 명령문 수
### Cover 커버리지 수, Missing은 Miss 명련문의 줄 번호

1. 브랜치 커버리지 + app 패키지 기준 리포트용 git 명령어
- coverage run -m pytest

2. tests 폴더 기준 명령어(--source로 폴더 지정)
- coverage run --source=tests -m pytest

3. 특정 패키지만 보고 싶을 때
- coverage report --include="app/*"

4. 특정 패키지만 제외
- coverage report --omit="tests/*"

5. 상위 명령어 실행 후 터미널에서 간단 리포트 확인
- coverage report

6. 상위 명령어 html root에 htmlcov 경로에 html report 생성
- coverage html

---

## 설치
```bash

# 가상환경 생성 (Python 3.11.9 기준)
python -m venv .venv      
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 패키지 설치
pip install -r requirements.txt


## 기술 스택
Python 3.11
Selenium
webdriver-manager
JSON 데이터 처리

📁 각 폴더에 대한 상세한 설명
helpychat-project/
├─ reports/
│   ├─ logs/          # 테스트 실행 로그
│   └─ screenshots/   # 테스트 실패/성공 시 캡처된 스크린샷
│
├─ src/
│   ├─ config/        # 환경별 URL, 브라우저 옵션 등 설정 파일
│   ├─ managers/      # DriverManager, FileManager 등 관리 클래스
│   ├─ pages/         # Page Object Model(POM) 클래스
│   ├─ resources/     # 테스트 데이터 및 이미지 리소스
│   └─ utils/         # 공통 유틸리티 함수 및 도구
│       ├─ defines.py # Selector, XPath 등 관리
│       └─ headers.py # 헤더 정보 관리
├─ tests/
│   ├─ conftest.py    # 테스트 초기 설정 관리(fixture 등)
│   └─ test_main.py   # 실제 Pytest 테스트 케이스
│
├─ pytest.ini          # Pytest 실행 옵션 (ex: pythonpath=src)
├─ requirements.txt    # 프로젝트 Python 패키지 명시
└─ Jenkinsfile         # CI/CD 파이프라인 정의
