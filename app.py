import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="늘옆에", page_icon="💬")

# 사이드바
with st.sidebar:
    st.title("💬 늘옆에 (MindLog)")
    st.info("비밀 보장: 대화 내용은 저장되지 않습니다.")
    # 공백 제거 기능 추가 (실수로 빈칸 들어가도 작동하게)
    api_key_input = st.text_input("새로 만든 Google API Key를 입력하세요", type="password")
    api_key = api_key_input.strip() if api_key_input else None

# 시스템 프롬프트 (성격 설정)
system_instruction = """
너의 이름은 '늘옆에'다. 너는 사용자의 가장 친한 친구이자, 심리 상담 보조 AI다.
해결책을 주지 말고, 오직 경청하고 공감해줘.
'/리포트'라고 하면 의료진 제출용 심리 상태 요약 보고서를 작성해줘.
"""

# 앱 로직
if api_key:
    try:
        genai.configure(api_key=api_key)
        # [수정] 가장 안정적인 gemini-pro 모델 사용
        model = genai.GenerativeModel("gemini-pro") 
        
        # 채팅창 초기화
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "model", "content": "안녕? 오늘 마음은 좀 어때? 나한테 다 털어놔도 돼. (지금 시스템 프롬프트가 적용된 gemini-pro 모델입니다.)"}
            ]

        # 이전 대화 표시
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "assistant"
            with st.chat_message(role):
                st.markdown(msg["content"])

        # 채팅 입력 및 처리
        if prompt := st.chat_input("하고 싶은 말을 적어보세요..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                # 프롬프트에 페르소나 강제 주입 (gemini-pro 호환성 위해)
                full_prompt = system_instruction + "\n\n사용자: " + prompt
                
                chat = model.start_chat(history=[])
                response = chat.send_message(full_prompt)
                st.markdown(response.text)
            
            st.session_state.messages.append({"role": "model", "content": response.text})
            
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
        st.error("API 키가 올바른지 확인해주세요. (새로 만든 키를 써주세요!)")
