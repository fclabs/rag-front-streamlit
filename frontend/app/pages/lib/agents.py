from typing import TypedDict, Annotated, Sequence
import functools
import operator

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

SUPERVISOR_PROMPT ="""
You are a supervisor that manages a team of travel assistants. You are assisting the user to plan its vacations.

- Do NOT interact with the user.
- If the user does not know where to go on vacations or ask for suggestions offer a location with the suggestion agent.
- If a location was mentioned in the conversation, do NOT call again the suggestion agent.
- If a city or a country is mentioned in the conversation, always explore places to visit near to that location with 
the explorer agent. 
- If there are suggestion mentioned in the conversation, do NOT call again the explorer agent.
- If the weather are not mentioned, offer the weather conditions with the weather agent.
    
Last, use the summary agent to provide a summary of the information gathered during the conversation.

To call the suggestion agent answer with %DEFINE% token.
To call the explorer agent answer with %EXPLORE% token.
To call the weather agent answer with %WEATHER% token.
To call the summary agent answer with %SUMMARY% token.
"""

DEFINE_PROMPT="""
Chose one of the following options:
* Argentina
* Brazil
* Canada
* Denmark
* Egypt
* France

Return to name option choosen. Only mention the name of the country.
"""

EXPLORE_PROMPT="""
You are a travel assistant. Using the location metioned, provide information about interesting places 
around or in that location. 
Do NOT interact with the user.
"""

WEATHER_AGENT_PROMPT="""
Using the location mentioned, provide information about the history weather conditions. 
Do NOT interact with the user.
"""

SUMMARY_PROMPT="""
Provide a summary of the information gathered during the conversation. Say the user to enjoy the vacations.  
Don't ask questions or request confirmation.
"""

MAP = {
    "%WEATHER%": "weather",
    "%EXPLORE%": "explore",
    "%DEFINE%": "define",
    "%SUMMARY%": "summary",
}

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

def create_agent( base_prompt ):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", base_prompt ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    llm_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=1024)
    
    return prompt | llm_model

def agent_node(state: AgentState, agent, name):
    result = agent.invoke(state)
    last = result.content
    
    next = "supervisor"
    if name == "supervisor":
        next = "summary" ## Default next state for supervisor
        
        for token, target in MAP.items():
            if token in last:
                last = last.replace(token, "")
                next = target
                break
    
    return {"messages": [AIMessage(content=last)] if last.strip() else [] , 'next': next }
    
def get_multi_agent():
    
    super_node = functools.partial(agent_node, agent=create_agent(SUPERVISOR_PROMPT), name="supervisor")
    define_node = functools.partial(agent_node, agent=create_agent(DEFINE_PROMPT), name="define")
    explore_node = functools.partial(agent_node, agent=create_agent(EXPLORE_PROMPT), name="explore")
    weather_node = functools.partial(agent_node, agent=create_agent(WEATHER_AGENT_PROMPT), name="weather")
    summary_node = functools.partial(agent_node, agent=create_agent(SUMMARY_PROMPT), name="summary")
    
    workflow = StateGraph(AgentState)
    workflow.add_node("supervisor", super_node)
    workflow.add_node("define", define_node)
    workflow.add_node("explore", explore_node)
    workflow.add_node("weather", weather_node)
    workflow.add_node("summary", summary_node)
    workflow.add_edge(START, "supervisor")

    workflow.add_conditional_edges("supervisor", lambda state: state['next'] )
    workflow.add_edge("summary", END )
    workflow.add_edge("define", "explore" )
    workflow.add_edge("explore", "weather" )
    workflow.add_edge("weather", "supervisor" )
    workflow.compile()
    return workflow.compile()