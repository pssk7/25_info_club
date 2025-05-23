import streamlit as st

# --- MBTI Questions ---
# Each question is a dictionary with 'question' and 'choices'
# The choices' values determine the score for each MBTI dimension
questions = [
    {
        "question": "After a long week, how do you prefer to recharge?",
        "choices": {
            "Spending time with a large group of friends, going out to a party.": "E",
            "Having a quiet evening at home, perhaps reading or watching a movie.": "I",
        },
    },
    {
        "question": "When working on a project, are you more inclined to focus on:",
        "choices": {
            "The practical realities and details, ensuring everything is concrete.": "S",
            "The big picture, possibilities, and theoretical concepts.": "N",
        },
    },
    {
        "question": "When making a decision, what typically guides you?",
        "choices": {
            "Logical analysis and objective facts.": "T",
            "Personal values and the impact on others.": "F",
        },
    },
    {
        "question": "Do you prefer to:",
        "choices": {
            "Have things decided and planned in advance, sticking to the schedule.": "J",
            "Keep your options open and be spontaneous, adapting as you go.": "P",
        },
    },
    {
        "question": "At a social gathering, you are more likely to:",
        "choices": {
            "Initiate conversations and meet new people.": "E",
            "Observe the interactions and talk to people you already know.": "I",
        },
    },
    {
        "question": "When learning something new, do you prefer:",
        "choices": {
            "To follow instructions and learn step-by-step.": "S",
            "To explore ideas and learn by experimenting.": "N",
        },
    },
    {
        "question": "When giving feedback to others, are you usually more:",
        "choices": {
            "Direct and honest, even if it might be hard to hear.": "T",
            "Gentle and diplomatic, focusing on preserving harmony.": "F",
        },
    },
    {
        "question": "Your workspace is typically:",
        "choices": {
            "Organized and tidy, with everything in its place.": "J",
            "A bit more relaxed and flexible, with things easily accessible.": "P",
        },
    },
]

# --- MBTI Type Descriptions (simplified for brevity) ---
mbti_types = {
    "ISTJ": "The Inspector: Practical, fact-minded individuals.",
    "ISFJ": "The Protector: Warm, considerate, and responsible guardians.",
    "INFJ": "The Advocate: Quiet and mystical, yet very inspiring and tireless idealists.",
    "INTJ": "The Architect: Imaginative and strategic thinkers, with a plan for everything.",
    "ISTP": "The Virtuoso: Bold and practical experimenters, masters of all kinds of tools.",
    "ISFP": "The Adventurer: Flexible and charming artists, always ready to explore and experience something new.",
    "INFP": "The Mediator: Poetic, kind and altruistic people, always eager to help a good cause.",
    "INTP": "The Logician: Innovative inventors with an unquenchable thirst for knowledge.",
    "ESTP": "The Entrepreneur: Smart, energetic and very perceptive people, who truly enjoy living on the edge.",
    "ESFP": "The Entertainer: Spontaneous, energetic and enthusiastic people – life is never boring around them.",
    "ENFP": "The Campaigner: Enthusiastic, creative and sociable free spirits, who can always find a reason to smile.",
    "ENTP": "The Debater: Smart and curious thinkers who cannot resist an intellectual challenge.",
    "ESTJ": "The Executive: Excellent administrators, unsurpassed at managing things – or people.",
    "ESFJ": "The Consul: Extraordinarily caring, social and popular people, always eager to help.",
    "ENFJ": "The Protagonist: Charismatic and inspiring leaders, who are able to mesmerize their listeners.",
    "ENTJ": "The Commander: Bold, imaginative and strong-willed leaders, always finding a way – or making one.",
}


def calculate_mbti(scores):
    """Calculates the MBTI type based on the accumulated scores."""
    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"
    return mbti


st.set_page_config(page_title="MBTI Explorer App", layout="centered")

st.title("Discover Your MBTI Type!")
st.markdown("Answer a few questions to find out your potential MBTI personality type.")

if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
    st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    st.session_state.quiz_complete = False

if not st.session_state.quiz_complete:
    current_q_data = questions[st.session_state.current_question_index]
    st.subheader(f"Question {st.session_state.current_question_index + 1}/{len(questions)}")
    st.write(current_q_data["question"])

    selected_choice = st.radio("Choose your answer:", list(current_q_data["choices"].keys()), key=f"q_{st.session_state.current_question_index}")

    if st.button("Next Question"):
        if selected_choice:
            # Get the MBTI dimension corresponding to the selected choice
            dimension = current_q_data["choices"][selected_choice]
            st.session_state.scores[dimension] += 1

            st.session_state.current_question_index += 1
            if st.session_state.current_question_index >= len(questions):
                st.session_state.quiz_complete = True
                st.experimental_rerun() # Rerun to show results immediately
        else:
            st.warning("Please select an answer before proceeding.")

else:
    st.subheader("Quiz Complete!")
    user_mbti = calculate_mbti(st.session_state.scores)
    st.success(f"Your calculated MBTI type is: **{user_mbti}**")

    if user_mbti in mbti_types:
        st.info(mbti_types[user_mbti])
    else:
        st.warning("Could not find a description for this MBTI type.")

    if st.button("Retake Quiz"):
        st.session_state.current_question_index = 0
        st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        st.session_state.quiz_complete = False
        st.experimental_rerun()

st.markdown("---")
st.markdown("Disclaimer: This is a simplified quiz for entertainment purposes and may not accurately reflect your true MBTI type. For a professional assessment, consult a certified practitioner.")
