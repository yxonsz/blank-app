import streamlit as st
import random
import re

# --- 앱 구성 설정 ---
st.set_page_config(
    page_title="감성 플레이리스트",
    page_icon="🎧",
    layout="wide",
)

# --- 데이터베이스 ---
# 인간의 복합적인 감정을 고려하여 카테고리를 대폭 확장하고, 각 감정에 맞는 노래 목록을 구성합니다.
music_database = {
    # 긍정적 & 높은 에너지
    "환희": {
        "EDM": [
            {"artist": "Avicii", "song": "Levels"},
            {"artist": "Coldplay", "song": "A Sky Full Of Stars"},
            {"artist": "Alan Walker", "song": "Faded"},
        ],
        "댄스 팝": [
            {"artist": "방탄소년단", "song": "Permission to Dance"},
            {"artist": "Lady Gaga", "song": "Just Dance"},
            {"artist": "Pharrell Williams", "song": "Happy"},
        ],
    },
    "열정": {
        "록": [
            {"artist": "Queen", "song": "We Will Rock You"},
            {"artist": "Imagine Dragons", "song": "Believer"},
            {"artist": "국카스텐", "song": "Lazenca, Save Us"},
        ],
        "힙합": [
            {"artist": "Eminem", "song": "Lose Yourself"},
            {"artist": "Jessi", "song": "눈누난나 (NUNU NANA)"},
            {"artist": "Drake", "song": "God's Plan"},
        ],
    },
    # 긍정적 & 낮은 에너지
    "평온": {
        "재즈": [
            {"artist": "Bill Evans", "song": "Waltz for Debby"},
            {"artist": "Norah Jones", "song": "Don't Know Why"},
            {"artist": "Chet Baker", "song": "My Funny Valentine"},
        ],
        "어쿠스틱": [
            {"artist": "제이슨 므라즈", "song": "I'm Yours"},
            {"artist": "아이유", "song": "밤편지"},
            {"artist": "Ed Sheeran", "song": "Perfect"},
        ],
        "클래식": [
            {"artist": "드뷔시", "song": "달빛 (Clair de Lune)"},
            {"artist": "사티", "song": "짐노페디 1번"},
            {"artist": "바흐", "song": "무반주 첼로 모음곡 1번"},
        ],
    },
    "설렘": {
        "인디 팝": [
            {"artist": "볼빨간사춘기", "song": "썸 탈꺼야"},
            {"artist": "CHEEZE", "song": "Madeleine Love"},
            {"artist": "숀(SHAUN)", "song": "Way Back Home"},
        ],
        "R&B": [
            {"artist": "Ariana Grande", "song": "Daydreamin'"},
            {"artist": "Crush", "song": "잊어버리지마"},
            {"artist": "폴킴", "song": "모든 날, 모든 순간"},
        ],
    },
    # 부정적 & 낮은 에너지
    "우울": {
        "발라드": [
            {"artist": "박효신", "song": "야생화"},
            {"artist": "Adele", "song": "Someone Like You"},
            {"artist": "임창정", "song": "소주 한 잔"},
        ],
        "포크": [
            {"artist": "김광석", "song": "서른 즈음에"},
            {"artist": "Bob Dylan", "song": "Blowin' in the Wind"},
            {"artist": "Damien Rice", "song": "The Blower's Daughter"},
        ],
    },
    "쓸쓸함": {
        "모던 록": [
            {"artist": "Radiohead", "song": "Creep"},
            {"artist": "넬", "song": "기억을 걷는 시간"},
            {"artist": "Coldplay", "song": "The Scientist"},
        ],
        "OST": [
            {"artist": "Lasse Lindh", "song": "C'mon Through"},
            {"artist": "김필", "song": "그때 그 아인"},
            {"artist": "Hoppipolla", "song": "About Time"},
        ],
    },
    # 부정적 & 높은 에너지
    "분노": {
        "메탈": [
            {"artist": "Metallica", "song": "Enter Sandman"},
            {"artist": "Rage Against The Machine", "song": "Killing In The Name"},
            {"artist": "System Of A Down", "song": "B.Y.O.B."},
        ],
        "하드코어 힙합": [
            {"artist": "DMX", "song": "X Gon' Give It To Ya"},
            {"artist": "켄드릭 라마", "song": "DNA."},
            {"artist": "에픽하이", "song": "Born Hater"},
        ],
    },
    # 복합적 감정
    "그리움": {
        "포크 록": [
            {"artist": "산울림", "song": "회상"},
            {"artist": "이문세", "song": "옛사랑"},
            {"artist": "Fleetwood Mac", "song": "Landslide"},
        ],
        "시티 팝": [
            {"artist": "유키카", "song": "서울여자"},
            {"artist": "Mariya Takeuchi", "song": "Plastic Love"},
            {"artist": "김현철", "song": "오랜만에"},
        ],
    },
}

