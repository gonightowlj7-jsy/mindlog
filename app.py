import streamlit as st
import google.generativeai as genai

# 페이지 기본 설정
st.set_page_config(page_title="늘옆에", page_icon="💬")

# 사이드바: 제목 및 사용 설명
with st.sidebar:
    st.title("💬 늘옆에 (Always By Your Side)")
    st.markdown("당신의 마음을 들어주는 AI 친구입니다.")
    st.markdown("---")
    st.info("비밀 보장: 대화 내용은 저장되지 않습니다.")
    
    # API 키 입력받기
    api_key = st.text_input("Google API Key를 입력하세요", type="password")
    if not api_key:
        st.warning("앱을 사용하려면 API 키가 필요합니다.")

# === 뇌(Brain) 설정: 시스템 프롬프트 ===
system_instruction = """
너의 이름은 '늘옆에'다. 너는 사용자의 가장 친한 친구이자, 심리 상담 보조 AI다.

[대화 원칙]
1. 따뜻한 친구: 부드러운 반말과 존댓말이 섞인 친근한 구어체 사용.
2. 절대 공감: 해결책 제시 금지. 오직 경청하고 공감하며 되물어주기.
3. 기억 유지: 수면 패턴, 식욕, 스트레스 원인, 감정 키워드를 기억할 것.

[닥터 리포트 기능]
사용자가 '/리포트'라고 입력하면 친구 모드를 해제하고 다음 양식의 '의료진 제출용 보고서'를 출력하라.

- 양식:
## 🏥 [늘옆에] 심리 상태 요약 리포트
1. 주호소 (Chief Complaint)
2. 주요 증상 데이터 (수면/식욕/감정 키워드/스트레스 요인)
3. 관찰 소견
4. 상세 대화 로그
5. 제안: 의사 선생님께 이 화면을 보여주세요.
"""

# === 앱 로직 ===
if api_key:
    # 1. 모델 설정
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction=system_instruction
    )

    # 2. 채팅 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "model", "content": "안녕? 오늘 하루는 어땠어? 무거운 마음이 있다면 나한테 다 털어놔도 돼."})

    # 3. 화면에 이전 대화 표시
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["content"])

    # 4. 사용자 입력 처리
    if prompt := st.chat_input("하고 싶은 말을 적어보세요..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            
        st.session_state.messages.append({"role": "model", "content": response.text})
