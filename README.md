# Customer Support Chat Application

A voice-enabled AI customer support chat application that uses multiple specialized agents to handle different types of customer queries.

## Project Overview

This project implements a conversational AI system with a Streamlit-based user interface that can handle customer support queries through both text and voice input. The system uses a triage agent to route queries to specialized agents based on the nature of the question.

## Architecture

### Agents

1. **Triage Agent**: The central coordinator that determines which specialized agent should handle a customer query. Acts as the first point of contact and can also respond to general questions.

2. **Returns Agent**: Specializes in handling product return queries, accessing a knowledge base to determine return eligibility.

    - Tools Available:
        - RAG Retrieval (to check if return is eligible)
        - Process Return (to process the return if eligible)
        - Escalate to Manager (to escalate the issue to a manager if not eligible)

3. **Tracking Agent**: Focuses on providing order status and tracking information for customers.

    - Tools Available:
        - Get Order Status (to get the order status)


## Technology Stack

- **Frontend**: Streamlit, streamlit-chat, streamlit-mic-recorder
- **Backend**: FastAPI
- **AI Agents**: OpenAI Agents SDK
- **Speech-to-Text**: OpenAI Whisper
- **Vector Database**: Chroma
- **Embeddings**: OpenAI Embeddings
- **Package Management**: uv

## Installation

### Prerequisites

- Python 3.10+
- OpenAI API key

### Setup

1. Clone the repository

2. Create and activate a virtual environment using uv:

```bash
pip install uv
uv venv
uv venv activate
```

3. Install dependencies:

```bash
uv pip install -r requirements.txt
```

4. Set up your OpenAI API key:

Create a `.env` file in the project root with the following content:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

1. First, start the FastAPI server for order status API:

```bash
python -m uvicorn tools.order_api:app --reload
```

2. In a new terminal, run the Streamlit application:

```bash
streamlit run main.py
```

3. Open your browser and navigate to the URL displayed in the terminal (usually http://localhost:8501)



## Agent Details

### Triage Agent
The coordinator that determines which specialized agent to use based on the customer's question. It:
- Analyzes incoming queries
- Routes to appropriate specialized agent
- Handles general questions directly
- Uses input guardrails to filter inappropriate content

### Returns Agent
Handles all return and refund related queries. It has the following tools:
- **RAG Retriever**: Accesses vector database to check return eligibility
- **Process Return**: Creates return tickets for eligible returns
- **Escalate to Manager**: Handles special cases requiring manager intervention

### Tracking Agent
Handles order status and tracking queries. It has the following tool:
- **Get Order Status**: Retrieves order information from the order database

## Voice Input

The application uses OpenAI's Whisper model for speech-to-text transcription, allowing customers to:
- Record voice messages directly in the browser
- Have speech automatically transcribed and processed
- Interact with the support system naturally through voice

## Implementation Notes

- The UI is based on the streamlit-chatgpt-ui template
- The RAG system uses Chroma as the vector store
- Handoffs between agents are handled transparently to the user
- Order data is stored in a simple CSV file for demonstration purposes

## Data Files

### Dummy Return Policy
A PDF document containing the return policy rules used by the RAG system. This document is processed and stored in a Chroma vector database. The RAG retriever tool queries this database to determine if a return is eligible based on the customer's query.

The return policy covers various scenarios like:
- Standard return windows (30 days)
- Non-returnable items (gift cards, personalized items)
- Damaged items policy
- Return shipping costs
- Store credit vs refund policies

### Dummy Customer Order Data
A CSV file containing mock customer order data used by the Tracking Agent. This data includes:
- Customer IDs
- Order IDs
- Order dates
- Order status (processing, shipped, delivered)


This data is accessed through the FastAPI endpoint to provide order status information when customers make tracking-related queries.
