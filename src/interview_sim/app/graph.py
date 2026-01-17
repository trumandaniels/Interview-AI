from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.sqlite import SqliteSaver #For a more advanced e.g. persistant version in the future
from langgraph.checkpoint.memory import MemorySaver
from .state import InterviewState

llm = ChatOpenAI(model="gpt-5-nano")

def generate_question_node(state: InterviewState):
    if state.question_count >= state.max_questions:
        return {"is_finished": True}
        
    system_prompt = f"""
    You are an expert interviewer for {state.company_description}.
    Job Role: {state.job_description}
    Candidate Resume: {state.resume_text}
    
    Your Goal: Assess the candidate based on the following RUBRIC:
    {state.rubric}
    
    History of questions asked so far is in the chat history.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{messages}")
    ])
    
    chain = prompt | llm
    
    try:
        inputs = state.model_dump()
    except AttributeError:
        inputs = state.dict() #
        
    response = chain.invoke(inputs)
    
    return {
        "messages": [response], 
        "question_count": state.question_count + 1
    }

def grading_node(state: InterviewState):
    system_prompt = f"""
    The interview is over. You are the Lead Hiring Manager.
    Rubric: {state.rubric}
    Task: Analyze the conversation...
    """
    
    messages = state.messages
    response = llm.invoke([("system", system_prompt)] + messages)
    
    content = response.content
    return {"final_score": 0, "feedback_report": content}

def route_conversation(state: InterviewState):
    if state.is_finished:
        return "to_grader"
    return "wait_for_user"

workflow = StateGraph(InterviewState)
workflow.add_node("interviewer", generate_question_node)
workflow.add_node("grader", grading_node) 

workflow.add_edge(START, "interviewer")
workflow.add_conditional_edges(
    "interviewer",
    route_conversation,
    {
        "to_grader": "grader", 
        "wait_for_user": END 
    }
)
workflow.add_edge("grader", END)

checkpointer = MemorySaver()
app_graph = workflow.compile(checkpointer=checkpointer)