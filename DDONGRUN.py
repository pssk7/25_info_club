import streamlit as st
import random
import time

# --- 게임 설정 변수 ---
PLAYER_SIZE = 50  # 플레이어 캐릭터 크기 (픽셀)
POOP_SIZE = 30    # 똥 캐릭터 크기 (픽셀)
GAME_AREA_WIDTH = 500  # 게임 영역 너비 (픽셀)
GAME_AREA_HEIGHT = 400 # 게임 영역 높이 (픽셀)
POOP_SPEED = 7    # 똥이 한 프레임에 내려오는 픽셀 수 (클수록 빠름)
PLAYER_MOVE_SPEED = 25 # 플레이어가 한 번 움직일 때 이동하는 픽셀 수
POOP_GEN_PROB = 0.04 # 매 프레임마다 똥이 생성될 확률 (높을수록 많이 생성)
POINTS_PER_SECOND = 100 # 초당 획득 점수

# --- 게임 초기화 및 루프 함수 ---
def run_game():
    st.title("💩 똥피하기 게임 💩")

    # 세션 상태 변수 초기화 (페이지 새로고침에도 값 유지)
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'player_x' not in st.session_state:
        st.session_state.player_x = GAME_AREA_WIDTH / 2 - PLAYER_SIZE / 2 # 플레이어 초기 X 위치 (가운데)
    if 'poops' not in st.session_state:
        st.session_state.poops = [] # 현재 화면에 있는 똥들의 리스트 [(x, y), ...]
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = 0.0 # 게임 시작 시간 (밀리초)
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

    # 게임 시작/다시 시작 버튼 표시
    if not st.session_state.game_started and not st.session_state.game_over:
        if st.button("게임 시작"):
            # 게임 상태 초기화
            st.session_state.game_started = True
            st.session_state.player_x = GAME_AREA_WIDTH / 2 - PLAYER_SIZE / 2
            st.session_state.poops = []
            st.session_state.score = 0
            st.session_state.start_time = time.time() * 1000 # 현재 시간을 밀리초로 저장
            st.session_state.game_over = False
            st.experimental_rerun() # 게임 시작 후 즉시 화면 새로고침
    elif st.session_state.game_over:
        st.error(f"**게임 오버! 💩** 최종 점수: {st.session_state.score}점")
        if st.button("다시 시작"):
            # 게임 상태 초기화 및 재시작
            st.session_state.game_started = False
            st.session_state.game_over = False
            st.experimental_rerun()

    # 게임이 시작되었을 때만 게임 루프 실행
    if st.session
