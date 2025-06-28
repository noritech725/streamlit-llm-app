from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


def get_expert_response(input_text, expert_type):
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーからの入力テキスト
        expert_type (str): 専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    # 専門家タイプに応じてシステムメッセージを設定
    expert_prompts = {
        "医療専門家": "あなたは経験豊富な医療専門家です。医学的な知識を基に、正確で分かりやすい回答を提供してください。ただし、診断や治療に関する具体的なアドバイスは避け、必要に応じて医療機関への相談を勧めてください。",
        "法律専門家": "あなたは経験豊富な法律専門家です。法的な観点から正確で分かりやすい情報を提供してください。ただし、具体的な法的アドバイスは避け、必要に応じて専門の弁護士への相談を勧めてください。",
        "IT専門家": "あなたは経験豊富なIT専門家です。プログラミング、システム設計、技術トレンドなどに関する専門的で実践的なアドバイスを提供してください。コード例や具体的な解決策も含めて回答してください。",
        "料理専門家": "あなたは経験豊富な料理専門家です。レシピ、調理技術、食材の知識、栄養に関する情報を分かりやすく提供してください。実践的なコツやアドバイスも含めて回答してください。"
    }
    
    # LLMの初期化
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # メッセージの作成
    messages = [
        SystemMessage(content=expert_prompts[expert_type]),
        HumanMessage(content=input_text),
    ]
    
    # LLMに問い合わせて結果を取得
    result = llm(messages)
    return result.content

# Streamlitアプリのメイン部分
st.title("🤖 AI専門家チャットボット")

st.markdown("""
## アプリの概要
このアプリでは、様々な分野の専門家として振る舞うAIとチャットできます。
質問したい分野の専門家を選択して、自由に質問してみてください。

## 操作方法
1. **専門家を選択**: ラジオボタンから相談したい分野の専門家を選んでください
2. **質問を入力**: テキストエリアに質問や相談内容を入力してください
3. **送信**: 「回答を取得」ボタンをクリックして、AI専門家からの回答を受け取ってください

## 利用可能な専門家
- **医療専門家**: 健康や医学に関する質問
- **法律専門家**: 法律や規制に関する質問
- **IT専門家**: プログラミングや技術に関する質問
- **料理専門家**: レシピや調理技術に関する質問
""")

st.divider()

# 専門家選択のラジオボタン
expert_type = st.radio(
    "相談したい専門家を選択してください:",
    ["医療専門家", "法律専門家", "IT専門家", "料理専門家"],
    index=0
)

# 入力フォーム
user_input = st.text_area(
    "質問や相談内容を入力してください:",
    placeholder="こちらに質問を入力してください...",
    height=150
)

# 送信ボタンと回答表示
if st.button("回答を取得", type="primary"):
    if user_input.strip():
        with st.spinner(f"{expert_type}が回答を準備しています..."):
            try:
                response = get_expert_response(user_input, expert_type)
                
                st.success("回答が完了しました！")
                st.subheader(f"💬 {expert_type}からの回答:")
                st.write(response)
                
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
                st.info("APIキーが正しく設定されているか確認してください。")
    else:
        st.warning("質問を入力してください。")