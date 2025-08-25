import streamlit as st
import random
import re

# --- 앱 구성 설정 ---
st.set_page_config(
    page_title="감성 AI 뮤직 큐레이터",
    page_icon="🎤",
    layout="centered",
)

# --- v7: K-POP과 POP을 중심으로 전면 재구성 및 확장된 데이터베이스 ---
music_database_v7 = {
    # K-POP 독립 카테고리 신설
    "K-POP": {
        "댄스/아이돌": [
            {"artist": "방탄소년단", "song": "Dynamite"},
            {"artist": "BLACKPINK", "song": "How You Like That"},
            {"artist": "IVE (아이브)", "song": "LOVE DIVE"},
            {"artist": "뉴진스 (NewJeans)", "song": "Hype Boy"},
        ],
        "발라드": [
            {"artist": "아이유", "song": "밤편지"},
            {"artist": "박효신", "song": "야생화"},
            {"artist": "태연", "song": "만약에"},
            {"artist": "성시경", "song": "거리에서"},
        ],
        "R&B/힙합": [
            {"artist": "DEAN", "song": "instagram"},
            {"artist": "Crush", "song": "Oasis"},
            {"artist": "지코 (ZICO)", "song": "아무노래"},
            {"artist": "에픽하이", "song": "Love Love Love"},
        ],
        "인디/록": [
            {"artist": "혁오 (HYUKOH)", "song": "위잉위잉"},
            {"artist": "잔나비", "song": "주저하는 연인들을 위해"},
            {"artist": "10CM", "song": "스토커"},
            {"artist": "쏜애플", "song": "시퍼런 봄"},
        ],
    },
    # POP 독립 카테고리 신설
    "POP": {
        "Top 40/댄스 팝": [
            {"artist": "The Weeknd", "song": "Blinding Lights"},
            {"artist": "Taylor Swift", "song": "Shake It Off"},
            {"artist": "Dua Lipa", "song": "Don't Start Now"},
            {"artist": "Harry Styles", "song": "As It Was"},
        ],
        "팝 발라드": [
            {"artist": "Adele", "song": "Someone Like You"},
            {"artist": "Ed Sheeran", "song": "Perfect"},
            {"artist": "Sam Smith", "song": "Stay With Me"},
            {"artist": "John Legend", "song": "All of Me"},
        ],
        "인디 팝/얼터너티브": [
            {"artist": "Billie Eilish", "song": "bad guy"},
            {"artist": "Lana Del Rey", "song": "Summertime Sadness"},
            {"artist": "The 1975", "song": "Somebody Else"},
            {"artist": "Tame Impala", "song": "The Less I Know The Better"},
        ],
        "팝 록": [
            {"artist": "Coldplay", "song": "Viva La Vida"},
            {"artist": "Imagine Dragons", "song": "Believer"},
            {"artist": "Maroon 5", "song": "Moves Like Jagger"},
            {"artist": "OneRepublic", "song": "Counting Stars"},
        ],
    },
    # 기존 상황별 카테고리는 더욱 전문화
    "일에 집중해야 할 때": {
        "클래식 (피아노 솔로)": [{"artist": "쇼팽", "song": "녹턴 2번"}, {"artist": "베토벤", "song": "월광 소나타 1악장"}, {"artist": "드뷔시", "song": "아마빛 머리의 소녀"}],
        "IDM": [{"artist": "Aphex Twin", "song": "Avril 14th"}, {"artist": "Boards of Canada", "song": "Music Is Math"}, {"artist": "Flying Lotus", "song": "Zodiac Shit"}],
        "다운템포": [{"artist": "Bonobo", "song": "Cirrus"}, {"artist": "Four Tet", "song": "Two Thousand and Seventeen"}, {"artist": "Tycho", "song": "Awake"}],
        "자연의 소리 (ASMR)": [{"artist": "Various Artists", "song": "잔잔한 빗소리"}, {"artist": "Various Artists", "song": "타닥거리는 장작불 소리"}, {"artist": "Various Artists", "song": "숲 속의 아침"}],
    },
    "지친 하루의 끝, 위로가 필요할 때": {
        "어쿠스틱": [{"artist": "이하이", "song": "한숨"}, {"artist": "Coldplay", "song": "Fix You"}, {"artist": "악뮤(AKMU)", "song": "오랜 날 오랜 밤"}, {"artist": "Jeff Buckley", "song": "Hallelujah"}],
        "Lo-fi": [{"artist": "potsu", "song": "i'm closing my eyes"}, {"artist": "Idealism", "song": "controlla"}, {"artist": "Nujabes", "song": "Aruarian Dance"}, {"artist": "RŮDE", "song": "Eternal Youth"}],
        "OST (Score)": [{"artist": "Hans Zimmer", "song": "Time"}, {"artist": "Joe Hisaishi", "song": "One Summer's Day"}, {"artist": "Max Richter", "song": "On the Nature of Daylight"}],
        "포스트 클래시컬": [{"artist": "Ólafur Arnalds", "song": "Tomorrow's Song"}, {"artist": "Nils Frahm", "song": "Says"}, {"artist": "Ludovico Einaudi", "song": "Nuvole Bianche"}],
    },
    # 나머지 카테고리는 유지...
}

