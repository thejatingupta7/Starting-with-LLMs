import streamlit as st
import traceback

from ollama import chat
from langchain_utils import (
    load_embedding_model,
    load_vector_store,
)
from langchain_core.prompts import PromptTemplate

# --- RAG Setup ---
embedding_model = load_embedding_model("all-MiniLM-L6-v2")
retriever = load_vector_store("vectorstore", embedding_model)

rag_prompt_template = PromptTemplate(
    template="""
You are a legal expert in Indian Law and Jurisdiction. Use the following context to answer the legal question. 
If the question is not legal, respond that you only assist with legal queries.

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"]
)

# --- Streamlit + Streaming RAG Logic ---
def get_rag_response_stream(query):
    try:
        # Step 1: Retrieve documents
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([doc.page_content for doc in docs[:4]]) or "No relevant documents found."

        # Step 2: Format prompt with context
        formatted_prompt = rag_prompt_template.format(context=context, question=query)

        # Step 3: Stream from model
        stream = chat(
            model='llama3.2:1b',
            messages=[{'role': 'user', 'content': formatted_prompt}],
            stream=True,
        )
        for chunk in stream:
            content = chunk['message']['content']
            yield content

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error(traceback.format_exc())
        yield "[Error generating response]"

# --- Page setup and styling ---
def configure_page():
    st.set_page_config(page_title="LegalThinkFlow", page_icon="⚖️", layout="wide")

def add_custom_css():
    st.markdown("""
    <style>
    .stButton button {
        width: 220px;
        height: 60px;
        font-size: 16px;
        border-radius: 10px;
        background-color: #1E1E2F;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #2C2C3A;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Main App ---
def main():
    configure_page()
    add_custom_css()
    st.title("LegalThinkFlow ⚖️📜")
    st.subheader("Your AI Assistant for Indian Legal Queries")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Predefined legal questions
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Property Disputes"):
            st.session_state['user_query'] = "What are common legal remedies for property disputes in India?"
    with col2:
        if st.button("Marriage & Divorce Laws"):
            st.session_state['user_query'] = "What is the legal process for divorce under Hindu Marriage Act?"
    with col3:
        if st.button("Contract Enforcement"):
            st.session_state['user_query'] = "How are contracts legally enforced in India?"
    with col4:
        if st.button("Consumer Rights"):
            st.session_state['user_query'] = "What rights does a consumer have under the Consumer Protection Act?"

    user_query = st.text_input(
        "Enter your Legal Query:",
        value=st.session_state.get('user_query', "")
    )

    if user_query:
        st.session_state['history'].append({"user": user_query, "response": ""})
        response_container = st.empty()
        full_response = ""
        with st.spinner("Retrieving legal context and generating response..."):
            for chunk in get_rag_response_stream(user_query):
                full_response += chunk
                response_container.markdown(f"**Response:** {full_response}▌")
        st.session_state['history'][-1]["response"] = full_response

    # Sidebar history
    with st.sidebar:
        st.header("Conversation History")
        for entry in reversed(st.session_state['history'][-5:]):
            st.markdown(f"*Q:* {entry['user']}")
            st.markdown(f"*A:* {entry['response']}")
            st.markdown("---")

if __name__ == "__main__":
    main()
