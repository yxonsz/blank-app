import streamlit as st
import random
import re

# --- 앱 구성 설정 ---
st.set_page_config(
    page_title="뮤직 큐레이터",
    page_icon="🎼",
    layout="centered",
)

# --- 확장된 음악 데이터베이스 ---
# 사용자의 다양한 취향과 세밀한 감정선을 만족시키기 위해
# 카테고리를 '상황/분위기' 중심으로 재편하고, 장르와 곡 목록을 대폭 확장했습니다.
music_database_v4 = {
    "위로가 필요한 날": {
        "어쿠스틱 팝": [
            {"artist": "이하이", "song": "한숨"},
            {"artist": "Coldplay", "song": "Fix You"},
            {"artist": "Billie Eilish", "song": "everything i wanted"},
            {"artist": "악뮤(AKMU)", "song": "오랜 날 오랜 밤"},
        ],
        "Lo-fi": [
            {"artist": "potsu", "song": "i'm closing my eyes"},
            {"artist": "Idealism", "song": "controlla"},
            {"artist": "Nujabes", "song": "Aruarian Dance"},
            {"artist": "RŮDE", "song": "Eternal Youth"},
        ],
        "앰비언트": [
            {"artist": "Brian Eno", "song": "Music for Airports 1/1"},
            {"artist": "Aphex Twin", "song": "#3"},
            {"artist": "류이치 사카모토", "song": "Merry Christmas Mr. Lawrence"},
        ],
    },
    "자신감이 넘치는 순간": {
        "팝 록": [
            {"artist": "Queen", "song": "We Are The Champions"},
            {"artist": "Katy Perry", "song": "Roar"},
            {"artist": "Bon Jovi", "song": "It's My Life"},
            {"artist": "Fall Out Boy", "song": "Centuries"},
        ],
        "힙합": [
            {"artist": "Kendrick Lamar", "song": "HUMBLE."},
            {"artist": "이영지", "song": "FIGHTING (Feat. 이영지)"},
            {"artist": "Jay-Z", "song": "Empire State Of Mind (Feat. Alicia Keys)"},
            {"artist": "Cardi B", "song": "Bodak Yellow"},
        ],
    },
    "비 오는 창 밖을 보며": {
        "재즈": [
            {"artist": "Chet Baker", "song": "But Not For Me"},
            {"artist": "Billie Holiday", "song": "Gloomy Sunday"},
            {"artist": "Miles Davis", "song": "Blue in Green"},
            {"artist": "선우정아", "song": "비 온다"},
        ],
        "네오 소울": [
            {"artist": "D'Angelo", "song": "Brown Sugar"},
            {"artist": "Erykah Badu", "song": "On & On"},
            {"artist": "Maxwell", "song": "Ascension (Don't Ever Wonder)"},
            {"artist": "크러쉬", "song": "가끔"},
        ],
    },
    "밤 드라이브의 설렘": {
        "시티 팝": [
            {"artist": "Mariya Takeuchi", "song": "Plastic Love"},
            {"artist": "김현철", "song": "드라이브"},
            {"artist": "유키카", "song": "서울여자"},
            {"artist": "Anri", "song": "Last Summer Whisper"},
        ],
        "신스웨이브": [
            {"artist": "Kavinsky", "song": "Nightcall"},
            {"artist": "The Midnight", "song": "Sunset"},
            {"artist": "Lorn", "song": "Acid Rain"},
        ],
    },
    "몽환적인 새벽 감성": {
        "드림 팝": [
            {"artist": "Cigarettes After Sex", "song": "Apocalypse"},
            {"artist": "Beach House", "song": "Space Song"},
            {"artist": "Lana Del Rey", "song": "Video Games"},
            {"artist": "The xx", "song": "Intro"},
        ],
        "포스트 록": [
            {"artist": "Explosions in the Sky", "song": "Your Hand in Mine"},
            {"artist": "Sigur Rós", "song": "Svefn-g-englar"},
            {"artist": "Mogwai", "song": "Auto Rock"},
        ],
    },
}


