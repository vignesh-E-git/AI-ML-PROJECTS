from typing import TypedDict,Annotated,Sequence

from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage,ToolMessage,AIMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

# AGENT STATE SCHEMA
class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage],add_messages]

llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash')

# NODE FUNCTIONS
def process(state : AgentState)-> AgentState:
    system_prompt = SystemMessage(content = 'you are an chatbot , respond to the user very funny and short. ')
    user_msg = state['messages']

    try:
        response = llm.invoke([system_prompt] + user_msg)
        print(f'\nAI : {response.content}')

    except Exception as e:
        print(e)
        return {'messages' : ''}
    return {'messages': [AIMessage(content = response.content)]}

# EDGES + GRAPH BUILING
graph = StateGraph(AgentState)
graph.add_node('process',process)
graph.add_edge(START,'process')
graph.add_edge('process',END)

# DRAW Graph
app = graph.compile()
#app.get_graph().draw_mermaid_png(output_file_path='Chatbot/graphImg.png')

print('='*60)
print('HI I AM A CHATBOT'.center(50))
print('='*60)
print('type EXIT or QUIT to exit the chat')

print()
user_input = input('YOU : ')
conversation = []

while user_input.lower() not in ['exit','quit']:
    conversation.append(HumanMessage(content= user_input))
    res = app.invoke({'messages' : conversation})

    conversation = res['messages']
    user_input = input('\nYOU : ')





