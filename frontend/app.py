import streamlit as st
import requests
import re
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(
    page_title="DevOps AI Assistant Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bulletproof Clean URL Extractor
def clean_url(url_str: str) -> str:
    if not url_str:
        return ""
    match = re.search(r'https?://[a-zA-Z0-9.\-_:]+', url_str)
    if match:
        return match.group(0)
    return "http://127.0.0.1:8000"

BASE_HOST = clean_url("http://127.0.0.1:8000")

def check_backend_health() -> bool:
    """Checks if FastAPI backend server is alive."""
    try:
        res = requests.get(f"{BASE_HOST}/", timeout=2)
        return res.status_code == 200
    except Exception:
        return False

def sanitize_mermaid(mermaid_code: str) -> str:
    """Sanitizes LLM generated Mermaid code to prevent parsing errors."""
    clean = re.sub(r'```mermaid', '', mermaid_code, flags=re.IGNORECASE)
    clean = re.sub(r'```', '', clean).strip()
    
    sanitized_lines = []
    for line in clean.splitlines():
        line_str = line.strip()
        if not line_str:
            continue
            
        line_str = re.sub(r'\[\s*([^"\]]+?)\s*\]', r'["\1"]', line_str)
        line_str = line_str.replace('[""', '["').replace('""]', '"]')
        
        sanitized_lines.append(line_str)
        
    return "\n".join(sanitized_lines)

# 2. Mermaid Diagram Visual Renderer
def render_mermaid(mermaid_code: str):
    clean_code = sanitize_mermaid(mermaid_code)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {{
            background-color: #0b0f19;
            margin: 0;
            padding: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .mermaid {{
            background-color: #0b0f19;
            width: 100%;
        }}
      </style>
      <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true, 
            theme: 'dark',
            securityLevel: 'loose',
            flowchart: {{ useMaxWidth: true, htmlLabels: true }}
        }});
      </script>
    </head>
    <body>
      <pre class="mermaid">
{clean_code}
      </pre>
    </body>
    </html>
    """
    components.html(html_code, height=520, scrolling=True)

# 3. Advanced Custom CSS Styling (Modern SaaS Glassmorphism)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    /* Header Card Banner */
    .header-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(12px);
    }
    .header-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .header-sub {
        color: #94a3b8;
        font-size: 1.05rem;
    }

    /* Input Field Container */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background-color: #1e293b !important;
    }
    
    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    div[data-testid="stMetricValue"] {
        font-weight: 700;
        color: #38bdf8 !important;
    }

    /* Styled Custom Tab Bar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #111827;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0px 16px;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }

    /* Buttons Styling */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border: none;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# 4. Sidebar Configuration & Live Health Check
st.sidebar.markdown("### ⚡ DevOps AI Control")
st.sidebar.caption("Powered by Local Models (Qwen 2.5 Coder)")

st.sidebar.markdown("---")
st.sidebar.markdown("#### 📡 System Status")

is_healthy = check_backend_health()
if is_healthy:
    st.sidebar.success("🟢 Backend API: Online")
else:
    st.sidebar.error("🔴 Backend API: Offline")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Pro Tip**: Enter any public GitHub repo URL to generate architecture diagrams, SAST security reports, and deployment manifests.")

# 5. Header Area Banner
st.markdown("""
    <div class="header-banner">
        <div class="header-title">⚡ DevOps AI Assistant Platform</div>
        <div class="header-sub">Automated Repository Analysis, Architecture Flowcharts, Security Audits & CI/CD Pipelines</div>
    </div>
