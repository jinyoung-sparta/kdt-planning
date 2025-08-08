# KDT Planning Dashboard

Streamlit을 사용한 KDT 계획 관리 대시보드입니다.

## 기능

- 📊 **평가표**: 개발/비개발 과목별 평가 항목 관리
- 📝 **출제자 평가 템플릿**: 평가 템플릿 생성 및 편집
- 📤 **구글 스프레드시트 연동**: 평가 템플릿을 구글 스프레드시트로 내보내기
- ⚙️ **설정**: 사용자 설정 및 테마 관리

## 설치 및 실행

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 앱 실행:
```bash
streamlit run app.py
```

3. 브라우저에서 `http://localhost:8501`로 접속

## 구글 스프레드시트 연동 설정

구글 스프레드시트로 평가 템플릿을 내보내려면 다음 설정이 필요합니다:

### 1. Google Cloud Console 설정

1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. "APIs & Services" > "Library"로 이동
4. 다음 API들을 활성화:
   - Google Sheets API
   - Google Drive API

### 2. 서비스 계정 생성

1. "APIs & Services" > "Credentials"로 이동
2. "Create Credentials" > "Service Account" 선택
3. 서비스 계정 이름과 설명 입력
4. "Create and Continue" 클릭
5. 역할은 "Editor" 또는 "Owner" 선택 (권한 필요)
6. "Done" 클릭

### 3. 서비스 계정 키 다운로드

1. 생성된 서비스 계정 클릭
2. "Keys" 탭으로 이동
3. "Add Key" > "Create new key" 선택
4. "JSON" 형식 선택 후 "Create" 클릭
5. 다운로드된 JSON 파일을 프로젝트 폴더에 `credentials.json`으로 저장

### 4. 파일 구조 확인

```
kdt-planning/
├── app.py
├── requirements.txt
├── credentials.json          # 구글 서비스 계정 키 파일
├── credentials.json.example  # 예시 파일
└── README.md
```

⚠️ **주의사항**: `credentials.json` 파일은 민감한 정보이므로 Git에 커밋하지 마세요!

## 프로젝트 구조

```
kdt-planning/
├── app.py              # 메인 Streamlit 앱
├── requirements.txt    # 패키지 의존성
└── README.md          # 프로젝트 문서
```

## 사용법

### 기본 사용법

1. **평가표 설정**:
   - 사이드바에서 "평가표" 페이지 선택
   - 개발/비개발 과목 선택
   - 원하는 평가 항목들을 선택
   - "평가 템플릿에 추가" 버튼 클릭

2. **템플릿 편집**:
   - "출제자 평가 템플릿" 페이지로 이동
   - 평가 내용, 배점, 상/중/하 기준 등을 입력
   - 실시간으로 데이터 편집 가능

3. **구글 스프레드시트 내보내기**:
   - 스프레드시트 이름 입력
   - "스프레드시트로 내보내기" 버튼 클릭
   - 생성된 링크로 구글 스프레드시트에서 확인

### 템플릿 정보 확인

- 총 항목 수
- 작성된 평가 내용 수
- 배점 설정 완료 수

## 기술 스택

- **Streamlit**: 웹 앱 프레임워크
- **Pandas**: 데이터 처리
- **NumPy**: 수치 계산
- **Plotly**: 인터랙티브 차트
