import streamlit as st
import random
import time

# --- 게임 설정 변수 ---
ROOM_COUNT = 3
HINT_PENALTY_SCORE = 50 # 힌트 사용 시 점수 패널티
GAME_END_SCORE_BONUS = 500 # 게임 성공 시 추가 점수

# --- 암호화 관련 함수 ---
# 1. 단일 치환 암호 함수
def encrypt_substitution(text, key_map):
    encrypted_text = ""
    for char in text:
        if char in key_map:
            encrypted_text += key_map[char]
        else:
            encrypted_text += char
    return encrypted_text

# 2. 시저 암호 함수
def encrypt_caesar(text, shift):
    encrypted_text = ""
    for char in text:
        if '가' <= char <= '힣': # 한글 범위
            start = ord('가')
            end = ord('힣')
            char_code = ord(char)
            new_code = start + (char_code - start + shift) % (end - start + 1)
            encrypted_text += chr(new_code)
        elif 'a' <= char <= 'z':
            encrypted_text += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
        elif 'A' <= char <= 'Z':
            encrypted_text += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            encrypted_text += char # 특수문자, 숫자 등은 그대로
    return encrypted_text

# 3. RSA 소인수분해 문제 설정 함수 (간단한 예시)
def get_rsa_puzzle():
    # 게임 난이도에 따라 P와 Q를 조절하세요.
    # 너무 크면 계산이 어려워지므로 적절한 수준으로.
    primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47] # 사용할 소수 목록
    
    # 서로 다른 두 소수를 랜덤으로 선택
    p = random.choice(primes)
    q = random.choice([pr for pr in primes if pr != p])
    
    n = p * q
    return n, p, q

# --- 게임 초기화 함수 ---
def init_game_state():
    st.session_state.current_room = 1
    st.session_state.puzzle_solved = [False] * (ROOM_COUNT + 1) # 각 방 퍼즐 해결 여부
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.show_hint = [False] * (ROOM_COUNT + 1)

    # 1번 방 (단일 치환) 설정
    room1_messages = ["면목고 축제에 온걸 환영해", "우리 부스에 와줘서 고마워"]
    st.session_state.room1_original_message = random.choice(room1_messages)
    # 단일 치환 키 (예시) - 실제 게임에서는 더 복잡하게 만들 수 있습니다.
    # 'ㅁ'을 '☆'으로 치환, 'ㅎ'을 '◎'으로, 'ㅏ'를 '＋'로, 'ㅐ'를 '－'로
    st.session_state.room1_key_map = {
        'ㅁ': '☆', 'ㅎ': '◎', 'ㅏ': '＋', 'ㅐ': '－', 'ㅇ': '●', 'ㅜ': '▲', 'ㅗ': '▼'
        # 실제 암호화할 문장의 모든 글자에 대한 치환 규칙을 정의하거나
        # 랜덤하게 매핑하는 로직을 추가할 수 있습니다.
        # 예시: 'ㄱ': 'A', 'ㄴ': 'B' ... (완전 랜덤으로 키를 생성하는 로직 추가 가능)
    }
    # 더 많은 글자 추가 및 랜덤 키 생성
    hangul_chars = "가나다라마바사아자차카타파하기니디리미비시이지치키티피히" # 예시
    shuffled_chars = list(hangul_chars)
    random.shuffle(shuffled_chars)
    for i, char in enumerate(hangul_chars):
        if char not in st.session_state.room1_key_map:
            st.session_state.room1_key_map[char] = shuffled_chars[i]


    st.session_state.room1_encrypted_message = encrypt_substitution(
        st.session_state.room1_original_message, st.session_state.room1_key_map
    )

    # 2번 방 (시저 암호) 설정
    room2_messages = ["면목고 축제를 편하게 즐겨줘", "우리 부스를 편하게 즐겨줘"]
    st.session_state.room2_original_message = random.choice(room2_messages)
    st.session_state.room2_shift = random.randint(3, 7) # 이동 값 랜덤 (3~7)
    st.session_state.room2_encrypted_message = encrypt_caesar(
        st.session_state.room2_original_message, st.session_state.room2_shift
    )

    # 3번 방 (RSA 소인수분해) 설정
    st.session_state.room3_original_message = "감사합니다"
    st.session_state.room3_n, st.session_state.room3_p, st.session_state.room3_q = get_rsa_puzzle()

