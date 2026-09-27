import requests
import streamlit as st

from backend.config import get_settings
from backend.utils.document_formatter import format_html_preview
from frontend.utils.exporters import (
    export_txt,
    export_docx,
    export_pdf
)


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

settings = get_settings()

BACKEND_URL = settings.backend_url


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #0e1117;
        color: white;
    }

    /* Main container */
    .block-container {
        max-width: 850px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    /* Logo */
    .logo {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 21px;
        font-weight: 500;
        margin-bottom: 30px;
        color: #ffffff;
    }

    /* Labels */
    label {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Text inputs */
    input {
        background-color: #20232d !important;
        color: white !important;
        border: 1px solid #353947 !important;
    }

    /* Text areas */
    textarea {
        background-color: #20232d !important;
        color: white !important;
        border: 1px solid #353947 !important;
    }

    /* Select box */
    div[data-baseweb="select"] > div {
        background-color: #20232d !important;
        color: white !important;
        border-color: #353947 !important;
    }

    /* Generate button */
    .stButton > button {
        width: 100%;
        background-color: #0879d1;
        color: white;
        border: none;
        border-radius: 5px;
        height: 45px;
        font-size: 16px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #0969b5;
        color: white;
    }

    /* Download buttons */
    .stDownloadButton > button {
        width: 100%;
        border-radius: 5px;
    }

    /* Success message */
    div[data-testid="stAlert"] {
        border-radius: 5px;
    }

    /* Document area */
    .document-container {
        background-color: #111827;
        border-radius: 8px;
        padding: 25px;
        margin-top: 15px;
        border: 1px solid #202938;
    }

    /* Generated heading */
    .generated-title {
        font-size: 28px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Info text */
    .info-text {
        color: #b8bec9;
        text-align: center;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = ""


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="logo">
        ⚖️ LegalEase
    </div>

    <div class="subtitle">
        AI Legal Document Generator
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------

st.markdown("### Document Type")

document_type = st.text_input(
    "Document Type",
    value="Freelance Work Contract",
    label_visibility="collapsed",
    placeholder="Example: Freelance Work Contract"
)


st.markdown("### Parties Involved")

parties = st.text_area(
    "Parties",
    label_visibility="collapsed",
    height=100,
    placeholder=(
        "Example:\n"
        "Jane Doe (Service Provider), "
        "TechNova Inc. (Client)"
    )
)


st.markdown("### Terms & Conditions")

terms = st.text_area(
    "Terms",
    label_visibility="collapsed",
    height=150,
    placeholder=(
        "Example:\n"
        "Work must be delivered by May 15, 2025;\n"
        "Payment will be made within 7 days of invoice;\n"
        "The client retains intellectual property rights."
    )
)


st.markdown("### Effective Date")

dates = st.text_input(
    "Effective Date",
    value="April 15, 2025",
    label_visibility="collapsed",
    placeholder="Example: April 15, 2025"
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

generate = st.button(
    "Generate Document"
)


# --------------------------------------------------
# GENERATE DOCUMENT
# --------------------------------------------------

if generate:

    if not document_type.strip():

        st.error(
            "Please enter the document type."
        )

    elif not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    elif not dates.strip():

        st.error(
            "Please enter the effective date."
        )

    else:

        request_data = {
            "document_type": document_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "dates": dates.strip()
        }

        api_url = (
            BACKEND_URL
            + "/api/generate"
        )

        with st.spinner(
            "Generating legal document..."
        ):

            try:

                response = requests.post(
                    api_url,
                    json=request_data,
                    timeout=180
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.generated_document = (
                        result["content"]
                    )

                    st.session_state.document_type = (
                        result["document_type"]
                    )

                    st.success(
                        "✅ Document Generated Successfully!"
                    )

                else:

                    try:

                        error_data = response.json()

                        error_message = error_data.get(
                            "detail",
                            "Unknown backend error."
                        )

                    except Exception:

                        error_message = response.text

                    st.error(
                        "Backend Error: "
                        + str(error_message)
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to backend. "
                    "Please start FastAPI on port 8000."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "❌ Request timed out. "
                    "Please try again."
                )

            except Exception as error:

                st.error(
                    "❌ Error: "
                    + str(error)
                )


# --------------------------------------------------
# GENERATED DOCUMENT
# --------------------------------------------------

if st.session_state.generated_document:

    st.markdown(
        """
        <div class="generated-title">
            Document Generated
        </div>
        """,
        unsafe_allow_html=True
    )


    # Editable document
    edited_document = st.text_area(
        "Generated Document",
        value=st.session_state.generated_document,
        height=600
    )


    st.session_state.generated_document = edited_document


    # --------------------------------------------------
    # PREVIEW
    # --------------------------------------------------

    st.markdown("### Document Preview")

    preview = format_html_preview(
        edited_document,
        st.session_state.document_type
    )

    st.components.v1.html(
        preview,
        height=700,
        scrolling=True
    )


    # --------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------

    st.markdown("### Download Document")

    col1, col2, col3 = st.columns(3)


    with col1:

        st.download_button(
            "📄 Download TXT",
            data=export_txt(
                edited_document
            ),
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True
        )


    with col2:

        st.download_button(
            "📝 Download DOCX",
            data=export_docx(
                edited_document,
                st.session_state.document_type
            ),
            file_name="LegalEase_Document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )


    with col3:

        st.download_button(
            "📕 Download PDF",
            data=export_pdf(
                edited_document,
                st.session_state.document_type
            ),
            file_name="LegalEase_Document.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="info-text">
        LegalEase - AI Powered Legal Document Generator
    </div>
    """,
    unsafe_allow_html=True
)