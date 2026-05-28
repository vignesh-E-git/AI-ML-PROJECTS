# NOTEs
# 1.at line 28 , update the path to store the vector db
# 2. No memory BOT
# 3. modify testing and dot env
from typing import Sequence,Annotated,TypedDict,List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from langchain_core.messages import BaseMessage, AIMessage,HumanMessage,ToolMessage,SystemMessage
from langgraph.graph.message import add_messages

from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

load_dotenv(r'C:\VKY\02_SKILLS\LANGHAIN\LEVEL-2\.env')

DEBUG = True


def debug_print(message: str) -> None:
    if DEBUG:
        print(f'[DEBUG] {message}')


# INPUT - pdf path ; OUTUT - a message
# pdf -> chunking -> embedding
# UNDONE


# path = ''
# db = create_db(path)

# embedding_model = GoogleGenerativeAIEmbeddings(model = 'gemini-embedding-2')
db = None
def set_up_db(path):
    global db
    db = path

# AGENT ARCHITECTURE
# 1.create agentstate
class AgentState(TypedDict):
    message : Annotated[Sequence[BaseMessage],add_messages]

#----------helper for testing----------------------
# db = Chroma(
#     collection_name= 'pdf_data',
#     persist_directory = db,
#     embedding_function= GoogleGenerativeAIEmbeddings(model = 'gemini-embedding-2')
# )
path_env = r'C:\VKY\02_SKILLS\LANGHAIN\LEVEL-2\.env'

#-------------------------------
# 2.create tools
@tool
def retrieve_tool(query:str) -> str:
    '''This tool is used to retrieve related information for a given query.'''
    debug_print(f'retrieve_tool called with query: {query}')

    if db is None:
        return 'vector db is not config.'
    
    retriever = db.as_retriever(
        search_type = 'similarity' ,
        search_kwargs = {'k' : 4}
    )
    data = retriever.invoke(query)
    debug_print(f'Retriever returned {len(data) if data else 0} document(s).')

    if not data:
        debug_print('No matching data found for query.')
        return 'DATA NOT FOUND.'
    if data:
        debug_print('Data retrieved successfully.')

    res = []
    for i,chunk in enumerate(data):
        debug_print(f'Formatting retrieved document {i+1}. Content length: {len(chunk.page_content)}')
        res.append(f'Document : {i+1}\n{chunk.page_content}\n')
    return '\n\n'.join(res)

# 3.CREATE NODE , GRAPH

tools = [retrieve_tool]
tool_dict = {tool.name : tool for tool in tools}
llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash').bind_tools(tools=tools)

def process(state:AgentState) -> AgentState:
    debug_print(f'Process node started. Message count: {len(state["message"])}')
    system_prompt = 'you are a instructor . you have given a tool to retrieve information from the provided document . you work is to use the tool and respond from that chunksl. please dont hallucinate or make up.'
    messages = [SystemMessage(content=system_prompt), *state['message']]
    response = llm.invoke(messages)
    debug_print(f'LLM response received. Tool calls: {len(response.tool_calls) if hasattr(response, "tool_calls") else 0}')
    return {'message': response}


def should_continue(state : AgentState) -> AgentState:
    debug_print('should_continue node started.')
    last_msg = state['message'][-1]
    if not hasattr(last_msg,'tool_calls') or not last_msg.tool_calls:
        debug_print('No tool calls found. Routing to END.')
        return 'exit'
    else:
        debug_print(f'Tool calls found: {len(last_msg.tool_calls)}. Routing to retriever_agent.')
        return 'tool'

def retriever_agent(state : AgentState) -> AgentState: # tool node
    debug_print('retriever_agent node started.')
    # check if the tool is a valid tool available.
    llm_tool = state['message'][-1].tool_calls
    debug_print(f'Latest LLM tool payload: {llm_tool}')

    results = []
    for tool in llm_tool:
        debug_print(f'Processing tool call: {tool}')
        name = tool['name']
        query = tool['args'].get('query','')
        if name in tool_dict:
            
            
            debug_print(f'Invoking tool "{name}" with query: {query}')
            result = tool_dict[name].invoke(query)
        else:
            debug_print('Invalid tool call received.')
            result = 'NO VALID TOOL FOUND.'
        results.append(ToolMessage(name = tool['name'] , tool_call_id=tool["id"],content=result))
        debug_print(f'Tool message prepared for tool call id: {tool["id"]}')
    return {'message' : results}

# 4. node and connect edges
graph = StateGraph(AgentState)

graph.add_node('process',process)
graph.add_node('should_continue',lambda state:state)
graph.add_node('retriever_agent',retriever_agent)

graph.add_edge(START,'process')
graph.add_edge('process','should_continue')
graph.add_conditional_edges('should_continue',path = should_continue,
                            path_map= {'tool' : 'retriever_agent' ,
                                       'exit' : END})
graph.add_edge('retriever_agent','process')

app = graph.compile()
#app.get_graph().draw_mermaid_png(output_file_path='RAG/rag.png')



# execute 
def Agent(query:str)->str:

    debug_print(f'Application invocation started with query: {query}')
    result = app.invoke({'message' : [HumanMessage(content = query)]})
    debug_print('Application invocation completed.')
    print('result\n')

    content = result['message'][-1].content
    if isinstance(content,str):
        return content
    return content[0]['text']
