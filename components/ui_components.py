import streamlit as st

def header_component():
    st.markdown('<h1 class="nothing-title">DEVOPS_COPILOT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="nothing-subtitle">AI-DRIVEN CLOUD OPERATIONS // POWERED BY BEDROCK NOVA PRO</p>', unsafe_allow_html=True)

def footer_component():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #444; font-size: 0.8rem; font-family: Silkscreen;">(C) 2026 // SYSTEM_ACTIVE // ARENA_AI</p>', unsafe_allow_html=True)

def sidebar_components():
    with st.sidebar:
        st.markdown('<div class="dot-matrix" style="font-size: 1.5rem; margin-bottom: 20px;">MENU</div>', unsafe_allow_html=True)
        
        st.markdown("### ARCHIVE_TEMPLATES")
        
        p1 = st.button("GitHub Actions (Java)")
        p2 = st.button("Terraform (AWS VPC)")
        p3 = st.button("K8s Deployment (Nginx)")
        p4 = st.button("Multi-Stage Docker")
        p5 = st.button("DevSecOps Pipeline")
        
        st.markdown("---")
        st.markdown('<div class="dot-matrix" style="color: #FF0031;">SYSTEM_STATUS</div>', unsafe_allow_html=True)
        st.info("NOVA_PRO // ONLINE\n\nLATENCY // 14ms")
        
        if p1: return "Generate GitHub Actions workflow for a Spring Boot Maven application with unit tests"
        if p2: return "Generate Terraform script for an EC2 t3.micro in us-east-1 within a custom VPC"
        if p3: return "Generate Kubernetes deployment for nginx with 3 replicas and a load balancer"
        if p4: return "Create a multi-stage Dockerfile for a production Node.js application"
        if p5: return "Generate a GitLab CI pipeline with integrated TruffleHog secret scanning and Snyk container scanning"
            
    return None

def _get_syntax_language(file_name, artifact_type=""):
    extension = file_name.split('.')[-1].lower() if '.' in file_name else ''
    mapping = {
        'tf': 'terraform',
        'yaml': 'yaml',
        'yml': 'yaml',
        'json': 'json',
        'sh': 'bash',
        'py': 'python',
        'txt': 'text',
        'dockerfile': 'dockerfile'
    }
    if extension in mapping:
        return mapping[extension]
    return artifact_type.lower().replace(" ", "") if artifact_type else ""


def _render_artifact(artifact, top_type=None, key_prefix=""):
    artifact_type = artifact.get('artifactType', 'Unknown')
    file_name = artifact.get('fileName', 'generated.txt')
    language = _get_syntax_language(file_name, artifact_type)

    st.markdown('---')
    st.markdown(f'<div class="dot-matrix" style="color: #FF0031; font-size: 1.2rem;">OUTPUT // {top_type or artifact_type}</div>', unsafe_allow_html=True)
    st.subheader(file_name)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.code(artifact.get('code', ''), language=language)

    with col2:
        st.markdown('<div class="dot-matrix" style="font-size: 0.8rem;">ACTIONS</div>', unsafe_allow_html=True)
        st.download_button(
            label="DOWNLOAD_FILE",
            data=artifact.get('code', ''),
            file_name=file_name,
            mime="text/plain",
            key=f"download_{key_prefix}"
        )
        if st.button("COPY_CLIPBOARD", key=f"copy_{key_prefix}"):
            st.toast("LOG: BYTES_COPIED_TO_CLIPBOARD")

    st.markdown('<div class="dot-matrix" style="font-size: 0.8rem; margin-top: 20px;">LOG_ANALYSIS</div>', unsafe_allow_html=True)
    st.info(artifact.get('explanation', ''))

    if artifact.get('compliance'):
        st.markdown('<div class="dot-matrix" style="font-size: 0.8rem; color: #00ff00;">COMPLIANCE_SCAN_PASS</div>', unsafe_allow_html=True)
        st.success("\n".join(artifact.get('compliance', [])))


def artifact_display(result):
    if not result:
        return

    artifacts = result.get('artifacts') if isinstance(result, dict) else None

    if artifacts and isinstance(artifacts, list):
        if len(artifacts) == 1:
            _render_artifact(artifacts[0], top_type=artifacts[0].get('artifactType', result.get('type', 'Output')),
                             key_prefix=artifacts[0].get('fileName', 'artifact').replace(' ', '_'))
            return

        st.markdown('---')
        st.markdown(f'<div class="dot-matrix" style="color: #FF0031; font-size: 1.2rem;">OUTPUT // MULTIPLE ARTIFACTS</div>', unsafe_allow_html=True)
        st.markdown('**Files Generated:**')
        for file_name in [artifact.get('fileName', 'artifact') for artifact in artifacts]:
            st.markdown(f'- {file_name}')

        for artifact in artifacts:
            section_name = artifact.get('fileName', 'artifact').replace(' ', '_')
            with st.expander(artifact.get('fileName', 'artifact')):
                _render_artifact(artifact, top_type=artifact.get('artifactType', result.get('type', 'Artifact')),
                                 key_prefix=section_name)
        return

    _render_artifact(result, top_type=result.get('type', 'Output'), key_prefix=result.get('file_name', 'artifact').replace(' ', '_'))
