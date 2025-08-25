import streamlit as st
import random
import re

# --- 앱 구성 설정 ---
st.set_page_config(
    page_title="나를 위한 음악",
    page_icon="🎶🎧",
    layout="wide", # 넓은 레이아웃으로 변경하여 더 많은 정보를 표시
)

# --- v5 데이터베이스 (이전과 동일) ---
music_database_v5 = {
    "지친 하루의 끝, 위로가 필요할 때": {
        "어쿠스틱 팝": [{"artist": "이하이", "song": "한숨"}, {"artist": "Coldplay", "song": "Fix You"}, {"artist": "악뮤(AKMU)", "song": "오랜 날 오랜 밤"}, {"artist": "Justin Bieber", "song": "Love Yourself"}],
        "Lo-fi Hip Hop": [{"artist": "potsu", "song": "i'm closing my eyes"}, {"artist": "Idealism", "song": "controlla"}, {"artist": "Nujabes", "song": "Aruarian Dance"}, {"artist": "RŮDE", "song": "Eternal Youth"}],
        "OST (Score)": [{"artist": "Hans Zimmer", "song": "Time"}, {"artist": "Joe Hisaishi", "song": "One Summer's Day"}, {"artist": "Max Richter", "song": "On the Nature of Daylight"}],
        "포스트 클래시컬": [{"artist": "Ólafur Arnalds", "song": "Tomorrow's Song"}, {"artist": "Nils Frahm", "song": "Says"}, {"artist": "Ludovico Einaudi", "song": "Nuvole Bianche"}],
        "슬로우코어": [{"artist": "Cigarettes After Sex", "song": "K."}, {"artist": "Lana Del Rey", "song": "Summertime Sadness"}, {"artist": "Mazzy Star", "song": "Fade Into You"}],
    },
    "세상의 중심이 된 듯, 자신감이 폭발할 때": {
        "팝 록": [{"artist": "Queen", "song": "We Are The Champions"}, {"artist": "Imagine Dragons", "song": "Believer"}, {"artist": "Fall Out Boy", "song": "Centuries"}, {"artist": "The Script", "song": "Hall of Fame"}],
        "힙합/트랩": [{"artist": "Kendrick Lamar", "song": "HUMBLE."}, {"artist": "Drake", "song": "Started From the Bottom"}, {"artist": "Travis Scott", "song": "SICKO MODE"}, {"artist": "Future", "song": "Mask Off"}],
        "펑크 (Funk)": [{"artist": "James Brown", "song": "Get Up Offa That Thing"}, {"artist": "Mark Ronson", "song": "Uptown Funk"}, {"artist": "Earth, Wind & Fire", "song": "September"}],
        "일렉트로 팝": [{"artist": "Daft Punk", "song": "One More Time"}, {"artist": "The Weeknd", "song": "Blinding Lights"}, {"artist": "Lady Gaga", "song": "Applause"}],
    },
    "창 밖에 비가 내릴 때": {
        "재즈 (보컬)": [{"artist": "Chet Baker", "song": "But Not For Me"}, {"artist": "Billie Holiday", "song": "Gloomy Sunday"}, {"artist": "Norah Jones", "song": "Don't Know Why"}, {"artist": "김필", "song": "목소리"}],
        "네오 소울": [{"artist": "D'Angelo", "song": "Brown Sugar"}, {"artist": "Erykah Badu", "song": "On & On"}, {"artist": "Maxwell", "song": "Ascension (Don't Ever Wonder)"}, {"artist": "크러쉬", "song": "가끔"}],
        "트립합 (Trip-Hop)": [{"artist": "Massive Attack", "song": "Teardrop"}, {"artist": "Portishead", "song": "Glory Box"}, {"artist": "Tricky", "song": "Overcome"}],
        "R&B 발라드": [{"artist": "DEAN", "song": "D (half moon)"}, {"artist": "백예린", "song": "우주를 건너"}, {"artist": "Frank Ocean", "song": "Thinking Bout You"}],
    },
    "설레는 밤의 드라이브": {
        "시티 팝": [{"artist": "Mariya Takeuchi", "song": "Plastic Love"}, {"artist": "김현철", "song": "드라이브"}, {"artist": "유키카", "song": "서울여자"}, {"artist": "Tatsuro Yamashita", "song": "RIDE ON TIME"}],
        "신스웨이브": [{"artist": "Kavinsky", "song": "Nightcall"}, {"artist": "The Midnight", "song": "Sunset"}, {"artist": "M83", "song": "Midnight City"}],
        "인디 록": [{"artist": "Phoenix", "song": "1901"}, {"artist": "The Strokes", "song": "Last Nite"}, {"artist": "검정치마", "song": "EVERYTHING"}],
        "프렌치 하우스": [{"artist": "Justice", "song": "D.A.N.C.E."}, {"artist": "Stardust", "song": "Music Sounds Better With You"}, {"artist": "Madeon", "song": "The City"}],
    },
    "생각이 많아지는 새벽": {
        "드림 팝": [{"artist": "Beach House", "song": "Space Song"}, {"artist": "The xx", "song": "Intro"}, {"artist": "Joji", "song": "SLOW DANCING IN THE DARK"}],
        "포스트 록": [{"artist": "Explosions in the Sky", "song": "Your Hand in Mine"}, {"artist": "Sigur Rós", "song": "Svefn-g-englar"}, {"artist": "Mogwai", "song": "Auto Rock"}],
        "슈게이징 (Shoegazing)": [{"artist": "My Bloody Valentine", "song": "Only Shallow"}, {"artist": "Slowdive", "song": "When the Sun Hits"}, {"artist": "Ride", "song": "Vapour Trail"}],
        "미니멀리즘": [{"artist": "Philip Glass", "song": "Metamorphosis One"}, {"artist": "Steve Reich", "song": "Music for 18 Musicians"}, {"artist": "Terry Riley", "song": "In C"}],
    },
    "신나는 파티! 리듬에 몸을 맡길 때": {
        "디스코 (Disco)": [{"artist": "Bee Gees", "song": "Stayin' Alive"}, {"artist": "ABBA", "song": "Dancing Queen"}, {"artist": "Donna Summer", "song": "Hot Stuff"}],
        "하우스 (House)": [{"artist": "Daft Punk", "song": "Around the World"}, {"artist": "Avicii", "song": "Wake Me Up"}, {"artist": "Calvin Harris", "song": "Summer"}],
        "라틴 팝": [{"artist": "Luis Fonsi", "song": "Despacito"}, {"artist": "Daddy Yankee", "song": "Gasolina"}, {"artist": "Shakira", "song": "Hips Don't Lie"}],
        "K-POP (댄스)": [{"artist": "PSY", "song": "강남스타일"}, {"artist": "BLACKPINK", "song": "뚜두뚜두 (DDU-DU DDU-DU)"}, {"artist": "TWICE", "song": "FANCY"}],
    },
    "일에 집중해야 할 때": {
        "클래식 (피아노 솔로)": [{"artist": "쇼팽", "song": "녹턴 2번"}, {"artist": "베토벤", "song": "월광 소나타 1악장"}, {"artist": "드뷔시", "song": "아마빛 머리의 소녀"}],
        "IDM (Intelligent Dance Music)": [{"artist": "Aphex Twin", "song": "Avril 14th"}, {"artist": "Boards of Canada", "song": "Music Is Math"}, {"artist": "Flying Lotus", "song": "Zodiac Shit"}],
        "다운템포 (Downtempo)": [{"artist": "Bonobo", "song": "Cirrus"}, {"artist": "Four Tet", "song": "Two Thousand and Seventeen"}, {"artist": "Tycho", "song": "Awake"}],
        "자연의 소리 (ASMR)": [{"artist": "Various Artists", "song": "잔잔한 빗소리 (Gentle Rain)"}, {"artist": "Various Artists", "song": "타닥거리는 장작불 소리 (Crackling Fireplace)"}, {"artist": "Various Artists", "song": "숲 속의 아침 (Forest Morning)"}],
    },
}
# 감정 분석 엔진 (이전과 동일)
emotion_lexicon_v4 = {
    "지친 하루의 끝, 위로가 필요할 때": {"위로": 2.5, "힘들": 2, "지쳤": 2, "눈물": 1.5, "혼자": 1.5, "슬퍼": 1, "괜찮아": 1},
    "세상의 중심이 된 듯, 자신감이 폭발할 때": {"자신감": 2.5, "성공": 2, "해냈어": 2, "최고": 1.5, "할수있어": 1.5, "뿌듯": 1, "극복": 1},
    "창 밖에 비가 내릴 때": {"비": 2.5, "창밖": 2, "흐린": 1.5, "센치": 1.5, "빗소리": 1.2, "차분": 1},
    "설레는 밤의 드라이브": {"드라이브": 2.5, "밤공기": 2, "도로": 1.5, "네온사인": 1.5, "설레": 1, "질주": 1},
    "생각이 많아지는 새벽": {"새벽": 2.5, "꿈": 2, "몽환": 2, "고요": 1.5, "생각": 1.2, "잠 못 드는": 1},
    "신나는 파티! 리듬에 몸을 맡길 때": {"파티": 2.5, "신나": 2, "댄스": 1.8, "축제": 1.5, "리듬": 1.2, "흔들어": 1},
    "일에 집중해야 할 때": {"집중": 2.5, "공부": 2, "작업": 2, "코딩": 1.5, "독서": 1.2, "몰입": 1},
}
def analyze_text_mood_v4(text):
    scores = {mood: 0 for mood in emotion_lexicon_v4}
    cleaned_text = re.sub(r'[^\w\s]', '', text).lower()
    for mood, keywords in emotion_lexicon_v4.items():
        for keyword, weight in keywords.items():
            if keyword in cleaned_text: scores[mood] += weight
    positive_scores = {mood: score for mood, score in scores.items() if score > 0}
    return max(positive_scores, key=positive_scores.get) if positive_scores else None

