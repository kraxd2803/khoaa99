import streamlit as st
import random
import time
import base64
import os

def get_audio_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def play_bgm(file_path):
    base64_audio = get_audio_base64(file_path)
    if base64_audio:
        # Sử dụng thuộc tính controls để kiểm tra xem nhạc có load được không
        # Sau khi nhạc chạy ok, bạn có thể xóa chữ 'controls' và thêm 'style="display:none"'
        audio_html = f"""
            <audio autoplay loop id="bgm-player" controls> 
                <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
            </audio>
            <script>
                var audio = document.getElementById("bgm-player");
                audio.volume = 0.3;
                // Buộc trình duyệt phát lại nếu bị chặn
                document.body.addEventListener("click", function() {{
                    audio.play();
                }}, {{ once: true }});
            </script>
        """
        st.components.v1.html(audio_html, height=50)

def play_local_audio(file_path):
    base64_audio = get_audio_base64(file_path)
    if base64_audio:
        audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
            </audio>
        """
        st.components.v1.html(audio_html, height=0)


# 1. Khởi tạo State
if 'machine_emoji' not in st.session_state:
    st.session_state.machine_emoji = "❓"
if 'last_result' not in st.session_state:
    st.session_state.last_result = None
if 'p' not in st.session_state:
    st.session_state.p = 1000


st.set_page_config(page_title="KHOAA777", page_icon="💸")
st.title("VÒNG QUAY MAY MẮN🎰")
st.caption("Made by Đăng Khoa 🔰")
on_music = st.toggle("Nhạc nền", value=False)

if on_music==True:
    play_bgm("bgm.mp3")
emoji_list = ["🍎", "🍊", "🍇", "🍓", "🍉", "🍒"]


# 2. Hiển thị thông báo kết quả (Nếu có)
if st.session_state.last_result == "win":
    play_local_audio("win.mp3")
    st.balloons()
    st.success(f"MAY ĐẤY! Máy đã ra {st.session_state.machine_emoji}")
elif st.session_state.last_result == "loss":
    play_local_audio("lose.mp3")
    st.error(f"CÚNG RỒI NHA HẸ HẸ =)) Máy đã ra {st.session_state.machine_emoji}")

# 3. Bố cục 2 cột
col1, col2 = st.columns(2)
with col1:
    st.subheader("Máy chọn")
    st.markdown(f"<div style='font-size: 100px; text-align: center; border: 5px solid #555; border-radius: 15px;'>{st.session_state.machine_emoji}</div>", unsafe_allow_html=True)

with col2:
    st.subheader("Bạn chọn")
    st.write(f"SỐ ĐIỂM HIỆN CÓ {st.session_state.p}")
    user_choice = st.selectbox("Chọn Emoji:", emoji_list)
    st.markdown(f"<div style='font-size: 100px; text-align: center;'>{user_choice}</div>", unsafe_allow_html=True)

# 4. Nút bấm
if st.button("QUAY SỐ", use_container_width=True):
    st.toast("Đang quay...", icon="🎲")

    play_local_audio("spin.mp3")
    placeholder = st.empty()
    sl=30
    for i in range(sl):
        temp = random.choice(emoji_list)
        placeholder.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{temp}</h1>", unsafe_allow_html=True)
        toc_do = 0.05 + (i / sl) * 0.2 
        time.sleep(toc_do)
    
    placeholder.empty()
    kq = random.choice(emoji_list)
    
    # Cập nhật State để hiển thị sau khi rerun
    st.session_state.machine_emoji = kq
    if st.session_state.p<=500:
        st.session_state.last_result = "win"
        st.session_state.p+=50
    elif kq == user_choice and st.session_state.p>500:
        st.session_state.last_result = "win"
        st.session_state.p+=50
    else:
        st.session_state.last_result = "loss"
        st.session_state.p-=50

    st.rerun()
