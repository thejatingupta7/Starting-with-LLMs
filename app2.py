import streamlit as st
import traceback
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler

# Import from your utils
from langchain_utils import load_embedding_model, load_vector_store, load_qa_chain

# ------------- Streamlit + LangChain Token Handler -------------
class StreamlitStreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(f"**Response:** {self.text}▌")  # typing effect

# ------------- Streamlit Page Setup -------------
def configure_page():
    st.set_page_config(
        page_title="CA-ThinkFlow",
        page_icon="💰",
        layout="wide"
    )

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

# ------------- Setup LangChain LLM and QA Chain -------------
def setup_llm_and_chain(stream_handler):
    try:
        embedding_model = load_embedding_model("all-MiniLM-L6-v2")
        retriever = load_vector_store("vectorstore", embedding_model)

        prompt_template = PromptTemplate(
            template="""
            You are a financial expert specializing in detailed analysis of financial statements and performing a wide range of data-driven financial tasks. 

            Context: {context}
            Question: {question}
            Answer:
            """,
            input_variables=["context", "question"]
        )

        llm = Ollama(
            model="llama3.1:8b",
            temperature=0.7,
            # streaming=True,
            callbacks=[stream_handler],
            verbose=True
        )

        chain = load_qa_chain(retriever, llm, prompt_template)
        return chain
    except Exception as e:
        st.error(f"Error setting up LLM and Chain: {e}")
        st.error(traceback.format_exc())
        return None

# ------------- Main App Logic -------------
def main():
    configure_page()
    add_custom_css()

    st.title("CA-ThinkFlow 🪙💰💱")
    st.subheader("Your AI Financial Consultant")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # --- Predefined financial query buttons ---
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

    # --- Stream LLM Response ---
    if user_query:
        st.session_state['history'].append({"user": user_query, "response": ""})
        with st.spinner("Analyzing your query..."):
            response_container = st.empty()  # placeholder for streaming response
            stream_handler = StreamlitStreamHandler(response_container)
            chain = setup_llm_and_chain(stream_handler)

            if chain:
                try:
                    chain({"query": user_query})  # Streamed output gets handled live
                    st.session_state['history'][-1]["response"] = stream_handler.text
                except Exception as e:
                    st.error("Something went wrong during streaming.")
                    st.error(traceback.format_exc())

    # --- Show Sidebar History ---
    with st.sidebar:
        st.header("Conversation History")
        for entry in reversed(st.session_state['history'][-5:]):
            st.markdown(f"*Q:* {entry['user']}")
            st.markdown(f"*A:* {entry['response']}")
            st.markdown("---")

if __name__ == "__main__":
    main()