# --- v3: 고도화된 감정 분석 엔진 ---
# '상황/분위기'에 대한 키워드와 가중치를 대폭 보강하여 문장 인식률을 높였습니다.
emotion_lexicon_v3 = {
    "위로가 필요한 날": {"위로": 2.5, "힘들": 2, "지쳤": 2, "눈물": 1.5, "혼자": 1.5, "슬퍼": 1, "괜찮아": 1},
    "자신감이 넘치는 순간": {"자신감": 2.5, "성공": 2, "해냈어": 2, "최고": 1.5, "할수있어": 1.5, "뿌듯": 1, "극복": 1},
    "비 오는 창 밖을 보며": {"비": 2.5, "창밖": 2, "흐린": 1.5, "센치": 1.5, "빗소리": 1.2, "차분": 1},
    "밤 드라이브의 설렘": {"드라이브": 2.5, "밤공기": 2, "도로": 1.5, "네온사인": 1.5, "설레": 1, "질주": 1},
    "몽환적인 새벽 감성": {"새벽": 2.5, "꿈": 2, "몽환": 2, "고요": 1.5, "생각": 1.2, "잠 못 드는": 1},
}

def analyze_text_mood_v3(text):
    scores = {mood: 0 for mood in emotion_lexicon_v3}
    cleaned_text = re.sub(r'[^\w\s]', '', text).lower()
    
    for mood, keywords in emotion_lexicon_v3.items():
        for keyword, weight in keywords.items():
            # 문장 안에 키워드가 포함되어 있으면 가중치를 더합니다.
            if keyword in cleaned_text:
                scores[mood] += weight
    
    positive_scores = {mood: score for mood, score in scores.items() if score > 0}
    if not positive_scores:
        return None
    
    detected_mood = max(positive_scores, key=positive_scores.get)
    return detected_mood


# --- 앱 UI ---
st.title("🎼 당신의 순간을 위한 뮤직 큐레이터")
st.write("당신의 감정, 혹은 지금의 분위기를 알려주세요. 꼭 맞는 음악을 선별해 드릴게요.")

tab1, tab2 = st.tabs(["**✍️ 텍스트로 내 기분 설명하기**", "**🖼️ 특정 상황/분위기 선택하기**"])

final_mood = None

with tab1:
    st.subheader("당신의 이야기를 들려주세요")
    text_input = st.text_area(
        "어떤 하루를 보내셨나요? 지금 어떤 감정을 느끼고 있나요?",
        placeholder="예: 오늘따라 비도 오고 옛날 생각이 나서 좀 센치해지네...",
        height=150
    )
    if st.button("내 이야기에 맞는 음악 찾기", use_container_width=True, type="primary"):
        if text_input:
            mood = analyze_text_mood_v3(text_input)
            if mood:
                st.success(f"분석 결과: **'{mood}'** 와 가장 어울리는 분위기네요.")
                final_mood = mood
            else:
                st.warning("감정을 파악하기 어려워요. 조금 더 구체적인 단어를 사용해 다시 시도해보세요.")
        else:
            st.error("먼저 당신의 이야기를 들려주세요!")

with tab2:
    st.subheader("지금 어떤 순간에 계신가요?")
    mood_options = ["어떤 순간에 어울리는 음악을 찾으세요?"] + list(music_database_v4.keys())
    selected_mood = st.selectbox(
        "상황/분위기를 선택하세요",
        options=mood_options,
        index=0,
        label_visibility="collapsed"
    )
    if selected_mood != mood_options[0]:
        final_mood = selected_mood

# --- 음악 추천 섹션 ---
if final_mood:
    st.divider()
    st.header(f"🎧 '{final_mood}'을(를) 위한 추천 플레이리스트")

    genres = list(music_database_v4[final_mood].keys())
    
    for genre in genres:
        # st.expander를 사용해 깔끔한 UI 구성
        with st.expander(f"**{genre}** 장르의 추천곡", expanded=True):
            songs_in_genre = music_database_v4[final_mood][genre]
            
            # 곡이 4곡 이상이면 3곡을 랜덤 샘플링, 3곡 이하면 모두 보여줌
            num_to_recommend = min(len(songs_in_genre), 3)
            recommended_songs = random.sample(songs_in_genre, num_to_recommend)
            
            for song in recommended_songs:
                # 검색어의 정확도를 높이기 위해 아티스트와 곡명을 합쳐서 쿼리 생성
                query = f"{song['artist']} {song['song']}"
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; padding: 5px 0;">
                        <div>
                            <span style="font-weight: bold; font-size: 1.1em;">{song['song']}</span>
                            <br>
                            <span style="color: #A0A0A0;">{song['artist']}</span>
                        </div>
                        <a href="https://www.youtube.com/results?search_query={query.replace(" ", "+")}" target="_blank" 
                           style="text-decoration: none; color: white; background-color: #E63946; padding: 8px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em;">
                            YouTube
                        </a>
                    </div>
                    """, unsafe_allow_html=True
                )
    
    # 새로운 추천을 위한 리프레시 버튼
    if st.button('🔄 다른 곡 추천받기', use_container_width=True):
        st.rerun()