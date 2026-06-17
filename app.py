import streamlit as st
from project.services.bedrock_service import BedrockService
from project.components.ui_components import sidebar_components, artifact_display, header_component, footer_component

# Page Configuration
st.set_page_config(
    page_title="DevOps Copilot // Nothing OS Edition",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Nothing OS Theme Implementation
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Silkscreen&display=swap');

    :root {
        --nothing-red: #FF0031;
        --nothing-black: #000000;
        --nothing-white: #FFFFFF;
        --nothing-grey: #111111;
        --nothing-border: #333333;
    }

    /* Main Container */
    .stApp {
        background-color: var(--nothing-black);
        color: var(--nothing-white);
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Dot Matrix Title Style */
    .dot-matrix {
        font-family: 'Silkscreen', cursive;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--nothing-white);
    }

    .nothing-title {
        font-family: 'Silkscreen', cursive;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        color: var(--nothing-white);
    }

    .nothing-subtitle {
        color: #888888;
        font-weight: 300;
        letter-spacing: 1px;
        margin-bottom: 3rem;
    }

    /* Cards */
    .stMetric, .stAlert, div[data-testid="stExpander"], .nothing-card {
        background-color: var(--nothing-grey) !important;
        border: 1px solid var(--nothing-border) !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--nothing-white) !important;
        color: var(--nothing-black) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: var(--nothing-red) !important;
        color: var(--nothing-white) !important;
        transform: scale(1.02);
    }

    /* Text Area */
    .stTextArea>div>div>textarea {
        background-color: var(--nothing-grey) !important;
        color: var(--nothing-white) !important;
        border: 1px solid var(--nothing-border) !important;
        border-radius: 15px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 15px !important;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: var(--nothing-red) !important;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: var(--nothing-black) !important;
        border-right: 1px solid var(--nothing-border) !important;
    }

    /* Sidebar button overrides */
    section[data-testid="stSidebar"] .stButton>button {
        background-color: transparent !important;
        color: #888888 !important;
        border: 1px solid var(--nothing-border) !important;
        text-align: left !important;
        padding: 0.5rem 1rem !important;
        margin-bottom: 5px !important;
    }

    section[data-testid="stSidebar"] .stButton>button:hover {
        border-color: var(--nothing-red) !important;
        color: var(--nothing-white) !important;
    }

    /* Progress/Spinner color */
    .stSpinner > div > div {
        border-top-color: var(--nothing-red) !important;
    }

    /* Code Block Styling */
    code {
        color: var(--nothing-red) !important;
        background-color: #1a1a1a !important;
    }
    
    pre {
        border: 1px solid var(--nothing-border) !important;
        border-radius: 12px !important;
        background-color: #080808 !important;
    }

    /* Success box override */
    .stSuccess {
        background-color: #051005 !important;
        border: 1px solid #004400 !important;
        color: #00ff00 !important;
    }

    /* Info box override */
    .stInfo {
        background-color: #080808 !important;
        border: 1px solid var(--nothing-border) !important;
        color: #aaaaaa !important;
    }

    </style>
""", unsafe_allow_html=True)

# Initialize Service
@st.cache_resource
def get_service():
    return BedrockService()

bedrock_service = get_service()

def main():
    # Sidebar
    template_prompt = sidebar_components()
    
    # Header
    header_component()
    
    # Use session state for input
    if 'prompt_input' not in st.session_state:
        st.session_state.prompt_input = ""
        
    if template_prompt:
        st.session_state.prompt_input = template_prompt

    # Input Section
    with st.container():
        user_input = st.text_area(
            "INPUT_REQUIREMENTS",
            value=st.session_state.prompt_input,
            placeholder="Describe your architecture... (e.g., AWS VPC with EKS and a Jenkins pipeline)",
            height=150,
            key="main_input",
            label_visibility="collapsed"
        )
        
        col1, col2, _ = st.columns([1, 1, 4])
        
        st.session_state.prompt_input = user_input

        with col1:
            generate_clicked = st.button("EXECUTE_GENERATION")
        with col2:
            clear_clicked = st.button("CLEAR_LOGS")
        
        if clear_clicked:
            st.session_state.prompt_input = ""
            if 'result' in st.session_state:
                del st.session_state.result
            st.rerun()

    # Generator Logic
    if generate_clicked and user_input:
        with st.spinner("PROCESS // ANALYZING ARCHITECTURE..."):
            result = bedrock_service.generate_artifact(user_input)
            st.session_state.result = result
            
    # Display Result
    if 'result' in st.session_state:
        artifact_display(st.session_state.result)
    else:
        # Initial View
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="dot-matrix">01 // IAC</div>', unsafe_allow_html=True)
            st.markdown("Automated Terraform scripting for cloud infrastructure.")
        with c2:
            st.markdown('<div class="dot-matrix">02 // CI-CD</div>', unsafe_allow_html=True)
            st.markdown("Pipeline orchestration for GitHub, GitLab, and Jenkins.")
        with c3:
            st.markdown('<div class="dot-matrix">03 // SEC</div>', unsafe_allow_html=True)
            st.markdown("Embedded DevSecOps compliance scanning.")

    footer_component()

if __name__ == "__main__":
    main()
