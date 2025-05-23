import streamlit as st

# --- 게임 데이터 정의 ---
# 각 질문은 딕셔너리로 구성됩니다:
# 'question': 질문 내용
# 'options': 선택지 딕셔너리. {선택지 텍스트: 다음 질문 인덱스 또는 엔딩 키}
#            엔딩 키는 'ending_X' 와 같은 형식으로, 최종 엔딩을 나타냅니다.
#            여기에선 선택지마다 다음 질문의 번호 (0, 1, 2, 3)를 지정하거나,
#            엔딩으로 바로 이동하는 경우 'ending_XYZ'와 같은 고유 키를 지정합니다.

# 편의상 각 질문 인덱스를 0, 1, 2, 3으로 가정하고,
# 선택지 텍스트는 간결하게 작성합니다.
# 실제 앱에서는 더 풍부한 스토리와 선택지 텍스트를 작성해주세요.

questions = [
    {
        "id": "q1",
        "story": "좀비 사태 발생! 당신은 집에서 나와 피난처를 찾아야 합니다. 주변은 아비규환입니다. 어디로 향하시겠습니까?",
        "options": {
            "A. 사람들이 모여있던 대형 마트로 향한다. (물자 확보)": "q2_path_A",
            "B. 조용하고 외진 숲길로 숨어든다. (은신)": "q2_path_B",
            "C. 경찰서로 향한다. (정보 및 안전 확보)": "q2_path_C",
        },
    },
    {
        "id": "q2_path_A", # Q1에서 A를 선택했을 때의 Q2
        "story": "대형 마트는 이미 아수라장입니다. 좀비들이 들끓고, 생존자들은 약탈 중입니다. 당신은 어떻게 하시겠습니까?",
        "options": {
            "1. 재빨리 필요한 물자만 챙겨 도망친다.": "q3_path_A1",
            "2. 다른 생존자들과 합류하여 좀비에 맞서 싸운다.": "q3_path_A2",
            "3. 몰래 숨어서 상황을 지켜본다.": "q3_path_A3",
        },
    },
    {
        "id": "q2_path_B", # Q1에서 B를 선택했을 때의 Q2
        "story": "고요한 숲길에 들어섰지만, 갑자기 좀비 무리가 나타납니다. 지형이 복잡하여 도망치기 쉽지 않습니다. 당신의 선택은?",
        "options": {
            "1. 근처 나무 위로 올라가 숨는다.": "q3_path_B1",
            "2. 흩어져 있는 좀비들을 피해 샛길로 도망친다.": "q3_path_B2",
            "3. 가지고 있던 둔기로 맞서 싸운다.": "q3_path_B3",
        },
    },
    {
        "id": "q2_path_C", # Q1에서 C를 선택했을 때의 Q2
        "story": "경찰서는 이미 점령당했거나, 내부가 위험해 보입니다. 좀비의 울음소리가 들립니다. 당신은 어떻게 하시겠습니까?",
        "options": {
            "1. 다른 안전한 장소를 찾아 즉시 발길을 돌린다.": "q3_path_C1",
            "2. 조심스럽게 경찰서 내부로 진입해 본다.": "q3_path_C2",
            "3. 근처 차량을 찾아 타고 도주를 시도한다.": "q3_path_C3",
        },
    },
    # Q3 질문들 (선택지가 3개씩, 총 9개)
    # 각 질문의 ID는 이전 질문의 선택지에 따라 달라집니다. (예: q3_path_A1)
    # 여기서는 예시를 위해 몇 가지만 작성하고, 모든 81가지 엔딩을 만들기 위해 필요한
    # 27개의 Q3와 81개의 Q4를 모두 작성하려면 코드가 매우 길어집니다.
    # 하지만 로직은 동일하게 확장하면 됩니다.
    {
        "id": "q3_path_A1", # Q2_A에서 1을 선택했을 때의 Q3
        "story": "물자를 챙겨 도망치던 중, 좀비에게 둘러싸인 생존자를 발견했습니다. 어떻게 하시겠습니까?",
        "options": {
            "1. 모른 척 지나간다.": "q4_path_A1_1",
            "2. 구출을 시도한다.": "q4_path_A1_2",
            "3. 상황을 살피며 기회를 노린다.": "q4_path_A1_3",
        },
    },
    {
        "id": "q3_path_A2", # Q2_A에서 2를 선택했을 때의 Q3
        "story": "생존자들과 함께 싸우는 중, 무기가 부러졌습니다. 주변에 쓸만한 것이 있나요?",
        "options": {
            "1. 맨손으로 싸운다.": "q4_path_A2_1",
            "2. 다른 생존자의 무기를 빌린다.": "q4_path_A2_2",
            "3. 주변을 뒤져 새로운 무기를 찾는다.": "q4_path_A2_3",
        },
    },
    # ... (여기에 q3_path_A3, q3_path_B1, q3_path_B2, q3_path_B3,
    #        q3_path_C1, q3_path_C2, q3_path_C3 에 해당하는 9개의 Q3 질문을 추가)

    # 마지막 Q4 질문들 (총 27개)은 엔딩으로 바로 연결됩니다.
    # 각 엔딩은 고유한 ID를 가지며, 최종 엔딩 메시지는 'endings' 딕셔너리에서 찾아옵니다.
    {
        "id": "q4_path_A1_1",
        "story": "모른 척 지나쳤지만, 뒤에서 좀비가 당신을 덮쳤습니다. 당신은...",
        "options": {
            "1.": "ending_A111", # 더 이상 선택지가 없으므로 엔딩으로 바로 연결
            "2.": "ending_A112",
            "3.": "ending_A113",
        },
    },
    # ... (여기에 모든 27개의 Q4 질문을 추가하고 각 선택지를 엔딩으로 연결)
]

