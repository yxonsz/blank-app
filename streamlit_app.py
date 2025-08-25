import streamlit as st
import random

# --- 앱 구성 설정 ---
st.set_page_config(
    page_title="무드 플레이리스트",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- 데이터 ---
# 각 기분과 장르에 맞는 노래 목록 (예시 데이터)
# 실제 애플리케이션에서는 더 많은 곡을 데이터베이스나 API를 통해 가져올 수 있습니다.
music_database = {
    "행복": {
        "팝": [
            {"artist": "방탄소년단", "song": "Dynamite"},
            {"artist": "아이유", "song": "Celebrity"},
            {"artist": "TWICE", "song": "Dance The Night Away"},
        ],
        "댄스": [
            {"artist": "Mark Ronson", "song": "Uptown Funk (Feat. Bruno Mars)"},
            {"artist": "Dua Lipa", "song": "Don't Start Now"},
            {"artist": "Justin Timberlake", "song": "Can't Stop the Feeling!"},
        ],
        "인디": [
            {"artist": "볼빨간사춘기", "song": "여행"},
            {"artist": "10CM", "song": "사랑은 은하수 다방에서"},
            {"artist": "치즈(CHEEZE)", "song": "Madeleine Love"},
        ],
    },
    "슬픔": {
        "발라드": [
            {"artist": "박효신", "song": "야생화"},
            {"artist": "Adele", "song": "Someone Like You"},
            {"artist": "이선희", "song": "인연"},
        ],
        "R&B": [
            {"artist": "딘(DEAN)", "song": "D (half moon)"},
            {"artist": "백예린", "song": "우주를 건너"},
            {"artist": "Frank Ocean", "song": "Thinking Bout You"},
        ],
        "OST": [
            {"artist": "거미", "song": "You Are My Everything"},
            {"artist": "Lasse Lindh", "song": "C'mon Through"},
            {"artist": "김필", "song": "그때 그 아인"},
        ],
    },
    "에너지 넘치는": {
        "록": [
            {"artist": "Queen", "song": "Don't Stop Me Now"},
            {"artist": "윤도현밴드", "song": "나는 나비"},
            {"artist": "Bon Jovi", "song": "It's My Life"},
        ],
        "힙합": [
            {"artist": "지코 (ZICO)", "song": "아무노래"},
            {"artist": "Eminem", "song": "Lose Yourself"},
            {"artist": "다이나믹 듀오", "song": "출첵"},
        ],
        "EDM": [
            {"artist": "The Chainsmokers", "song": "Closer"},
            {"artist": "Avicii", "song": "Wake Me Up"},
            {"artist": "Calvin Harris", "song": "Summer"},
        ],
    },
    "차분한": {
        "재즈": [
            {"artist": "Norah Jones", "song": "Don't Know Why"},
            {"artist": "Chet Baker", "song": "My Funny Valentine"},
            {"artist": "Billie Holiday", "song": "Summertime"},
        ],
        "어쿠스틱": [
            {"artist": "Jason Mraz", "song": "I'm Yours"},
            {"artist": "Ed Sheeran", "song": "Thinking Out Loud"},
            {"artist": "Jeff Buckley", "song": "Hallelujah"},
        ],
        "클래식": [
            {"artist": "클로드 드뷔시", "song": "달빛 (Clair de Lune)"},
            {"artist": "요한 파헬벨", "song": "캐논 변주곡"},
            {"artist": "프레데리크 쇼팽", "song": "녹턴 2번"},
        ],
    },
}

# --- 앱 UI ---

st.title("🎵 무드 플레이리스트")
st.write("오늘 당신의 기분은 어떤가요? 기분에 맞는 노래를 추천해 드립니다.")

# --- 입력 방식 선택 ---
input_method = st.radio(
    "어떻게 기분을 알려주시겠어요?",
    ("객관식으로 선택하기", "주관식으로 입력하기"),
    horizontal=True,
    label_visibility="collapsed"
)

user_mood = ""
mood_detected = False

# 객관식 입력
if input_method == "객관식으로 선택하기":
    mood_options = list(music_database.keys())
    selected_mood = st.selectbox("오늘의 기분을 선택해주세요.", mood_options, index=None, placeholder="기분을 선택하세요...")
    if selected_mood:
        user_mood = selected_mood
        mood_detected = True

# 주관식 입력
else:
    text_input = st.text_input("오늘의 기분이나 상태를 자유롭게 입력해보세요. (예: 행복, 우울, 신나는 등)")
    if text_input:
        # 간단한 키워드 매칭
        for mood in music_database.keys():
            if mood in text_input:
                user_mood = mood
                mood_detected = True
                break
        if not mood_detected:
            st.warning("입력하신 기분에 맞는 추천 목록이 아직 준비되지 않았어요. 다른 키워드를 시도해보세요. (예: 행복, 슬픔, 에너지 넘치는, 차분한)")

# --- 노래 추천 로직 ---
if mood_detected:
    st.header(f"'{user_mood}' 기분을 위한 노래 추천", divider="rainbow")

    # 해당 기분에 맞는 장르 목록 가져오기
    genres = list(music_database[user_mood].keys())

    # 탭을 사용하여 장르별 추천 표시
    tabs = st.tabs(genres)

    for i, genre in enumerate(genres):
        with tabs[i]:
            st.subheader(f"🎧 {genre} 장르")
            
            # 해당 장르의 노래 목록 가져오기
            songs_in_genre = music_database[user_mood][genre]
            
            # 랜덤으로 3곡 이상 추천 (데이터가 3곡 미만일 경우 있는 만큼만)
            num_to_recommend = min(len(songs_in_genre), 3)
            recommended_songs = random.sample(songs_in_genre, num_to_recommend)
            
            # 추천 곡 목록 출력
            for j, song in enumerate(recommended_songs):
                col1, col2 = st.columns([1, 4])
                with col1:
                    # 이모티콘으로 순위 느낌 표현
                    st.markdown(f"### {j+1}위")
                with col2:
                    st.markdown(f"**{song['song']}** - {song['artist']}")
                    # 검색 링크 제공 (유튜브 검색)
                    st.link_button("노래 듣기 (YouTube)", f"https://www.youtube.com/results?search_query={song['artist']}+{song['song']}")