# --- 감정 분석 로직 ---
# 주관식 입력을 위한 감정 키워드 딕셔너리
# 외부 NLP 라이브러리 없이, 핵심 키워드 매칭 방식으로 감정을 추론합니다.
emotion_keywords = {
    "환희": ["최고야", "미쳤다", "환상적", "짜릿해", "날아갈", "끝내주는"],
    "열정": ["할 수 있어", "뜨거워", "불타오르네", "도전", "열정", "가자"],
    "평온": ["차분", "평화", "나른", "잔잔", "고요", "휴식", "릴랙스"],
    "설렘": ["설레", "두근", "심장이", "기대돼", "썸", "첫사랑"],
    "우울": ["우울", "슬퍼", "눈물", "힘들", "지쳤어", "혼자"],
    "쓸쓸함": ["외로워", "쓸쓸", "공허", "혼자", "텅 빈", "보고싶다"],
    "분노": ["화나", "열받네", "짜증", "분노", "다 부숴", "용서 못해"],
    "그리움": ["그리워", "옛날", "추억", "생각나", "돌아가고파", "그때"],
}

def analyze_text_mood(text):
    """
    입력된 텍스트에서 감정 키워드를 분석하여 가장 적합한 감정을 반환합니다.
    """
    scores = {mood: 0 for mood in emotion_keywords}
    
    # 텍스트에서 특수문자를 제거하고 소문자로 변환하여 분석 정확도를 높입니다.
    cleaned_text = re.sub(r'[^\w\s]', '', text).lower()

    for mood, keywords in emotion_keywords.items():
        for keyword in keywords:
            if keyword in cleaned_text:
                scores[mood] += 1
    
    # 가장 높은 점수를 받은 감정을 반환합니다. 동점일 경우 첫 번째 감정을 반환합니다.
    if any(score > 0 for score in scores.values()):
        detected_mood = max(scores, key=scores.get)
        return detected_mood
    
    return None

# --- 앱 UI ---
st.title("🎧 감성 플레이리스트")
st.write("당신의 지금 감정을 들려주세요. 꼭 맞는 노래를 추천해 드릴게요.")

# --- 입력 방식 선택 ---
input_method = st.radio(
    "어떻게 감정을 알려주시겠어요?",
    ("감정 목록에서 선택하기", "자유롭게 문장으로 표현하기"),
    horizontal=True,
    label_visibility="collapsed"
)

user_mood = ""
mood_detected = False

st.divider()

# 객관식 입력
if input_method == "감정 목록에서 선택하기":
    st.subheader("지금 당신의 감정과 가장 가까운 것을 골라보세요.")
    mood_options = list(music_database.keys())
    
    # 감정을 4개씩 묶어 버튼으로 표시
    cols = st.columns(4)
    for i, mood in enumerate(mood_options):
        if cols[i % 4].button(mood, use_container_width=True):
            user_mood = mood
            mood_detected = True

# 주관식 입력
else:
    st.subheader("오늘 하루, 어떤 감정들을 느끼셨나요?")
    text_input = st.text_area(
        "자유롭게 당신의 이야기를 들려주세요. 길게 쓸수록 더 정확해져요.",
        placeholder="예: 오늘따라 옛날 생각이 나면서 그 사람이 그립네..."
    )

    if st.button("내 감정에 맞는 노래 찾기", type="primary"):
        if text_input:
            detected_mood = analyze_text_mood(text_input)
            if detected_mood:
                user_mood = detected_mood
                mood_detected = True
                st.info(f"입력하신 문장에서 '{user_mood}'의 감정이 느껴지네요!")
            else:
                st.warning("감정을 파악하기 어려워요. 좀 더 자세하게 설명해주시겠어요?")
        else:
            st.error("먼저 오늘의 감정을 입력해주세요!")


# --- 노래 추천 로직 ---
if mood_detected:
    st.header(f"'{user_mood}'을(를) 위한 오늘의 추천 플레이리스트", divider="rainbow")

    genres = list(music_database[user_mood].keys())
    
    # 추천곡을 보기 좋게 카드 형태로 표시
    for genre in genres:
        with st.container(border=True):
            st.subheader(f"🎵 {genre}")
            
            songs_in_genre = music_database[user_mood][genre]
            num_to_recommend = min(len(songs_in_genre), 3) # 최대 3곡 추천
            recommended_songs = random.sample(songs_in_genre, num_to_recommend)
            
            for song in recommended_songs:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**{song['song']}** - _{song['artist']}_")
                with col2:
                    # 검색어를 더 정확하게 만들어 유튜브 링크 제공
                    query = f"{song['artist']} {song['song']}"
                    st.link_button("들어보기", f"https://www.youtube.com/results?search_query={query}", use_container_width=True)
            
            st.markdown("---")