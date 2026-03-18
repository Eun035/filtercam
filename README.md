# Streamlit 이미지 필터 비교 앱

이 프로젝트는 웹캠 또는 카메라로 촬영한 이미지를 실시간으로 변환하고 비교할 수 있는 Streamlit 기반 애플리케이션입니다.

## 주요 기능

- 웹캠에서 이미지 촬영 (`st.camera_input`)
- 필터 선택
  - 원본
  - 회색조
  - Gaussian 블러 (파라미터 조절 지원)
  - Canny 엣지 (파라미터 조절 지원)
  - 세피아
  - 선명화
- 이미지 출력 (원본 / 필터 적용)
- PNG 파일 다운로드

## 요구사항

- Python 3.8+
- `opencv-python`
- `numpy`
- `streamlit`

## 설치

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` 예시:

```
streamlit
opencv-python
numpy
```

## 실행

```bash
streamlit run filter_app.py
```

## 요구사항 문서

### 1. 목적
- 웹캠을 실시간으로 받아서 필터를 적용하고 비교 화면을 제공

### 2. 기능
- 웹캠 이미지 입력
- 필터 6종
- 파라미터 슬라이더
- 결과 동시 비교 (원본 vs 필터)
- 파일 다운로드

### 3. 비기능
- 에러 핸들링 (camera_photo null, 인코딩 실패)
- OpenCV BGR/RGB 변환
- 확장성 : filter 함수 추가 시 쉽게 기능 확장 가능

### 4. 수용 기준
- 텍스트 안내 정상 표시
- 선택 필터 정상 작동
- 다운로드 정상 동작
