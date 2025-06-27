import streamlit as st
import traceback
import os

from ollama import chat
from langchain_utils import (
    load_embedding_model,
    load_vector_store,
    load_qa_chain,   # still used if you want to do retrieval-based answers
)
from langchain_core.prompts import PromptTemplate

# --- Streamlit + Chat Streaming Handler (no LangChain callbacks) ---
def get_response_stream(query):
    """
    Stream the response from ollama.chat for the given query.
    """
    try:
        stream = chat(
            model='llama3.1:8b',
            messages=[{'role': 'user', 'content': query}],
            stream=True,
        )
        for chunk in stream:
            # each chunk is a dict like {'message': {'content': '…'}}
            content = chunk['message']['content']
            yield content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error(traceback.format_exc())
        yield "[Error generating response]"

# --- Page setup and styling ---
def configure_page():
    st.set_page_config(page_title="CA-ThinkFlow", page_icon="💰", layout="wide")

def add_custom_css():
    st.markdown("""
    <style>
    .stButton button {
        width: 200px;
        height: 60px;
        font-size: 16px;
        border-radius: 10px;
        background-color: #2C3E50;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #34495E;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- (Optional) retrieval-based setup if you still want context from your PDFs ---
def setup_retrieval_chain():
    embedding_model = load_embedding_model("all-MiniLM-L6-v2")
    retriever = load_vector_store("vectorstore", embedding_model)
    prompt = PromptTemplate(
        template="""
        You are a financial expert. Use the following context to answer.

        Context: {context}
        Question: {question}
        Answer:
        """,
        input_variables=["context", "question"]
    )
    return load_qa_chain(retriever, None, prompt)  # llm=None since we call chat() ourselves

# --- Main App ---
def main():
    configure_page()
    add_custom_css()
    st.title("CA-ThinkFlow 🪙💰💱")
    st.subheader("Your AI Financial Consultant")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Predefined buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Tax Benefits - Rental Income"):
            st.session_state['user_query'] = "What are the tax benefits for rental income in India?"
    with col2:
        if st.button("Property Tax Resolution"):
            st.session_state['user_query'] = "What are the tax implications when selling a property in India?"
    with col3:
        if st.button("Employment Tax"):
            st.session_state['user_query'] = "How does TDS work on salary income in India?"
    with col4:
        if st.button("ITR Filing Process"):
            st.session_state['user_query'] = "What is the process to file an Income Tax Return (ITR) in India?"

    user_query = st.text_input(
        "Enter your financial question:",
        value=st.session_state.get('user_query', "")
    )

    if user_query:
        st.session_state['history'].append({"user": user_query, "response": ""})
        response_container = st.empty()
        full_response = ""
        with st.spinner("Analyzing your query…"):
            for chunk in get_response_stream(user_query):
                full_response += chunk
                response_container.markdown(f"**Response:** {full_response}▌")
        # save final
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
