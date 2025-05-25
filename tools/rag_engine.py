from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./data/Dummy_Return_Policy.pdf")
pages = []
for page in loader.alazy_load():
    pages.append(page)

# Step 2: Split into fixed-size chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=10
)
chunks = splitter.split_documents(pages)
# Use OpenAI's embedding model
embedding_model = OpenAIEmbeddings()  

# Save to a persistent directory
vectorstore = Chroma.from_documents(chunks, embedding_model, persist_directory="./data/chroma_store")
vectorstore.persist()

retriever = vectorstore.as_retriever()

query = "non-returnable?"
docs = retriever.get_relevant_documents(query)

for i, doc in enumerate(docs):
    print(f"\n--- Relevant Chunk {i+1} ---\n{doc.page_content[:300]}")