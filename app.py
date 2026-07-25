import os
import sys
import streamlit as st

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Safe import with UI error reporting (Traceback redaction bypass)
try:
    from backend.app.services.ingestor import RepositoryIngestor
    from backend.app.services.llm_service import AIService
    from backend.app.services.rag_service import CodebaseRAG
except Exception as e:
    st.error(f"⚠️ Import Error while loading backend services: {e}")
    st.info("Ensure all requirements are installed and backend folder structure is correct.")
    st.stop()

# Page Configuration
st.set_page_config(page_title="DevPulse - DevOps AI Assistant", page_icon="⚡", layout="wide")

st.title("⚡ DevOps AI Assistant Platform")
st.caption("Automated Repository Analysis, Architecture Flowcharts, Security Audits & CI/CD Pipelines")

# Initialize AI Service
ai_service = AIService()

# Session State Initializations
if "repo_data" not in st.session_state:
    st.session_state.repo_data = None
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None

# Sidebar Status
with st.sidebar:
    st.header("⚡ DevPulse Control")
    st.success("System Status: Online (Groq Cloud API Active)")
    st.info("💡 **Tip:** Public GitHub Repository URL enter karke Process par click karo.")

# Repository Input Section
repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/username/repository.git")

if st.button("🚀 Process Repository", type="primary"):
    if not repo_url:
        st.warning("Please enter a valid GitHub repository URL.")
    else:
        with st.spinner("Cloning and processing repository codebase..."):
            try:
                ingestor = RepositoryIngestor(repo_url)
                files = ingestor.process_repository()
                summary = ingestor.get_summary()
                
                # Store in session state
                st.session_state.repo_data = {"files": files, "summary": summary}
                
                # Build RAG Engine
                rag = CodebaseRAG()
                rag.index_repository(files)
                st.session_state.rag_engine = rag
                
                st.success(f"Successfully processed repository! Total files: {len(files)}")
            except Exception as e:
                st.error(f"Error processing repository: {str(e)}")

# UI Tabs for Features
if st.session_state.repo_data:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏗️ Architecture", 
        "🛡️ Security SAST", 
        "💬 Code Chat", 
        "📄 Documentation", 
        "☁️ Cloud Strategy", 
        "⚙️ DevOps Manifests"
    ])

    files = st.session_state.repo_data["files"]
    summary = st.session_state.repo_data["summary"]

    with tab1:
        st.subheader("Project Architecture & Design Patterns")
        if st.button("Generate Architecture Diagram"):
            with st.spinner("Analyzing architecture and generating Mermaid flowchart..."):
                arch_res = ai_service.analyze_architecture(summary)
                st.markdown(arch_res)

    with tab2:
        st.subheader("SAST Vulnerability Audit & Security Review")
        if st.button("Run Security Audit"):
            with st.spinner("Auditing codebase for OWASP vulnerabilities..."):
                sec_res = ai_service.scan_repository_security(files)
                st.markdown(sec_res)

    with tab3:
        st.subheader("Interactive Codebase Q&A (RAG Engine)")
        user_query = st.text_input("Ask anything about this repo:")
        if user_query and st.session_state.rag_engine:
            with st.spinner("Retrieving relevant code and generating answer..."):
                answer = st.session_state.rag_engine.query(user_query, ai_service)
                st.markdown(answer)

    with tab4:
        st.subheader("Automated README.md Generator")
        if st.button("Generate Documentation"):
            with st.spinner("Drafting production README.md..."):
                doc_res = ai_service.generate_readme_docs(files)
                st.markdown(doc_res)

    with tab5:
        st.subheader("Cloud Infrastructure & Cost Optimization")
        if st.button("Analyze Cloud Strategy"):
            with st.spinner("Calculating optimal deployment strategy..."):
                cloud_res = ai_service.recommend_cloud_optimization(files)
                st.markdown(cloud_res)

    with tab6:
        st.subheader("Docker, Kubernetes & CI/CD Pipeline Generator")
        if st.button("Generate DevOps Manifests"):
            with st.spinner("Generating Dockerfile, K8s & GitHub Actions..."):
                devops_res = ai_service.generate_devops_manifests(files)
                st.markdown(devops_res)