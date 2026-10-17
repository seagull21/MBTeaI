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
    {"q": "質問1：あなたはどちらのタイプ？", "choices": ["1つのものを極めたい", "色々なものを試したい"]},
    {"q": "質問2：魅力を感じるのは？", "choices": ["見た目では分からない奥深さ", "第一印象から分かる個性"]},
    {"q": "質問3：好きなのはどっち？", "choices": ["だしの効いた料理", "香辛料の効いた料理"]},
    {"q": "質問4：好きな味は？", "choices": ["まろやかで甘い味", "キリッとした味"]},
    {"q": "質問5：今飲みたいのは？", "choices": ["あったかい飲み物", "冷たい飲み物"]}
]

# 8パターンの結果の定義 (質問3, 質問4, 質問5 の選択順)
# キーは (Q3の選択肢, Q4の選択肢, Q5の選択肢)
results_map = {
    ("だしの効いた料理", "まろやかで甘い味", "あったかい飲み物"): {
        "title": "【タイプ：りん】〇〇派",
        "desc": "あなたは〇〇なタイプです！"
    },
    ("だしの効いた料理", "まろやかで甘い味", "冷たい飲み物"): {
        "title": "【タイプ：くぼっち】〇〇派",
        "desc": "あなたは〇〇なタイプです！"
    },
    ("だしの効いた料理", "キリッとした味", "あったかい飲み物"): {
        "title": "【タイプ：こーへい】〇〇派",
        "desc": "あなたは〇〇なタイプです！"
    },
    ("だしの効いた料理", "キリッとした味", "冷たい飲み物"): {
        "title": "【タイプ：にいちゃん】〇〇派",
        "desc": "あなたは〇〇なタイプです！"
    },
    ("香辛料の効いた料理", "まろやかで甘い味", "あったかい飲み物"): {
        "title": "【タイプ：さとっしー】〇〇派",
        "desc": "あなたは〇〇なタイプです！"
    },
    ("香辛料の効いた料理", "まろやかで甘い味", "冷たい飲み物"): {
        "title": "【タイプ：フルオロ】〇〇派",
        "desc": "あなたは〇〇なタイプです！"
    },
    ("香辛料の効いた料理", "キリッとした味", "あったかい飲み物"): {
        "title": "【タイプ：こーちゃん】〇〇派",
        "desc": "あなたは〇〇なタイプです！"
    },
    ("香辛料の効いた料理", "キリッとした味", "冷たい飲み物"): {
        "title": "【タイプ：かいびぃ】〇〇派",
        "desc": "あなたは〇〇なタイプです！"
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