# --- 게임 실행 함수 ---
def run_game():
    st.set_page_config(layout="wide") # 넓은 레이아웃 사용
    st.title("면목고 미스터리: 방 탈출 게임 🗝️")
    st.markdown("---")

    # 게임 상태 초기화 (최초 실행 시 또는 다시 시작 시)
    if 'game_started' not in st.session_state:
        init_game_state()

    # 게임 시작/다시 시작 버튼
    if not st.session_state.game_started and not st.session_state.game_over:
        st.write("""
        면목고 축제가 한창이던 어느 날, 당신은 갑자기 낯선 교실에 갇혔습니다.
        창문 밖은 어둠에 잠겨 있고, 휴대폰은 먹통입니다.
        스피커에서 기분 나쁜 목소리가 흘러나옵니다.

        "어서 와, 면목고에 온 걸 환영한다. 이제 너의 지혜를 시험할 시간이야.
        세 개의 방을 통과해야만 이 미스터리한 공간에서 벗어날 수 있을 거야."

        과연 당신은 면목고의 비밀을 풀고 탈출할 수 있을까요?
        """)
        if st.button("게임 시작", key="start_game_button"):
            init_game_state() # 게임 상태 초기화
            st.session_state.game_started = True
            st.experimental_rerun() # 화면 새로고침하여 게임 시작
    elif st.session_state.game_over:
        st.balloons() # 게임 성공 시 풍선 효과
        st.success(f"🎉 **탈출 성공!** 축하합니다! 최종 점수: {st.session_state.score}점")
        if st.button("다시 플레이하기", key="restart_game_button"):
            init_game_state()
            st.experimental_rerun()
    elif st.session_state.game_started:
        # --- 게임 루프 (각 방 표시) ---
        display_game_room()

# --- 각 방을 표시하는 함수 ---
def display_game_room():
    st.header(f"현재 방: {st.session_state.current_room} / {ROOM_COUNT}")
    st.markdown("---")

    elapsed_time = int(time.time() - st.session_state.start_time)
    st.sidebar.markdown(f"**경과 시간: {elapsed_time}초**")
    st.sidebar.markdown(f"**현재 점수: {st.session_state.score}점**")

    if st.session_state.current_room == 1:
        room1_puzzle()
    elif st.session_state.current_room == 2:
        room2_puzzle()
    elif st.session_state.current_room == 3:
        room3_puzzle()
    else:
        # 모든 방 클리어
        if not st.session_state.game_over:
            st.session_state.score += GAME_END_SCORE_BONUS # 최종 보너스 점수
            st.session_state.game_over = True
            st.experimental_rerun() # 게임 오버 화면으로 이동

# --- 1번 방 퍼즐 ---
def room1_puzzle():
    st.subheader("첫 번째 방: 뒤섞인 글자 (단일 치환 암호)")
    st.write("칠판에 알 수 없는 기호와 글자들이 적혀 있습니다. 주어진 단서를 활용해 암호를 해독하세요.")

    st.markdown(f"**암호문**: `{st.session_state.room1_encrypted_message}`")

    st.info("""
    **단서:**
    - 힌트 1: 'ㅁ'은 '☆'으로 치환됩니다.
    - 힌트 2: 'ㅎ'은 '◎'으로 치환됩니다.
    - 칠판 한쪽 구석에 작은 표: `ㅏ -> ＋`, `ㅐ -> －`, `ㅇ -> ●`, `ㅜ -> ▲`, `ㅗ -> ▼`
    """)

    # 힌트 보기/숨기기
    with st.expander("더 많은 힌트 보기 (점수 감점!)"):
        if st.button("힌트 사용", key="hint1_button"):
            st.session_state.score = max(0, st.session_state.score - HINT_PENALTY_SCORE)
            st.session_state.show_hint[1] = True
            st.experimental_rerun() # 힌트 보여주기 위해 새로고침
        if st.session_state.show_hint[1]:
            st.write(f"원래 문장은 **`{st.session_state.room1_original_message[0]}...`** 로 시작해요.") # 첫 글자 힌트
            st.write(f"다른 힌트: 암호문 `☆◎＋●`는 원래 **`면목고`** 입니다.") # 구체적인 글자 힌트 (예시)
            st.write(f"힌트: 사용된 치환 규칙 중 일부는 다음과 같아요: {st.session_state.room1_key_map}")


    user_input = st.text_input("해독된 문장을 입력하세요:", key="room1_answer")

    if st.button("정답 확인", key="check_room1_answer"):
        if user_input.strip() == st.session_state.room1_original_message:
            st.success("✅ 정답입니다! 다음 방으로 가는 문이 열렸습니다.")
            st.session_state.puzzle_solved[1] = True
            st.session_state.current_room = 2
            st.experimental_rerun()
        else:
            st.error("❌ 틀렸습니다. 다시 시도해보세요.")