# --- UI 및 로직 함수 ---
def display_song(song):
    """개별 곡을 서식에 맞게 표시하는 함수"""
    query = f"{song['artist']} {song['song']}".replace(" ", "+")
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #333;">
            <div>
                <span style="font-weight: bold; font-size: 1.1em;">{song['song']}</span>
                <br>
                <span style="color: #A0A0A0;">{song['artist']}</span>
            </div>
            <a href="https://www.youtube.com/results?search_query={query}" target="_blank" 
               style="text-decoration: none; color: white; background-color: #FF4B4B; padding: 8px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em;">
                듣기
            </a>
        </div>
        """, unsafe_allow_html=True
    )

def recommend_and_display(genre_name, songs, is_expanded):
    """특정 장르의 곡들을 추천하고 화면에 표시하는 함수"""
    with st.expander(f"🎵 **{genre_name}**", expanded=is_expanded):
        num_to_recommend = min(len(songs), 3) # 최대 3곡 추천
        recommended_songs = random.sample(songs, num_to_recommend)
        for song in recommended_songs:
            display_song(song)

# --- 앱 UI 시작 ---
st.title("🎶 궁극의 뮤직 익스플로러")
st.markdown("당신의 **모든 순간**과 **모든 감정**을 위한, 가장 풍성한 플레이리스트를 만나보세요.")

# 세션 상태 초기화
if 'mood' not in st.session_state:
    st.session_state.mood = None

# 입력 UI
cols = st.columns([0.7, 0.3])
with cols[0]:
    text_input = st.text_input("지금 기분이나 상황을 알려주세요", placeholder="예: 오늘은 코딩에 집중해야 하는 날! 비트있는 음악으로 몰입하고 싶어.")
    if text_input:
        analyzed_mood = analyze_text_mood_v4(text_input)
        if analyzed_mood:
            st.session_state.mood = analyzed_mood

with cols[1]:
    mood_options = ["직접 상황 선택하기"] + list(music_database_v5.keys())
    selected_mood = st.selectbox("직접 상황 선택하기", options=mood_options, label_visibility="collapsed")
    if selected_mood != mood_options[0]:
        st.session_state.mood = selected_mood

# --- 음악 추천 로직 실행 ---
final_mood = st.session_state.mood

if final_mood:
    # 1. 맞춤 추천 섹션
    st.header(f"'{final_mood}' 맞춤 추천", divider="rainbow")
    st.write(f"당신의 **'{final_mood}'** 순간을 위해 엄선한 장르입니다. **새로운 음악을 원하시면 아래 버튼을 누르세요.**")
    
    tailored_genres = music_database_v5[final_mood]
    for genre, songs in tailored_genres.items():
        recommend_and_display(genre, songs, is_expanded=True)
    
    # 2. 다른 장르 둘러보기 섹션
    st.header("다른 장르 둘러보기", divider="gray")
    st.write("새로운 분위기의 음악을 발견해보세요.")

    other_moods = [mood for mood in music_database_v5 if mood != final_mood]
    
    for mood_category in other_moods:
        with st.container(border=True):
            st.subheader(f"'{mood_category}'의 분위기")
            genres_in_mood = music_database_v5[mood_category]
            for genre, songs in genres_in_mood.items():
                recommend_and_display(genre, songs, is_expanded=False)
    
    st.divider()
    # 3. 다른 곡 추천받기 버튼
    # 이 버튼을 누르면 st.rerun()이 호출되어 스크립트 전체가 재실행됩니다.
    # 재실행 시 random.sample()이 다시 호출되므로 자연스럽게 다른 곡이 추천됩니다.
    if st.button('🔄 새로운 음악 탐색하기 (모든 추천곡 갱신)', use_container_width=True, type="primary"):
        st.rerun()

else:
    st.info("텍스트를 입력하거나 메뉴에서 상황을 선택하여 음악 추천을 시작하세요.")