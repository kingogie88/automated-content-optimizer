import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Automated Content Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        .reportview-container {
            margin-top: -2em;
        }
        .css-1d391kg {
            padding-top: 1rem;
        }
        .stProgress .st-bo {
            background-color: #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # Sidebar
    st.sidebar.title("🚀 Content Optimizer")
    
    # User authentication status
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_main_interface()

def show_login_page():
    """Display the login interface"""
    st.title("Welcome to Content Optimizer")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            # TODO: Implement actual authentication
            if email and password:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Please enter valid credentials")
    
    st.markdown("---")
    st.markdown("Don't have an account? [Sign up here](https://contentoptimizer.ai/signup)")

def show_main_interface():
    """Display the main application interface"""
    # Sidebar navigation
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "SEO Optimizer", "GEO Optimizer", "Analytics", "Settings"]
    )
    
    # User info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### User: Pro Plan")
    st.sidebar.markdown("#### Optimizations left: 487/500")
    
    # Main content area
    if page == "Dashboard":
        show_dashboard()
    elif page == "SEO Optimizer":
        show_seo_optimizer()
    elif page == "GEO Optimizer":
        show_geo_optimizer()
    elif page == "Analytics":
        show_analytics()
    elif page == "Settings":
        show_settings()

def show_dashboard():
    """Display the dashboard page"""
    st.title("Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Optimizations", "1,234", "+12%")
    with col2:
        st.metric("Avg. SEO Score", "87/100", "+5%")
    with col3:
        st.metric("Avg. GEO Score", "92/100", "+8%")
    with col4:
        st.metric("ROI Impact", "$12,450", "+15%")
    
    # Recent optimizations
    st.subheader("Recent Optimizations")
    st.dataframe({
        "Date": ["2024-01-15", "2024-01-14", "2024-01-13"],
        "Content": ["Blog Post", "Landing Page", "Product Description"],
        "SEO Score": ["92/100", "88/100", "95/100"],
        "GEO Score": ["89/100", "94/100", "91/100"]
    })

def show_seo_optimizer():
    """Display the SEO optimization interface"""
    st.title("SEO Optimizer")
    
    # Content input
    content_type = st.selectbox(
        "Content Type",
        ["Text Input", "URL", "File Upload"]
    )
    
    if content_type == "Text Input":
        content = st.text_area("Enter your content", height=200)
    elif content_type == "URL":
        content = st.text_input("Enter URL")
    else:
        content = st.file_uploader("Upload content file", type=["txt", "docx", "pdf"])
    
    # Optimization options
    st.subheader("Optimization Options")
    col1, col2 = st.columns(2)
    
    with col1:
        st.multiselect(
            "Target Search Engines",
            ["Google", "Bing", "DuckDuckGo"],
            ["Google"]
        )
    
    with col2:
        st.multiselect(
            "Optimization Goals",
            ["Keyword Optimization", "Technical SEO", "Content Structure", "Link Analysis"],
            ["Keyword Optimization"]
        )
    
    if st.button("Start SEO Optimization"):
        with st.spinner("Optimizing content..."):
            # TODO: Implement actual optimization
            st.success("Optimization complete!")

def show_geo_optimizer():
    """Display the GEO optimization interface"""
    st.title("GEO (Generative Engine Optimizer)")
    
    # Similar structure to SEO optimizer but with AI-specific options
    content = st.text_area("Enter your content", height=200)
    
    st.subheader("AI Platform Targeting")
    col1, col2 = st.columns(2)
    
    with col1:
        st.multiselect(
            "Target AI Platforms",
            ["ChatGPT", "Claude", "Gemini", "Voice Assistants"],
            ["ChatGPT"]
        )
    
    with col2:
        st.multiselect(
            "Optimization Goals",
            ["Context Enhancement", "Factual Accuracy", "Voice Search", "Featured Snippets"],
            ["Context Enhancement"]
        )
    
    if st.button("Start GEO Optimization"):
        with st.spinner("Optimizing for AI platforms..."):
            # TODO: Implement actual optimization
            st.success("AI optimization complete!")

def show_analytics():
    """Display the analytics page"""
    st.title("Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Start Date")
    with col2:
        st.date_input("End Date")
    
    # Placeholder for charts
    st.subheader("Performance Metrics")
    st.line_chart({"SEO Score": [85, 87, 92, 95, 89],
                   "GEO Score": [82, 88, 90, 93, 91]})

def show_settings():
    """Display the settings page"""
    st.title("Settings")
    
    # API Configuration
    st.subheader("API Configuration")
    st.text_input("OpenAI API Key", type="password")
    st.text_input("Anthropic API Key", type="password")
    
    # User Preferences
    st.subheader("User Preferences")
    st.checkbox("Enable email notifications")
    st.checkbox("Enable auto-optimization")
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

if __name__ == "__main__":
    main() 