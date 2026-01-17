# Interview AI

## What this project is
Interview AI is an open-source, interactive mock interview agent designed to simulate real-world behavioral and technical interviews. This project uses LangGraph to build a stateful, cyclic conversational flow. It acts as an adaptive interviewer. Interview AI probes your responses, asking relevant follow-up questions, and pivoting topics based on your answers, just like a human hiring manager would.

## How to run currently (command line frontend)
Windows:
`python.exe examples/cli_test.py`

Linux (untested):
`python examples\cli_test.py`

## How to run (Streamlit frontend currently broken)
First, you need to run the LangGraph server component
`cd src/interview_sim`
`uvicorn interview_sim.app.main:app --reload`

Then, in a different console you need to run the front end

Windows:
`streamlit run src/interview_sim/frontend/app.py`

Linux (untested):
`streamlit run src\interview_sim\frontend/app.py`