from agents import Agent, function_tool
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings



# tool 1 - rag retriever - should check if return eligible or not.
@function_tool
def rag_retriever(query: str):
    """
    Use this tool to retrieve relevant documents from the knowledge base to answer return policy questions.
    """
    embedding_model = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="./data/chroma_store", embedding_function=embedding_model)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    results = retriever.get_relevant_documents(query)
    return results

#tool 2 - generate return ticket - if eligible, generate a return ticket.
@function_tool
def process_return():
    """
    Use this tool to process customer returns.
    """
    print(f"Processing return customer.")
    return "Return ticket created. ID: 12345"
    # In a real-world scenario, this would interact with a ticketing system

@function_tool
def escalate_to_manager():
    """
    Use this tool to escalate the issue to a manager.
    """
    print(f"Escalating non-eligible return to manager.")
    return "Issue escalated to manager."


# agent - should use the tools to check if return eligible or not.
# if eligible, generate a return ticket.

return_agent = Agent(
    name="Return Agent",
    model="gpt-4o", 
    instructions="You are a return agent and your job is to check if the return is eligible or not using the rag_retriever tool "+  
    "You will get a reason for your summoning as input. " +
    "You will use the rag_retriever tool to check if the return is eligible or not. " +
    "if eligible, process the return using the process_return tool. " +
    "if not eligible, tell the customer that this is not eligible for return. " +
    "if not eligible and the customer still wants to return, escalate the issue to a manager using the escalate_to_manager tool. " +
    "You can ask the user for reason for return if not already provided.",
    
    tools=[
        rag_retriever,
        process_return,
        escalate_to_manager
    ],
    handoff_description="Handles all return and refund related queries"
)