""", unsafe_allow_html=True)

# 6. Input Section
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        repo_url_input = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/expressjs/express",
            help="Enter any public GitHub repository link"
        )
    with col2:
        st.write("##")
        analyze_btn = st.button("🚀 Process Repository", use_container_width=True, type="primary")

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

clean_repo_url = repo_url_input.strip()

if analyze_btn or clean_repo_url:
    if not clean_repo_url:
        st.error("Please enter a valid GitHub Repository URL!")
    else:
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏗️ Architecture", 
            "🛡️ Security SAST", 
            "💬 Code Chat",
            "📄 Documentation",
            "☁️ Cloud Strategy",
            "⚙️ DevOps Manifests"
        ])

        # TAB 1: ARCHITECTURE
        with tab1:
            st.subheader("Project Architecture & Design Patterns")
            if analyze_btn:
                with st.spinner("Cloning Repo & Analyzing Architecture via Local AI..."):
                    try:
                        target_endpoint = f"{BASE_HOST}/api/v1/analyze-architecture"
                        res = requests.post(
                            target_endpoint,
                            json={"repo_url": clean_repo_url},
                            timeout=180
                        )
                        if res.status_code == 200:
                            data = res.json()
                            summary = data.get("summary", {})
                            report = data.get("architecture_report", "")

                            m1, m2, m3 = st.columns(3)
                            m1.metric("Parsed Code Files", summary.get("parsed_files", 0))
                            m2.metric("Total Lines of Code", f"{summary.get('total_lines', 0):,}")
                            m3.metric("Parsing Status", "Ready", delta="100% Success")

                            st.markdown("---")

                            mermaid_match = re.search(r'```mermaid\s*(.*?)\s*```', report, re.DOTALL)
                            if mermaid_match:
                                mermaid_code = mermaid_match.group(1).strip()
                                st.markdown("### 📊 Interactive Flowchart Diagram")
                                render_mermaid(mermaid_code)
                            
                            st.markdown("### 📋 Detailed Architecture Breakdown")
                            st.markdown(report)
                        else:
                            st.error(f"Error from backend: {res.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Failed to connect to backend server: {str(e)}")
            else:
                st.info("Click 'Process Repository' to generate Architecture Analysis.")

        # TAB 2: SECURITY & SAST
        with tab2:
            st.subheader("OWASP Vulnerabilities & SAST Security Audit")
            if analyze_btn:
                with st.spinner("Scanning Codebase for Bugs & Security Risks..."):
                    try:
                        target_endpoint = f"{BASE_HOST}/api/v1/scan-security"
                        res = requests.post(
                            target_endpoint,
                            json={"repo_url": clean_repo_url},
                            timeout=180
                        )
                        if res.status_code == 200:
                            sec_data = res.json()
                            sec_report = sec_data.get("security_audit_report", "")
                            st.markdown(sec_report)
                        else:
                            st.error(f"Security Scan Failed: {res.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Failed to connect to backend server: {str(e)}")
            else:
                st.info("Click 'Process Repository' to run Security SAST Audit.")

        # TAB 3: CODEBASE Q&A / CHAT
        with tab3:
            st.subheader("💬 Ask Anything About This Codebase")
            st.caption("Ask questions about functions, configuration, logic, or bug locations.")

            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            user_question = st.chat_input("e.g., Where is the main configuration loaded or how does authentication work?")
            
            if user_question:
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                with st.chat_message("user"):
                    st.markdown(user_question)

                with st.chat_message("assistant"):
                    with st.spinner("Searching codebase & generating AI response..."):
                        try:
                            target_endpoint = f"{BASE_HOST}/api/v1/chat-codebase"
                            res = requests.post(
                                target_endpoint,
                                json={
                                    "repo_url": clean_repo_url,
                                    "question": user_question
                                },
                                timeout=120
                            )
                            if res.status_code == 200:
                                answer = res.json().get("answer", "No answer received.")
                                st.markdown(answer)
                                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                            else:
                                st.error(f"Chat failed: {res.json().get('detail')}")
                        except Exception as e:
                            st.error(f"Failed to reach backend: {str(e)}")

        # TAB 4: AUTO-DOCUMENTATION
        with tab4:
            st.subheader("📄 Automated README.md Generator")
            st.caption("Auto-generate a comprehensive production-grade README documentation for this repository.")

            if analyze_btn:
                with st.spinner("Analyzing codebase and drafting README.md documentation..."):
                    try:
                        target_endpoint = f"{BASE_HOST}/api/v1/generate-docs"
                        res = requests.post(
                            target_endpoint,
                            json={"repo_url": clean_repo_url},
                            timeout=180
                        )
                        if res.status_code == 200:
                            doc_data = res.json()
                            readme_md = doc_data.get("readme_md", "")

                            st.download_button(
                                label="📥 Download README.md File",
                                data=readme_md,
                                file_name="README.md",
                                mime="text/markdown"
                            )

                            st.markdown("---")
                            st.markdown(readme_md)
                        else:
                            st.error(f"Documentation Generation Failed: {res.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Failed to connect to backend server: {str(e)}")
            else:
                st.info("Click 'Process Repository' to generate README.md Documentation.")

        # TAB 5: CLOUD & COST OPTIMIZER
        with tab5:
            st.subheader("☁️ Cloud Hosting & Cost Optimization Advisor")
            st.caption("AI-driven cloud infrastructure recommendations, server sizing, and monthly cost reduction strategy.")

            if analyze_btn:
                with st.spinner("Evaluating codebase for optimal cloud architecture and cost savings..."):
                    try:
                        target_endpoint = f"{BASE_HOST}/api/v1/cloud-optimizer"
                        res = requests.post(
                            target_endpoint,
                            json={"repo_url": clean_repo_url},
                            timeout=180
                        )
                        if res.status_code == 200:
                            cloud_data = res.json()
                            cloud_report = cloud_data.get("cloud_report", "")
                            st.markdown(cloud_report)
                        else:
                            st.error(f"Cloud Optimization Failed: {res.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Failed to connect to backend server: {str(e)}")
            else:
                st.info("Click 'Process Repository' to generate Cloud Strategy Report.")

        # TAB 6: DEVOPS & CI/CD GENERATOR
        with tab6:
            st.subheader("⚙️ Automated Docker, Kubernetes & CI/CD Generator")
            st.caption("Auto-generate Dockerfiles, docker-compose setups, Kubernetes deployment manifests, and GitHub Actions CI/CD pipelines.")

            if analyze_btn:
                with st.spinner("Generating production-ready Docker, K8s, and GitHub Actions workflows..."):
                    try:
                        target_endpoint = f"{BASE_HOST}/api/v1/devops-generator"
                        res = requests.post(
                            target_endpoint,
                            json={"repo_url": clean_repo_url},
                            timeout=180
                        )
                        if res.status_code == 200:
                            devops_data = res.json()
                            devops_report = devops_data.get("devops_report", "")
                            
                            st.download_button(
                                label="📥 Download DevOps Manifests (.md)",
                                data=devops_report,
                                file_name="devops_manifests.md",
                                mime="text/markdown"
                            )

                            st.markdown("---")
                            st.markdown(devops_report)
                        else:
                            st.error(f"DevOps Generation Failed: {res.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Failed to connect to backend server: {str(e)}")
            else:
                st.info("Click 'Process Repository' to auto-generate DevOps & CI/CD Pipeline files.")