import streamlit as st
import traceback
from ollama import chat

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="CA-ThinkFlow",
        page_icon="💰",
        layout="wide"
    )

def get_response_stream(query):
    """
    Stream the response from the model for the given query
    """
    try:
        # Stream the response from the model
        stream = chat(
            model='llama3.1:8b',  # Specify the model name
            messages=[{'role': 'user', 'content': query}],
            stream=True,
        )
        response = ""
        for chunk in stream:
            content = chunk['message']['content']
            response += content
            yield content  # Stream each chunk to the UI
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        st.error(error_msg)
        st.error(traceback.format_exc())
        yield "Sorry, I encountered an issue processing your query."

def setup_llm():
    """
    Placeholder for LLM setup (not needed for `ollama.chat`)
    """
    return True  # Return a dummy value to indicate successful setup

def add_custom_css():
    """Add custom CSS for enhanced UI"""
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

def main():
    configure_page()
    add_custom_css()
    
    st.title("CA-ThinkFlow ₹")
    st.subheader("Your AI Financial Consultant")
    
    llm = setup_llm()
    
    if not llm:
        st.error("Failed to initialize the AI assistant. Please check your configurations.")
        return
    
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    # Predefined query buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Tax Benefits - Rental Income"):
            st.session_state['user_query'] = "What are the tax benefits for rental income in India?"
    
    with col2:
        if st.button("Property Tax Resolution"):
            st.session_state['user_query'] = "What are the tax implications when selling a property in India?(in bullets simple expalin)"
    
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
        with st.spinner('Analyzing your query...'):
            response_container = st.empty()  # Placeholder for streaming response
            response = ""
            for chunk in get_response_stream(user_query):
                response += chunk
                response_container.markdown(f"**Response:** {response}")
            st.session_state['history'][-1]["response"] = response
    
    with st.sidebar:
        st.header("Conversation History")
        for entry in reversed(st.session_state['history'][-5:]):
            st.markdown(f"*Q:* {entry['user']}")
            st.markdown(f"*A:* {entry['response']}")
            st.markdown("---")

if __name__ == "__main__":
    main()
