import sys
import os
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from src.interview_sim.app.graph import app_graph
from src.interview_sim.app.state import InterviewState





def run_cli_interview():
    print("Starting CLI Example / Test")
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # Mock Data
    initial_state = InterviewState(
        messages=[],
        job_description="Senior Python Developer. Requirements: FastAPI, LangGraph.",
        company_description="TechCorp: AI automation startup.",
        resume_text="I am a Python developer with 5 years of experience.",
        rubric="Evaluate technical accuracy and clarity.",
        common_questions=["Tell me about yourself."],
        question_count=0,
        max_questions=3, 
        is_finished=False
    )

    print("Initializing Interview Graph...", end="\r")
    try:
        events = app_graph.invoke(initial_state, config=config)
    except Exception as e:
        print(f"\n❌ Graph Error: {e}")
        return

    print(" " * 30, end="\r") 
    
    last_message = events["messages"][-1]
    print(f"\n🤖 Interviewer: {last_message.content}\n")

    # 3. Chat Loop
    while True:
        try:
            user_input = input("👤 You: ")
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Exiting.")
                break

            update_data = {"messages": [HumanMessage(content=user_input)]}
            
            print("⏳ Thinking...", end="\r")
            events = app_graph.invoke(update_data, config=config)
            print(" " * 15, end="\r")

            if events.get("feedback_report"):
                print("\n" + "="*40)
                print("🏁 INTERVIEW COMPLETE")
                print("="*40)
                print(f"Final Score: {events.get('final_score')}/100")
                print("\n📝 FEEDBACK REPORT:")
                print(events["feedback_report"])
                break
            
            last_message = events["messages"][-1]
            print(f"\n🤖 Interviewer: {last_message.content}\n")

        except Exception as e:
            print(f"\n❌ Runtime Error: {e}")
            break

if __name__ == "__main__":
    run_cli_interview()