# KDT Planning Dashboard

Streamlit을 사용한 KDT 계획 관리 대시보드입니다.

## 기능

- 📊 **홈 대시보드**: 프로젝트 현황과 메트릭을 한눈에 확인
- 📈 **데이터 분석**: CSV 파일 업로드 및 데이터 분석
- 📊 **시각화**: 다양한 차트와 지도 시각화
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

## 프로젝트 구조

```
kdt-planning/
├── app.py              # 메인 Streamlit 앱
├── requirements.txt    # 패키지 의존성
└── README.md          # 프로젝트 문서
```

## 사용법

1. 사이드바에서 원하는 페이지를 선택
2. 홈에서 전체 현황 확인
3. 데이터 분석 페이지에서 CSV 파일 업로드하여 분석
4. 시각화 페이지에서 다양한 차트 확인
5. 설정에서 개인화 옵션 조정

## 기술 스택

- **Streamlit**: 웹 앱 프레임워크
- **Pandas**: 데이터 처리
- **NumPy**: 수치 계산
- **Plotly**: 인터랙티브 차트