# --- 엔딩 정의 ---
# 81가지 엔딩을 모두 정의해야 합니다.
# 각 키는 질문의 마지막 선택지 ID와 연결됩니다.
endings = {
    "ending_A111": "결국 좀비에게 잡혀 최후를 맞이했습니다. 조금 더 이기적이었어야 했을까요?",
    "ending_A112": "생존자를 구하려다 함께 위험에 처했지만, 극적으로 탈출했습니다. 당신의 용기가 빛났습니다!",
    "ending_A113": "상황을 살피다 기회를 놓쳐 위험에 처했습니다. 신중함이 때로는 독이 될 수도 있습니다.",
    # ... (여기에 81가지 모든 엔딩을 정의)
    "ending_default": "당신의 여정은 끝났습니다. 당신의 선택이 어떤 결과를 가져왔는지 확인해보세요!" # 모든 경로를 다 만들지 못했을 경우 대비
}

# --- 게임 상태 초기화 함수 ---
def initialize_game():
    st.session_state.current_question_id = "q1" # 첫 질문 ID
    st.session_state.player_choices = [] # 플레이어 선택 기록
    st.session_state.game_started = False
    st.session_state.game_over = False

# --- Streamlit 앱 시작 ---
st.set_page_config(page_title="좀비 서바이벌 스토리 게임", layout="centered")

st.title("🧟‍♂️ 좀비 서바이벌: 마지막 선택 🧟‍♀️")
st.markdown("---")

if 'game_started' not in st.session_state:
    initialize_game()

# 게임 시작 화면
if not st.session_state.game_started:
    st.image("https://images.unsplash.com/photo-1549495000-848e02c6d4c0?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="좀비 아포칼립스에 오신 것을 환영합니다...", use_column_width=True)
    st.write("당신은 좀비로 가득 찬 세상에서 살아남아야 합니다. 당신의 선택 하나하나가 생사를 가릅니다.")
    if st.button("게임 시작"):
        st.session_state.game_started = True
        st.experimental_rerun() # 상태 변경 후 새로고침

# 게임 진행
elif st.session_state.game_started and not st.session_state.game_over:
    current_q_id = st.session_state.current_question_id

    # 현재 질문 데이터 찾기
    current_question_data = next((q for q in questions if q["id"] == current_q_id), None)

    if current_question_data:
        st.subheader(current_question_data["story"])
        st.markdown("---")

        options_keys = list(current_question_data["options"].keys())
        selected_option = st.radio("당신의 선택은?", options_keys, key=current_q_id)

        if st.button("선택 완료"):
            if selected_option:
                next_path = current_question_data["options"][selected_option]
                st.session_state.player_choices.append(selected_option) # 선택 기록

                if next_path.startswith("ending_"):
                    st.session_state.final_ending_key = next_path
                    st.session_state.game_over = True
                else:
                    st.session_state.current_question_id = next_path
                st.experimental_rerun()
            else:
                st.warning("선택지를 골라주세요.")
    else:
        # 질문 ID를 찾지 못했을 경우 (오류 또는 마지막 질문에 도달하지 못한 경우)
        st.error("스토리 오류가 발생했습니다. 다시 시작해주세요.")
        st.session_state.game_over = True
        st.session_state.final_ending_key = "ending_default"
        st.experimental_rerun()

# 게임 종료 화면
elif st.session_state.game_over:
    st.subheader("게임 종료!")
    final_message = endings.get(st.session_state.final_ending_key, endings["ending_default"])
    st.success(f"**결과:** {final_message}")

    st.write("---")
    st.write("당신의 선택:")
    for i, choice in enumerate(st.session_state.player_choices):
        st.write(f"질문 {i+1}: {choice}")

    if st.button("다시 플레이"):
        initialize_game()
        st.experimental_rerun()

st.markdown("---")
st.caption("이 게임은 단순한 예시이며, 모든 경우의 수를 포함하지 않습니다. 더 많은 질문과 엔딩을 추가하여 스토리를 풍부하게 만들어보세요!")
