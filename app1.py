import streamlit as st
import traceback
from ollama import chat

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="LegalThinkFlow",
        page_icon="⚖️",
        layout="wide"
    )

def get_response_stream(query):
    """
    Stream the response from the model for the given query
    """
    try:
        # System prompt to guide the model's behavior
        system_prompt = {
            'role': 'system',
            'content': """
                You are a Legal Expert specializing in Indian law, providing precise and reliable legal guidance.

                ⚖️ Instructions:
                - Align all responses strictly with Indian legal provisions and case laws.
                - If answer options are given, respond only from those options.
                - Do not include unnecessary explanations or opinions—stick to legal facts.

                Reference sources include:
                - Statutory text
                - Case law
                - Legal documents

                If the question is not legal in nature, politely refuse and state that you only assist with legal queries.

                📝 Format your reply as:
                - Question: [Restate briefly]
                - Answer: [Your structured legal response]
                """
            }

        messages = [
            system_prompt,
            {'role': 'user', 'content': query}
        ]

        stream = chat(
            model='llama3.2:1b', # smaller models doesnt follow Sys. prompt well, Try going for llama3.2:3b or higher, as per your capacity of system 
            messages=messages,
            stream=True,
        )
        response = ""
        for chunk in stream:
            content = chunk['message']['content']
            response += content
            yield content
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        st.error(error_msg)
        st.error(traceback.format_exc())
        yield "Sorry, I encountered an issue processing your query."


def setup_llm():
    """Placeholder for LLM setup"""
    return True

def add_custom_css():
    """Add custom CSS for enhanced UI"""
    st.markdown("""
    <style>
    .stButton button {
        width: 220px;
        height: 60px;
        font-size: 16px;
        border-radius: 10px;
        background-color: #1f2e45;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #2e3e5e;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    configure_page()
    add_custom_css()
    
    st.title("⚖️ LegalThinkFlow")
    st.subheader("Your AI Legal Assistant")

    llm = setup_llm()
    
    if not llm:
        st.error("Failed to initialize the AI assistant. Please check your configurations.")
        return

    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Consumer Complaint Rights"):
            st.session_state['user_query'] = "What are my rights when filing a consumer complaint in India?"

    with col2:
        if st.button("Contract Disputes"):
            st.session_state['user_query'] = "What legal steps can I take if someone breaches a contract?"

    with col3:
        if st.button("Cyber Crime Reporting"):
            st.session_state['user_query'] = "How can I report a cyber crime in India?"

    with col4:
        if st.button("Legal Heirship Process"):
            st.session_state['user_query'] = "What is the process to claim legal heirship for property in India?"

    user_query = st.text_input(
        "Enter your legal question:",
        value=st.session_state.get('user_query', "")
    )
    
    if user_query:
        st.session_state['history'].append({"user": user_query, "response": ""})
        with st.spinner('Analyzing your legal query...'):
            response_container = st.empty()
            response = ""
            for chunk in get_response_stream(user_query):
                response += chunk
                response_container.markdown(f"**Response:** {response}")
            st.session_state['history'][-1]["response"] = response

    with st.sidebar:
        st.header("🕰️ Conversation History")
        for entry in reversed(st.session_state['history'][-5:]):
            st.markdown(f"*Q:* {entry['user']}")
            st.markdown(f"*A:* {entry['response']}")
            st.markdown("---")

if __name__ == "__main__":
    main()
