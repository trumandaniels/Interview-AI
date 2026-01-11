import streamlit as st
import requests
from audio_recorder_streamlit import audio_recorder # pip install audio-recorder-streamlit

BASE_URL = "http://127.0.0.1:8000"

st.title("AI Job Interview Simulator")

if "session_id" not in st.session_state:
    st.session_state.session_id = "user_123" # Generate random ID in prod
    st.session_state.chat_history = []
    st.session_state.started = False

if not st.session_state.started:
    with st.form("setup"):
        resume = st.text_area("Paste Resume Text")
        job = st.text_area("Job Description")
        rubric = st.text_area("Grading Rubric", value="Focus on technical depth and communication clarity.")
        submit = st.form_submit_button("Start Interview")
        
        if submit:
            data = {
                "resume": resume, 
                "job_desc": job, 
                "rubric": rubric, 
                "session_id": st.session_state.session_id
            }
            res = requests.post(f"{BASE_URL}/start_interview", data=data)
            st.session_state.chat_history.append({"role": "ai", "text": res.json()["response"]})
            st.session_state.started = True
            st.rerun()

else:
    # Display Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    # Audio Recorder
    st.write("### Record your answer:")
    audio_bytes = audio_recorder()
    
    if audio_bytes:
        # Prevent double submission
        if "last_audio" not in st.session_state or st.session_state.last_audio != audio_bytes:
            st.session_state.last_audio = audio_bytes
            
            with st.spinner("Transcribing and thinking..."):
                files = {"audio": ("answer.wav", audio_bytes, "audio/wav")}
                data = {"session_id": st.session_state.session_id}
                
                response = requests.post(f"{BASE_URL}/submit_answer", files=files, data=data)
                result = response.json()
                
                # Show user transcription
                if "transcription" in result:
                    st.session_state.chat_history.append({"role": "user", "text": result["transcription"]})
                
                # Show AI response or Final Score
                if result.get("status") == "completed":
                    st.success(f"Interview Complete! Score: {result.get('score', 'N/A')}")
                    st.markdown(result["report"])
                    st.session_state.chat_history.append({"role": "ai", "text": result["report"]})
                else:
                    st.session_state.chat_history.append({"role": "ai", "text": result["response"]})
                
                st.rerun()