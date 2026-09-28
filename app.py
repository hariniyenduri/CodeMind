import streamlit as st
from pathlib import Path

from config.settings import UPLOAD_DIR

from src.ingestion.zip_extractor import (
    extract_project,
    ZipExtractionError,
)
from src.ingestion.file_scanner import scan_project
from src.ingestion.code_loader import load_project

from src.processing.code_parser import parse_code_file
from src.processing.code_chunker import create_code_chunks

from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vectorstore.chroma_manager import ChromaManager

from src.rag.rag_engine import RAGEngine


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CodeMind",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# CUSTOM UI STYLING
# =========================================================

st.markdown(
    """
    <style>

    .codemind-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .codemind-subtitle {
        font-size: 17px;
        color: #6b7280;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    textarea {
        font-size: 16px !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None

if "embedding_generator" not in st.session_state:
    st.session_state.embedding_generator = None

if "chroma_manager" not in st.session_state:
    st.session_state.chroma_manager = None

if "project_processed" not in st.session_state:
    st.session_state.project_processed = False

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="codemind-title">🤖 CodeMind</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="codemind-subtitle">
        Your AI assistant for understanding existing software projects
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📁 Project")

    uploaded_file = st.file_uploader(
        "Upload your project ZIP",
        type=["zip"],
    )

    st.divider()

    st.markdown("### 💡 How to use CodeMind")

    st.markdown(
        """
        1. Upload your project ZIP.
        2. Wait until the project is processed.
        3. Once ready, ask your questions.
        4. Continue the conversation with CodeMind.
        """
    )


# =========================================================
# PROCESS UPLOADED PROJECT
# =========================================================

if uploaded_file is not None:

    # Process only when a new ZIP is uploaded
    if (
        st.session_state.processed_file
        != uploaded_file.name
    ):

        with st.spinner(
            "🔄 Processing your project..."
        ):

            try:

                # -----------------------------------------
                # STEP 1 — SAVE ZIP
                # -----------------------------------------

                zip_path = (
                    UPLOAD_DIR
                    / uploaded_file.name
                )

                with open(
                    zip_path,
                    "wb",
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )


                # -----------------------------------------
                # STEP 2 — EXTRACT PROJECT
                # -----------------------------------------

                extracted_path = extract_project(
                    Path(zip_path)
                )


                # -----------------------------------------
                # STEP 3 — SCAN SOURCE FILES
                # -----------------------------------------

                source_files = scan_project(
                    extracted_path
                )

                if not source_files:

                    raise RuntimeError(
                        "No supported source-code files "
                        "were found in the uploaded project."
                    )


                # -----------------------------------------
                # STEP 4 — LOAD SOURCE FILES
                # -----------------------------------------

                loaded_files = load_project(
                    source_files
                )

                if not loaded_files:

                    raise RuntimeError(
                        "The project files could not be loaded."
                    )


                # -----------------------------------------
                # STEP 5 — PARSE SOURCE CODE
                # -----------------------------------------

                parsed_files = []

                for code_file in loaded_files:

                    parsed = parse_code_file(
                        file_path=code_file.file_path,
                        content=code_file.content,
                        language=code_file.language,
                    )

                    parsed_files.append(
                        parsed
                    )


                # -----------------------------------------
                # STEP 6 — CREATE CODE CHUNKS
                # -----------------------------------------

                all_chunks = []

                for parsed, code_file in zip(
                    parsed_files,
                    loaded_files,
                ):

                    chunks = create_code_chunks(
                        parsed,
                        code_file.content,
                    )

                    all_chunks.extend(
                        chunks
                    )


                if not all_chunks:

                    raise RuntimeError(
                        "No meaningful code chunks "
                        "could be created from the project."
                    )


                # -----------------------------------------
                # STEP 7 — GENERATE EMBEDDINGS
                # -----------------------------------------

                embedding_generator = (
                    EmbeddingGenerator()
                )

                chunk_texts = [
                    chunk.content
                    for chunk in all_chunks
                ]

                embeddings = (
                    embedding_generator
                    .generate_embeddings(
                        chunk_texts
                    )
                )


                # -----------------------------------------
                # STEP 8 — STORE IN CHROMADB
                # -----------------------------------------

                chroma_manager = (
                    ChromaManager()
                )

                # Remove data from previous project
                chroma_manager.clear()

                chroma_manager.add_chunks(
                    all_chunks,
                    embeddings,
                )


                # -----------------------------------------
                # STEP 9 — INITIALIZE RAG ENGINE
                # -----------------------------------------

                rag_engine = RAGEngine()


                # -----------------------------------------
                # STEP 10 — SAVE COMPONENTS
                # -----------------------------------------

                st.session_state.embedding_generator = (
                    embedding_generator
                )

                st.session_state.chroma_manager = (
                    chroma_manager
                )

                st.session_state.rag_engine = (
                    rag_engine
                )

                st.session_state.project_processed = (
                    True
                )

                st.session_state.processed_file = (
                    uploaded_file.name
                )

                # Start a fresh conversation
                st.session_state.messages = []


            except ZipExtractionError as error:

                st.session_state.project_processed = False

                st.error(
                    "❌ The project could not be processed."
                )

                st.exception(error)


            except Exception as error:

                st.session_state.project_processed = False

                st.error(
                    "❌ Something went wrong while "
                    "processing the project."
                )

                st.exception(error)


# =========================================================
# PROJECT READY MESSAGE
# =========================================================

if (
    st.session_state.project_processed
    and st.session_state.processed_file
):

    st.success(
        "✅ Project processed successfully. "
        "You can now ask questions about your project."
    )


# =========================================================
# WELCOME MESSAGE
# =========================================================

if (
    st.session_state.project_processed
    and not st.session_state.messages
):

    st.info(
        "👋 You can now ask CodeMind about "
        "the project's files, functions, modules, "
        "algorithms, or execution flow."
    )


# =========================================================
# DISPLAY PREVIOUS CONVERSATION
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# QUESTION INPUT
# =========================================================

if st.session_state.project_processed:

    question = st.chat_input(
        "💬 Ask your doubts regarding the project..."
    )

else:

    question = None


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # ---------------------------------------------
    # USER QUESTION
    # ---------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )


    # ---------------------------------------------
    # GENERATE ANSWER
    # ---------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🔍 Understanding your question..."
        ):

            try:

                result = (
                    st.session_state
                    .rag_engine
                    .ask(question)
                )

                response = result.get(
                    "response",
                    "The provided project context "
                    "is not sufficient to determine this.",
                )

                st.markdown(
                    response
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )


            except Exception as error:

                error_message = (
                    "Sorry, I couldn't process "
                    "your question. Please try again."
                )

                st.error(
                    error_message
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )

                # Keep the technical error out of
                # the normal user interface.
                print(
                    f"CodeMind error: {error}"
                )