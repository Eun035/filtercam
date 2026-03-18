import streamlit as st

try:
    import cv2
except ModuleNotFoundError:
    st.error("`opencv-python` 또는 `opencv-python-headless` 를 설치해야 합니다.\n`pip install opencv-python-headless` 실행 후 재시도하세요.")
    st.stop()

import numpy as np

# ==========================================
# 1. 필터 함수 정의
# ==========================================
def apply_original(img):
    return img

def apply_grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Streamlit에서 원본과 나란히 표시할 때 채널 수를 맞추기 위해 다시 BGR 구조로 변환
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def apply_blur(img, ksize):
    # ksize는 홀수여야 함
    return cv2.GaussianBlur(img, (ksize, ksize), 0)

def apply_canny(img, t1, t2):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, t1, t2)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def apply_sepia(img):
    # OpenCV는 BGR 순서이므로 이에 맞춘 세피아 변환 행렬 적용
    kernel = np.array([
        [0.131, 0.534, 0.272],
        [0.168, 0.686, 0.349],
        [0.189, 0.769, 0.393]
    ])
    sepia = cv2.transform(img, kernel)
    return np.clip(sepia, 0, 255).astype(np.uint8)

def apply_sharpening(img):
    # 선명화를 위한 커널(Kernel) 생성
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(img, -1, kernel)


# ==========================================
# 2. Streamlit 웹 앱 UI 구성
# ==========================================
# 페이지 기본 설정
st.set_page_config(page_title="이미지 필터 비교 앱", layout="wide")
st.title("🎨 이미지 필터 비교 앱")

# --- 사이드바 (필터 설정) ---
st.sidebar.header("⚙️ 필터 설정")
filter_options = [
    "1. 원본", 
    "2. 회색조", 
    "3. Gaussian 블러", 
    "4. Canny 엣지", 
    "5. 세피아", 
    "6. 선명화"
]
selected_filter = st.sidebar.selectbox("적용할 필터를 선택하세요", filter_options)

# 선택한 필터에 따라 동적으로 슬라이더 표시
ksize = 5
t1, t2 = 100, 200

if selected_filter == "3. Gaussian 블러":
    ksize = st.sidebar.slider("블러 커널 크기 (홀수)", min_value=1, max_value=31, value=5, step=2)
elif selected_filter == "4. Canny 엣지":
    t1 = st.sidebar.slider("Threshold 1 (최소 임계값)", min_value=0, max_value=500, value=100)
    t2 = st.sidebar.slider("Threshold 2 (최대 임계값)", min_value=0, max_value=500, value=200)


# --- 메인 화면 (웹캠 사진 촬영) ---
# file_uploader 대신 camera_input 사용
camera_photo = st.camera_input("📸 웹캠으로 사진을 찍어 필터를 적용해 보세요")

if camera_photo is not None:
    # 촬영된 사진을 읽어와서 OpenCV 형식으로 변환
    file_bytes = np.frombuffer(camera_photo.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # (이후 필터 적용 및 화면 분할 코드는 기존과 동일하게 유지)
    # 필터 적용
    if selected_filter == "1. 원본":
        filtered_img = apply_original(img)
    elif selected_filter == "2. 회색조":
        filtered_img = apply_grayscale(img)
    elif selected_filter == "3. Gaussian 블러":
        filtered_img = apply_blur(img, ksize)
    elif selected_filter == "4. Canny 엣지":
        filtered_img = apply_canny(img, t1, t2)
    elif selected_filter == "5. 세피아":
        filtered_img = apply_sepia(img)
    elif selected_filter == "6. 선명화":
        filtered_img = apply_sharpening(img)
    

    # --- 화면 분할 및 결과 출력 ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ 원본 이미지")
        # OpenCV의 BGR을 웹 표시를 위해 RGB로 변환
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_container_width=True)
        
    with col2:
        st.subheader(f"✨ 필터 적용: {selected_filter.split('. ')[1]}")
        st.image(cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB), use_container_width=True)

    # --- 다운로드 버튼 ---
    st.markdown("---")
    # 저장할 이미지를 PNG 포맷의 바이트 데이터로 인코딩
    is_success, buffer = cv2.imencode(".png", filtered_img)
    if is_success:
        st.download_button(
            label="📥 필터 적용 이미지 다운로드",
            data=buffer.tobytes(),
            file_name=f"filtered_{selected_filter.split('. ')[1]}.png",
            mime="image/png"
        )
else:
    st.info("👆 위에 있는 업로드 버튼을 눌러 이미지를 추가해 보세요.")