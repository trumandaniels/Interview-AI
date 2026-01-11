# Interview AI

## What this project is
Interview AI is an open-source, interactive mock interview agent designed to simulate real-world behaviorall and technical interviews. This project uses LangGraph to build a stateful, cyclic conversational flow. It acts as an adaptive interviewer. Interview AI probes your responses, asking relevant follow-up questions, and pivoting topics based on your answers, just like a human hiring manager would.

## How to run
First, you need to run the LangGraph server component
`uvicorn src\interview_sim.app.main:app --reload`

Then, in a different console you need to run the front end
`streamlit run src/interview_sim/frontend/app.py`