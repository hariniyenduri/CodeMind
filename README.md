# 🤖 CodeMind

### AI-Powered Codebase Understanding Assistant

CodeMind is an AI-powered assistant designed to help developers, especially beginners and new team members, understand an existing software project.

Instead of manually going through hundreds of files and trying to understand how they are connected, a developer can upload the project as a ZIP file and ask questions about the codebase in natural language.

CodeMind retrieves the most relevant parts of the project and uses an LLM to generate a clear, beginner-friendly explanation based on the available project context.

---

## 📌 Problem

Understanding an unfamiliar software project can be difficult, especially for a fresher or a developer joining an existing project.

A project may contain:

- Many folders and files
- Multiple programming languages
- Large amounts of source code
- Different modules and functions
- Dependencies between files
- Complex execution flows

Reading the entire project manually before understanding a specific feature can take significant time.

---

## 💡 Solution

CodeMind provides a conversational interface for understanding an existing codebase.

The developer can:

1. Upload a project ZIP file.
2. CodeMind extracts the project.
3. Source-code files are identified.
4. The code is parsed into meaningful chunks.
5. Embeddings are generated for the code chunks.
6. The chunks and embeddings are stored in ChromaDB.
7. The developer asks a question.
8. CodeMind retrieves relevant code from the project.
9. The retrieved context is provided to an LLM.
10. The LLM generates a clear explanation.

---

## ✨ Features

### 📦 Project Upload

Upload an existing software project as a ZIP file.

### 🔍 Code Understanding

CodeMind processes source-code files and identifies meaningful elements such as:

- Functions
- Classes
- Imports
- Source-code sections

### 🧠 Semantic Code Retrieval

CodeMind uses embeddings to find code that is semantically related to the developer's question.

### 💬 Natural Language Questions

Developers can ask questions such as:

> Where is login implemented?

> What does this function do?

> Which file handles authentication?

> How does this feature work?

> What happens when the application starts?

### 🤖 LLM-Powered Explanations

Retrieved project context is provided to an LLM, which explains the code in a beginner-friendly manner.

### 🔄 LLM Fallback

CodeMind supports multiple LLM providers.

If one configured provider fails, CodeMind can try the next provider.

Current providers:

- Google Gemini
- Groq
- OpenRouter

### 👨‍💻 Beginner-Friendly Explanations

CodeMind is designed to explain an unfamiliar codebase as a senior developer would explain it to a new team member.

---

## 🏗️ System Architecture

