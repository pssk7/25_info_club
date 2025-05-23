import streamlit as st
import random

# --- 일본 애니 노래 데이터 (2025년 기준 인기 예상곡 및 번역 가사 포함) ---
# 실제 2025년 인기 TOP 10은 알 수 없으므로, 현재 인기곡과 예상 인기곡을 조합했습니다.
# 각 노래 제목과 해당 노래의 대표적인 한국어 번역 가사 (예시)
# 실제 앱에서는 각 노래의 특징적인 가사를 더 길게, 정확하게 번역하여 작성해야 합니다.
anime_song_data = {
    "YOASOBI - アイドル (Idol)": "완벽하고 궁극적인 아이돌",
    "Linked Horizon - 紅蓮の弓矢 (홍련의 화살)": "그들은 구축해야 할 적이다",
    "Kenshi Yonezu - Kick Back": "노력, 미래, 아름다운 별",
    "Official HIGE DANdism - Cry Baby": "멱살을 잡혀 억지로",
    "LiSA - 炎 (불꽃)": "꿈의 조각이 흘러넘쳐",
    "Ado - 新時代 (신시대)": "두려워하지 마, 떨지 마",
    "King Gnu - 一途 (일편단심)": "하얗게 내리는 눈처럼",
    "Kana-Boon - シルエット (실루엣)": "그날의 너의 모습이 희미하게 보였어",
    "Uru - プロローグ (프롤로그)": "눈을 감으면 언제나 그곳에 네가 있어",
    "Mrs. GREEN APPLE - 青と夏 (푸름과 여름)": "달리기 시작한 우리들의 여름"
}

# --- 게임 초기화 함수 ---
def initialize_game():
    st.session_state.score = 0
    st.session_state.current_question_num = 0
    # 모든 노래 제목을 가져와 섞어서 문제 출제용으로 사용
    st.session_state.available_songs = list(anime_song_data.keys())
    random.shuffle(st.session_state.available_songs)
    st.session_state.quiz_songs = st.session_state.available_songs[:3] # 총 3문제만 출제
    st.session_state.game_started = False
    st.session_state.game_over = False

# --- Streamlit 앱 설정 ---
st.set_page_config(page_title="애니 노래 가사 맞추기 퀴즈", layout="centered")

st.title("🎧 일본 애니 노래 가사 (번역) 맞추기 퀴즈! 🎤")
st.markdown("### 과연 당신은 진정한 애니 덕후인가?")
st.markdown("---")

# 세션 상태 초기화
if 'game_started' not in st.session_state:
    initialize_game()

# 게임 시작 화면
if not st.session_state.game_started:
    st.write("랜덤으로 선정된 일본 애니 노래의 **한국어 가사**를 보고 어떤 노래인지 맞춰보세요!")
    st.write("총 **3문제**가 출제되며, 각 문제당 3개의 보기가 주어집니다.")
    if st.button("✨ 퀴즈 시작 ✨"):
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
        # 해당 노래의 한국어 번역 가사
        lyrics_hint = anime_song_data[correct_song]

        st.subheader(f"문제 {current_q_idx + 1}/{len(st.session_state.quiz_songs)}")
        st.markdown("--- 가사 (한국어 번역) ---")
        st.info(f"**🎵 '{lyrics_hint}' 🎵**")
        st.markdown("------------")
        st.write("이 가사는 어떤 일본 애니 노래의 일부일까요?")

        # 오답 2개를 포함한 3개의 보기 생성
        # 전체 노래 리스트에서 정답을 제외하고, 2개를 무작위로 선택
        other_songs = [s for s in anime_song_data.keys() if s != correct_song]
        random_incorrect_songs = random.sample(other_songs, 2)
        
        # 정답과 오답을 합쳐서 보기 리스트 생성 후 섞기
        options = [correct_song] + random_incorrect_songs
        random.shuffle(options)

        # 사용자에게 보기 제시
        selected_answer = st.radio("정답을 선택하세요:", options, key=f"q{current_q_idx}")

        if st.button("✅ 정답 확인"):
            if selected_answer == correct_song:
                st.balloons() # 정답 시 풍선 효과
                st.success("🎉 정답입니다! 🎉")
                st.session_state.score += 1
            else:
                st.error(f"❌ 틀렸습니다! 정답은 **{correct_song}** 입니다.")
            
            # 다음 문제로 이동
            st.session_state.current_question_num += 1
            st.experimental_rerun() # 다음 문제로 넘어가기 위해 새로고침

# 게임 종료 화면
elif st.session_state.game_over:
    st.subheader("🎉 퀴즈 종료! 🎉")
    st.write(f"당신의 최종 점수는 **{len(st.session_state.quiz_songs)}점 만점에 {st.session_state.score}점**입니다!")

    if st.session_state.score == len(st.session_state.quiz_songs):
        st.balloons()
        st.success("💯 와우! 당신은 진정한 애니 노래 마스터입니다! 💯")
    elif st.session_state.score >= len(st.session_state.quiz_songs) / 2:
        st.info("👍 잘하셨어요! 애니 노래에 대한 지식이 꽤 있으시네요. 👍")
    else:
        st.warning("😅 아쉽지만, 다음번엔 더 좋은 결과를 기대해봅니다! 😅")


    if st.button("🔄 다시 플레이"):
        initialize_game()
        st.experimental_rerun()

st.markdown("---")
st.caption("**주의:** 이 앱의 2025년 인기 애니 노래 TOP 10은 임의로 선정된 것이며, 실제 순위와 다를 수 있습니다. 가사도 예시 및 번역본입니다.")
st.caption("Powered by Streamlit")
