import streamlit as st
import random

# --- 노래 데이터 ---
# 노래 제목과 해당 노래의 대표적인 가사 (예시)
# 실제 앱에서는 각 노래의 가사를 더 길게, 특징적으로 작성해야 합니다.
song_data = {
    "Shinzou wo Sasageyo": "바쳐라! 바쳐라! 모든 걸 바쳐라!",
    "YOU (I)": "You, who is similar to me, a small voice that only I knew",
    "The Peak": "끝없이 펼쳐진 세상 속에서 우리는",
    "10 minutes": "10분 안에 내게 넘어오게 할 거야",
    "두 번째 고백": "널 사랑한단 말이야 어색해서",
    "붉은 노을": "붉은 노을에 비친 너의 모습은",
    "Say I Love You (우디)": "말하기 어려웠던 사랑한단 그 말",
    "FANTASTIC BABY": "Boom Shaka Laka Boom Shaka Laka",
    "그 아픔까지 사랑한거야": "내 모든 걸 다 주어도 아깝지 않아",
    "좋은 밤 좋은 꿈": "오늘 밤도 너와 함께 좋은 꿈 꿀 거야",
    "미안해서 미안해": "미안해서 미안해 나의 사랑아",
    "주저하는 연인들을 위해": "사랑이 아니라 말하지 마",
    "어땠을까 (feat. 박정현)": "만약 우리 둘이 조금만 더",
    "사랑하긴 했었나요 스쳐가는 인연이었나요": "나는 알았어 처음 본 순간부터",
    "듣고 싶을까": "내 얘길 들어줄까",
    "사랑인가봐": "사랑인가봐 널 보면 심장이",
}

# --- 게임 초기화 함수 ---
def initialize_game():
    st.session_state.score = 0
    st.session_state.current_question_num = 0
    # 모든 노래 제목을 가져와 섞어서 문제 출제용으로 사용
    st.session_state.available_songs = list(song_data.keys())
    random.shuffle(st.session_state.available_songs)
    st.session_state.quiz_songs = st.session_state.available_songs[:3] # 3문제만 출제
    st.session_state.game_started = False
    st.session_state.game_over = False

# --- Streamlit 앱 설정 ---
st.set_page_config(page_title="노래 가사 맞추기 앱", layout="centered")

st.title("🎵 노래 가사 맞추기 퀴즈 🎵")
st.markdown("---")

# 세션 상태 초기화
if 'game_started' not in st.session_state:
    initialize_game()

# 게임 시작 화면
if not st.session_state.game_started:
    st.write("랜덤으로 선정된 가사를 보고 어떤 노래인지 맞춰보세요! 총 3문제입니다.")
    if st.button("게임 시작"):
        st.session_state.game_started = True
        st.experimental_rerun() # 게임 시작 후 새로고침

# 게임 진행 화면
elif st.session_state.game_started and not st.session_state.game_over:
    current_q_idx = st.session_state.current_question_num
    
    # 더 이상 문제가 없으면 게임 종료
    if current_q_idx >= len(st.session_state.quiz_songs):
        st.session_state.game_over = True
        st.experimental_rerun()
    else:
        # 현재 문제의 정답 노래
        correct_song = st.session_state.quiz_songs[current_q_idx]
        # 해당 노래의 가사
        lyrics_hint = song_data[correct_song]

        st.subheader(f"문제 {current_q_idx + 1}")
        st.write(f"--- 가사 ---")
        st.info(f"**{lyrics_hint}**")
        st.write(f"------------")
        st.write("이 가사는 어떤 노래의 일부일까요?")

        # 오답 2개를 포함한 3개의 보기 생성
        # 전체 노래 리스트에서 정답을 제외하고, 2개를 무작위로 선택
        other_songs = [s for s in song_data.keys() if s != correct_song]
        random_incorrect_songs = random.sample(other_songs, 2)
        
        # 정답과 오답을 합