```text
             User
               │
               ▼
       Upload Project ZIP
               │
               ▼
        ZIP Extraction
               │
               ▼
         File Scanning
               │
               ▼
          Code Loading
               │
               ▼
         Code Parsing
               │
               ▼
         Code Chunking
               │
               ▼
      Embedding Generation
               │
               ▼
           ChromaDB
        Vector Database
               │
               │
        User Question
               │
               ▼
       Query Embedding
               │
               ▼
       Semantic Retrieval
               │
               ▼
      Relevant Code Context
               │
               ▼
         Prompt Builder
               │
               ▼
        LLM Manager
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    Gemini    Groq   OpenRouter
       │       │        │
       └───────┼────────┘
               │
               ▼
        Generated Answer
               │
               ▼
              User

🛠️ Technology Stack
| Technology            | Purpose                               |
| --------------------- | ------------------------------------- |
| Python                | Core application development          |
| Streamlit             | User interface                        |
| Sentence Transformers | Code and query embeddings             |
| ChromaDB              | Vector storage and semantic retrieval |
| Tree-sitter           | Source-code parsing support           |
| Python AST            | Python code structure extraction      |
| Google Gemini         | LLM provider                          |
| Groq                  | LLM provider                          |
| OpenRouter            | LLM provider                          |
| python-dotenv         | Environment variable management       |

📂 Project Structure
CodeMind/
│
├── app.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── docs/
│   ├── architecture.md
│   └── project_notes.md
│
├── src/
│   │
│   ├── embeddings/
│   │   ├── __init__.py
│   │   └── embedding_generator.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── code_loader.py
│   │   ├── file_scanner.py
│   │   └── zip_extractor.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── fallback_manager.py
│   │   ├── gemini_provider.py
│   │   ├── groq_provider.py
│   │   ├── llm_client.py
│   │   ├── llm_manager.py
│   │   ├── openrouter_provider.py
│   │   ├── prompt_builder.py
│   │   └── providers.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── code_chunker.py
│   │   └── code_parser.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── context_builder.py
│   │   ├── rag_engine.py
│   │   └── retriever.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── retriever.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_utils.py
│   │   └── logger.py
│   │
│   └── vectorstore/
│       ├── __init__.py
│       └── chroma_manager.py
│
├── tests/
│   ├── __init__.py
│   ├── test_chunker.py
│   ├── test_embeddings.py
│   ├── test_extractor.py
│   ├── test_llm.py
│   ├── test_parser.py
│   ├── test_rag_engine.py
│   └── test_retrieval.py
│
├── .gitignore
├── README.md
└── requirements.txt
⚙️ How CodeMind Works
1. Upload

The user uploads a project ZIP file through the Streamlit interface.

2. Extraction

The ZIP file is safely extracted into the application's project data directory.

3. File Scanning

CodeMind scans the extracted project and identifies supported source-code files.

Unnecessary directories such as .git, .venv, node_modules, build, and dist are ignored.

4. Code Loading

The detected source files are loaded and their programming language is identified based on the file extension.

5. Code Parsing

CodeMind extracts structural information from source code.

For Python files, Python's AST parser is used to identify functions, classes, and imports.

6. Code Chunking

The source code is divided into meaningful chunks.

Each chunk contains information such as:

File path
Programming language
Chunk type
Function or class name
Start line
End line
Source code
7. Embedding Generation

CodeMind uses the all-MiniLM-L6-v2 Sentence Transformer model to generate vector representations of the code chunks.

8. Vector Storage

The embeddings and their associated code information are stored in ChromaDB.

9. Question Processing

When the developer asks a question, CodeMind generates an embedding for the question.

10. Retrieval

ChromaDB retrieves the code chunks that are semantically closest to the question.

11. Context Building

The retrieved code chunks are combined into project context.

12. LLM Response

The context and the user's question are sent to the configured LLM provider.

The LLM generates an explanation using the retrieved project context.

🔐 Environment Variables

API keys are stored in a .env file and are not included in the GitHub repository.

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

Never commit your .env file to GitHub.

The .gitignore file is configured to exclude it.

🚀 Installation
1. Clone the repository
git clone https://github.com/hariniyenduri/CodeMind.git
2. Enter the project directory
cd CodeMind
3. Create a virtual environment

Windows:

python -m venv .venv
4. Activate the virtual environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
5. Install dependencies
pip install -r requirements.txt
6. Configure API keys

Create a .env file in the project root and add the required API keys.

7. Run CodeMind
streamlit run app.py

The application will open in your browser.

💬 Example

After uploading a project, a developer can ask:

Where is login implemented?

CodeMind retrieves the relevant code and can explain:

Which file contains the login implementation
Which function implements it
How the function works
Where it is called
How it connects with other files
🔒 Security and Privacy

CodeMind is designed to work with source-code projects uploaded by the user.

Important considerations:

API keys are stored using environment variables.
.env is excluded from Git.
Uploaded projects are excluded from Git.
Extracted project files are excluded from Git.
Local ChromaDB data is excluded from Git.
ZIP extraction includes protection against path traversal attacks.

Users should avoid uploading confidential or sensitive source code to external LLM providers unless their organization's security and privacy requirements allow it.

⚠️ Current Limitations

CodeMind is currently an internship-level prototype and has some limitations.

Code parsing support varies by programming language.
Python currently has stronger structural parsing support.
Retrieval quality depends on the embedding model and available code context.
Very large projects may require additional optimization.
LLM responses depend on the retrieved project context.
External LLM providers may have API rate limits.
The application currently focuses on understanding an existing codebase rather than modifying or executing the uploaded project.
🎯 Project Goal

The goal of CodeMind is to reduce the time required for a developer to understand an unfamiliar software project.

Instead of manually searching through a large codebase, a developer can ask questions in natural language and receive explanations grounded in the project's source code.

👩‍💻 Author

Harini Yenduri

GitHub:
https://github.com/hariniyenduri