# --- 2번 방 퍼즐 ---
def room2_puzzle():
    st.subheader("두 번째 방: 밀려난 메시지 (시저 암호)")
    st.write("오래된 도서관의 책장 사이에서 낡은 종이를 발견했습니다. 글자들이 밀려난 것 같네요.")

    st.markdown(f"**암호문**: `{st.session_state.room2_encrypted_message}`")

    st.info("""
    **단서:**
    - 책장 사이에서 발견된 쪽지: "나는 원래 A였는데 E가 되었어. 잊지 마."
    - 오래된 지구본 옆에 작은 숫자 '7'이 적혀 있습니다. (이동 값 힌트)
    """)

    with st.expander("더 많은 힌트 보기 (점수 감점!)"):
        if st.button("힌트 사용", key="hint2_button"):
            st.session_state.score = max(0, st.session_state.score - HINT_PENALTY_SCORE)
            st.session_state.show_hint[2] = True
            st.experimental_rerun()
        if st.session_state.show_hint[2]:
            st.write(f"힌트: 시저 암호의 이동 값은 **`{st.session_state.room2_shift}`** 입니다.")
            st.write(f"힌트: 원래 문장의 첫 글자는 **`{st.session_state.room2_original_message[0]}`** 입니다.")

    user_shift = st.number_input("이동 값을 입력하세요:", min_value=1, max_value=50, value=0, key="room2_shift_input")
    user_answer = st.text_input("해독된 문장을 입력하세요:", key="room2_answer")

    if st.button("정답 확인", key="check_room2_answer"):
        if user_shift == st.session_state.room2_shift and \
           user_answer.strip() == st.session_state.room2_original_message:
            st.success("✅ 정답입니다! 마지막 방으로 가는 통로가 열렸습니다.")
            st.session_state.puzzle_solved[2] = True
            st.session_state.current_room = 3
            st.experimental_rerun()
        else:
            st.error("❌ 이동 값이 틀렸거나 해독된 문장이 틀렸습니다. 다시 시도해보세요.")

# --- 3번 방 퍼즐 ---
def room3_puzzle():
    st.subheader("세 번째 방: 최후의 숫자 (RSA 소인수분해)")
    st.write("어둡고 텅 빈 공간, 중앙에 알 수 없는 기계 장치와 숫자 패드만이 빛납니다. 탈출구로 보이는 문은 견고하게 잠겨 있습니다.")
    st.write("이 문을 열려면 두 개의 비밀 소수(Prime Number)를 찾아야 합니다. 다음 큰 숫자는 두 소수의 곱으로 이루어져 있습니다.")
    
    st.markdown(f"**주어진 큰 숫자 N**: `{st.session_state.room3_n}`")
    st.write(f"이 숫자를 소인수분해하여 두 소수 P와 Q를 찾아 입력하세요. (단, P와 Q는 1이 아닌 숫자여야 합니다)")

    st.info("""
    **단서:**
    - 소수는 1과 자기 자신으로만 나누어지는 1보다 큰 자연수입니다.
    - 두 소수 중 하나는 10보다 크고 20보다 작습니다. (난이도 조절용 힌트)
    """)

    with st.expander("더 많은 힌트 보기 (점수 감점!)"):
        if st.button("힌트 사용", key="hint3_button"):
            st.session_state.score = max(0, st.session_state.score - HINT_PENALTY_SCORE)
            st.session_state.show_hint[3] = True
            st.experimental_rerun()
        if st.session_state.show_hint[3]:
            st.write(f"힌트: 첫 번째 소수 P는 `{st.session_state.room3_p}` 입니다.")
            st.write(f"힌트: 최종 메시지는 **`{st.session_state.room3_original_message}`** 입니다.")


    user_p = st.number_input("첫 번째 소수 (P)를 입력하세요:", min_value=1, value=0, key="room3_p_input")
    user_q = st.number_input("두 번째 소수 (Q)를 입력하세요:", min_value=1, value=0, key="room3_q_input")

    if st.button("정답 확인", key="check_room3_answer"):
        # P와 Q가 소수인지 간단히 검사
        def is_prime(num):
            if num < 2: return False
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0: return False
            return True

        if is_prime(user_p) and is_prime(user_q) and user_p * user_q == st.session_state.room3_n:
            st.success("✅ 정답입니다! 문이 열리며 탈출 성공!")
            st.write(f"최종 메시지: **{st.session_state.room3_original_message}**")
            st.session_state.puzzle_solved[3] = True
            st.session_state.current_room = 4 # 게임 종료 상태로 전환
            st.experimental_rerun()
        else:
            st.error("❌ P와 Q가 소수가 아니거나, 곱이 N과 다릅니다. 다시 시도해보세요.")

# --- 앱 실행 ---
if __name__ == "__main__":
    run_game()
