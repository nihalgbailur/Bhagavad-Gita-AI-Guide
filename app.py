import streamlit as st
from langchain.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from config import MODEL_CONFIG, API_CONFIG
import requests.exceptions

# Configure page settings
st.set_page_config(
    page_title="Bhagavad Gita AI Guide",
    page_icon="🕉️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .sanskrit {
        font-family: 'Sanskrit Text', serif;
        font-size: 1.2em;
        color: #FF4B4B;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin: 10px 0;
    }
    .translation {
        color: #262730;
        padding: 15px;
        border-left: 3px solid #FF4B4B;
        margin: 10px 0;
    }
    .example {
        background-color: #e1e5ea;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stMarkdown {
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def initialize_llm():
    """Initialize the Ollama LLM and conversation chain"""
    try:
        system_prompt = """You are a knowledgeable Bhagavad Gita guide powered by the Deepseek model. 
        When users ask about specific chapters and verses:
        1. First provide the Sanskrit verse with proper formatting
        2. Then provide the English transliteration
        3. Follow with a clear translation
        4. Finally, give a modern-day example or application
        5. If the verse number isn't specified, provide a summary of the chapter
        Format your response using HTML-like tags for styling:
        <sanskrit>Sanskrit text</sanskrit>
        <transliteration>Transliterated text</transliteration>
        <translation>English translation</translation>
        <example>Modern example</example>"""
        
        llm = Ollama(
            model=MODEL_CONFIG["name"],
            temperature=MODEL_CONFIG["temperature"],
            base_url=API_CONFIG["ollama_base_url"],
            stop=["Human:", "Assistant:"],
            system=system_prompt
        )
        memory = ConversationBufferMemory(
            return_messages=True,
            human_prefix="Seeker",
            ai_prefix="Guide"
        )
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=True
        )
        return conversation
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to Ollama. Please ensure Ollama is running locally.")
        return None
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        return None

# Page header with decorative elements
st.markdown("# 🕉️ Bhagavad Gita AI Guide")
st.markdown("### Timeless Wisdom for Modern Life")

# Sidebar with chapter information
with st.sidebar:
    st.markdown("### Bhagavad Gita Chapters")
    st.markdown("""
    1. Arjuna Visada Yoga
    2. Sankhya Yoga
    3. Karma Yoga
    4. Jnana Yoga
    5. Karma Sanyasa Yoga
    6. Dhyana Yoga
    7. Jnana Vijnana Yoga
    8. Aksara Brahma Yoga
    9. Raja Vidya Yoga
    10. Vibhuti Yoga
    11. Visvarupa Darsana Yoga
    12. Bhakti Yoga
    13. Ksetra Ksetrajna Yoga
    14. Gunatraya Vibhaga Yoga
    15. Purusottama Yoga
    16. Daivasura Sampad Vibhaga Yoga
    17. Sraddhatraya Vibhaga Yoga
    18. Moksa Sanyasa Yoga
    """)
    
    st.markdown("### How to Ask")
    st.markdown("""
    - For specific verse: "Chapter 2, Verse 47"
    - For chapter summary: "Tell me about Chapter 4"
    - For topic search: "What does Gita say about karma?"
    """)

# Initialize conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = initialize_llm()

# Display chat messages with enhanced formatting
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if message["role"] == "assistant":
            # Parse and format the response
            if "<sanskrit>" in content:
                content = content.replace("<sanskrit>", "<div class='sanskrit'>")
                content = content.replace("</sanskrit>", "</div>")
                content = content.replace("<transliteration>", "<div class='translation'>")
                content = content.replace("</transliteration>", "</div>")
                content = content.replace("<translation>", "<div class='translation'>")
                content = content.replace("</translation>", "</div>")
                content = content.replace("<example>", "<div class='example'>📝 Modern Application:<br>")
                content = content.replace("</example>", "</div>")
                st.markdown(content, unsafe_allow_html=True)
            else:
                st.markdown(content)
        else:
            st.markdown(content)

# Chat input with placeholder
if prompt := st.chat_input("Ask about a chapter, verse, or concept from the Bhagavad Gita..."):
    if st.session_state.conversation is None:
        st.error("Cannot process request - Connection not established")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response with error handling
        with st.chat_message("assistant"):
            with st.spinner("Contemplating... 🕉️"):
                try:
                    response = st.session_state.conversation.predict(input=prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    # Parse and format the response
                    if "<sanskrit>" in response:
                        response = response.replace("<sanskrit>", "<div class='sanskrit'>")
                        response = response.replace("</sanskrit>", "</div>")
                        response = response.replace("<transliteration>", "<div class='translation'>")
                        response = response.replace("</transliteration>", "</div>")
                        response = response.replace("<translation>", "<div class='translation'>")
                        response = response.replace("</translation>", "</div>")
                        response = response.replace("<example>", "<div class='example'>📝 Modern Application:<br>")
                        response = response.replace("</example>", "</div>")
                        st.markdown(response, unsafe_allow_html=True)
                    else:
                        st.markdown(response)
                except Exception as e:
                    error_message = f"❌ Failed to generate response: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message}) 