import streamlit as st

# ページの設定
st.set_page_config(page_title="二択アンケート", page_icon="📝", layout="centered")

# セッション状態の初期化
if "page" not in st.session_state:
    st.session_state.page = 0  # 0: スタート, 1~5: 質問1~5, 6: 結果
if "answers" not in st.session_state:
    st.session_state.answers = []

# 質問リスト（計5問）
# ※ 質問3・4・5 の回答（0か1）の組み合わせで8パターンの結果を判定します
questions = [
    {"q": "質問1：朝型ですか、夜型ですか？", "choices": ["朝型", "夜型"]},
    {"q": "質問2：平日派ですか、休日派ですか？", "choices": ["平日派", "休日派"]},
    {"q": "質問3：インドア派ですか、アウトドア派ですか？", "choices": ["インドア派", "アウトドア派"]},
    {"q": "質問4：きのこの山ですか、たけのこの里ですか？", "choices": ["きのこの山", "たけのこの里"]},
    {"q": "質問5：コーヒーですか、紅茶ですか？", "choices": ["コーヒー", "紅茶"]}
]

# 8パターンの結果の定義 (質問3, 質問4, 質問5 の選択順)
# キーは (Q3の選択肢, Q4の選択肢, Q5の選択肢)
results_map = {
    ("インドア派", "きのこの山", "コーヒー"): {
        "title": "☕️ 【タイプA】おうち籠もりこだわり派",
        "desc": "静かな室内にこだわりコーヒーと甘いお菓子を持ち込んでマイペースに過ごすのが大好きなタイプです！"
    },
    ("インドア派", "きのこの山", "紅茶"): {
        "title": "🫖 【タイプB】優雅なティータイム派",
        "desc": "お部屋でゆったり紅茶の香りを楽しみながら、落ち着いた時間を大切にするタイプです！"
    },
    ("インドア派", "たけのこの里", "コーヒー"): {
        "title": "💻 【タイプC】集中力抜群の作業派",
        "desc": "お気に入りのデスクでサクサク作業を進めつつ、コーヒーブレイクを上手に楽しむタイプです！"
    },
    ("インドア派", "たけのこの里", "紅茶"): {
        "title": "📚 【タイプD】まったり癒やし読書派",
        "desc": "おうちで心地よい音楽と紅茶をお供に、のんびり自分時間を味わうタイプです！"
    },
    ("アウトドア派", "きのこの山", "コーヒー"): {
        "title": "🏕 【タイプE】アクティブキャンプ派",
        "desc": "外に出かけて自然の中で本格コーヒーを淹れ、エネルギッシュに活動するのが大好きなタイプです！"
    },
    ("アウトドア派", "きのこの山", "紅茶"): {
        "title": "🚶‍♂️ 【タイプF】爽やかお散歩派",
        "desc": "青空の下、マイボトルに美味しい紅茶を入れてピクニックや散策を楽しむタイプです！"
    },
    ("アウトドア派", "たけのこの里", "コーヒー"): {
        "title": "🏃‍♂️ 【タイプG】パワフル冒険派",
        "desc": "とにかく外で身体を動かしたり新しい刺激に出会うのが好きで、行動力抜群なタイプです！"
    },
    ("アウトドア派", "たけのこの里", "紅茶"): {
        "title": "🌺 【タイプH】リゾート・リフレッシュ派",
        "desc": "外の雰囲気を感じながら、優雅にリゾート気分で休日を楽しむバランス重視タイプです！"
    },
}

# --- ページ0：スタート画面 ---
if st.session_state.page == 0:
    st.title("📝 診断アンケート")
    st.write("全5問のアンケートに答えて、あなたのタイプを診断してみましょう！")
    
    if st.button("アンケートを始める", type="primary", use_container_width=True):
        st.session_state.answers = []
        st.session_state.page = 1
        st.rerun()

# --- ページ1〜5：質問画面 ---
elif 1 <= st.session_state.page <= 5:
    q_idx = st.session_state.page - 1
    
    st.progress(st.session_state.page / 5, text=f"質問 {st.session_state.page} / 5")
    st.subheader(questions[q_idx]["q"])
    
    # ラジオボタン
    choice = st.radio(
        "選択肢を選んでください：",
        questions[q_idx]["choices"],
        key=f"q_choice_{q_idx}"
    )
    
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.page > 1:
            if st.button("戻る", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()
    with col2:
        if st.button("次へ", type="primary", use_container_width=True):
            if len(st.session_state.answers) > q_idx:
                st.session_state.answers[q_idx] = choice
            else:
                st.session_state.answers.append(choice)
            
            st.session_state.page += 1
            st.rerun()

# --- ページ6：結果画面 ---
elif st.session_state.page == 6:
    st.title("🎉 診断結果")
    
    # 後半3つ（質問3, 4, 5）の回答を取得
    q3_ans = st.session_state.answers[2]
    q4_ans = st.session_state.answers[3]
    q5_ans = st.session_state.answers[4]
    
    # 8パターンから一致する結果を取得
    result_key = (q3_ans, q4_ans, q5_ans)
    result = results_map.get(result_key, {
        "title": "診断完了",
        "desc": "ご回答ありがとうございました！"
    })
    
    # 結果の表示
    st.header(result["title"])
    st.info(result["desc"])
    
    st.write("---")
    st.subheader("📋 あなたの回答一覧")
    for i, ans in enumerate(st.session_state.answers):
        st.write(f"・**{questions[i]['q']}** → {ans}")
    
    st.write("")
    if st.button("最初に戻る", type="primary", use_container_width=True):
        st.session_state.page = 0
        st.session_state.answers = []
        st.rerun()