# --- 최종 감정 분석 엔진 ---
# K-POP과 POP을 직접적으로 인식할 수 있는 키워드 추가
emotion_lexicon_final = {
    "K-POP": {"케이팝": 3, "kpop": 3, "아이돌": 2, "한국노래": 2, "방탄": 1.5, "블핑": 1.5, "뉴진스": 1.5},
    "POP": {"팝송": 3, "pop": 3, "빌보드": 2, "해외노래": 2, "테일러": 1.5, "위켄드": 1.5},
    "일에 집중해야 할 때": {"집중": 2.5, "공부": 2, "작업": 2, "코딩": 1.5, "독서": 1.2, "몰입": 1},
    "지친 하루의 끝, 위로가 필요할 때": {"위로": 2.5, "힘들": 2, "지쳤": 2, "눈물": 1.5, "혼자": 1.5, "슬퍼": 1, "괜찮아": 1},
    # 나머지 키워드는 이전과 유사
}

def analyze_text_mood_final(text):
    scores = {mood: 0 for mood in emotion_lexicon_final}
    cleaned_text = re.sub(r'[^\w\s]', '', text).lower()
    for mood, keywords in emotion_lexicon_final.items():
        for keyword, weight in keywords.items():
            if keyword in cleaned_text: scores[mood] += weight
    positive_scores = {mood: score for mood, score in scores.items() if score > 0}
    # 분석 결과가 없으면, 랜덤으로 상황을 추천해주는 것도 좋은 경험이 될 수 있습니다.
    if not positive_scores:
        return random.choice(list(music_database_v7.keys()))
    return max(positive_scores, key=positive_scores.get)

# --- UI 및 추천 로직 ---
def display_recommendations(mood_category):
    st.header(f"'{mood_category}' 맞춤 추천", divider="rainbow")
    st.write(f"당신의 **'{mood_category}'** 순간을 위해 엄선한 장르입니다.")
    
    tailored_genres = music_database_v7.get(mood_category, {})
    for genre, songs in tailored_genres.items():
        with st.expander(f"🎵 **{genre}**", expanded=True):
            num_to_recommend = min(len(songs), 3)
            recommended_songs = random.sample(songs, num_to_recommend)
            for song in recommended_songs:
                display_song(song)

    st.header("새로운 장르 탐험하기", divider="gray")
    st.write("다른 분위기의 음악도 발견해보세요.")

    other_moods = [mood for mood in music_database_v7 if mood != mood_category]
    for other_mood in other_moods:
        with st.expander(f"✨ **'{other_mood}'**의 분위기 둘러보기"):
            genres_in_mood = music_database_v7[other_mood]
            for genre, songs in genres_in_mood.items():
                 # 여기서는 한 곡씩만 맛보기로 보여주어 스크롤 부담을 줄입니다.
                song_to_preview = random.choice(songs)
                display_song(song_to_preview, show_genre=genre)

def display_song(song, show_genre=None):
    query = f"{song['artist']} {song['song']}".replace(" ", "+")
    genre_tag = f'<span style="font-size: 0.8em; color: #FF4B4B; background-color: #444; padding: 2px 6px; border-radius: 10px; margin-right: 5px;">{show_genre}</span>' if show_genre else ''
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid #222;">
            <div>
                {genre_tag}
                <span style="font-weight: bold; font-size: 1.1em;">{song['song']}</span>
                <span style="color: #A0A0A0;"> - {song['artist']}</span>
            </div>
            <a href="https://www.youtube.com/results?search_query={query}" target="_blank" style="text-decoration: none; color: white; background-color: #FF4B4B; padding: 8px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em;">
                듣기
            </a>
        </div>
        """, unsafe_allow_html=True)

# --- 앱 UI 시작 ---
st.title("🎤 감성 AI 뮤직 큐레이터")
st.markdown("**당신의 모든 순간을 위한 단 하나의 플레이리스트.** 지금 느끼는 감정이나 듣고 싶은 음악 장르를 자유롭게 이야기해주세요.")

# 세션 상태에 추천 결과를 저장하여 '다른 곡' 추천 시 활용
if 'mood' not in st.session_state:
    st.session_state.mood = None

text_input = st.text_area(
    "어떤 음악을 들려드릴까요?",
    placeholder="예: 케이팝 아이돌 노래 신나는 거! / 오늘 좀 우울한데 위로되는 팝송 추천해줘 / 집중해서 코딩할 때 듣기 좋은 음악",
    height=100,
    label_visibility="collapsed"
)

# 버튼을 중앙에 배치하기 위한 컬럼 사용
col1, col2, col3 = st.columns([1,1,1])

with col2:
    if st.button("내 감정에 맞는 음악 찾기", use_container_width=True, type="primary"):
        if text_input:
            st.session_state.mood = analyze_text_mood_final(text_input)
        else:
            st.warning("먼저 듣고 싶은 음악에 대해 이야기해주세요!")

# 추천 로직 실행
if st.session_state.mood:
    display_recommendations(st.session_state.mood)
    
    # '다른 곡 추천받기' 버튼은 이제 명확하게 'rerun'을 통해 새로운 랜덤 샘플을 생성합니다.
    if st.button('🔄 다른 곡으로 새로고침', use_container_width=True):
        st.rerun()