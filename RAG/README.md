# CLI RAG Agent

This project is a beginner-friendly command line RAG application.

RAG means Retrieval-Augmented Generation. In this project, the app reads a PDF, splits it into small chunks, stores those chunks in a vector database, and then answers your questions using the PDF content.

## Files

- `Agent.py` - run this file to start the CLI app.
- `main.py` - contains the LangGraph agent and retrieval tool.
- `Guidelines.pdf` - sample PDF you can use for testing.
- `testing/` - vector database folder created when you run the app.

## Requirements

You need:

- Python installed
- A Google Gemini API key
- The required Python packages

## 1. Open The Project Folder

In PowerShell or terminal, go to this project:

```powershell
cd "C:\VKY\03_PROJECTS\GIT_PROJECT(new)\RAG"
```

## 2. Create A Virtual Environment

This keeps the project packages separate from your system Python.

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Install Packages

Install the libraries used by the project:

```powershell
pip install langchain langchain-community langchain-text-splitters langchain-google-genai langchain-chroma langgraph python-dotenv pypdf
```

## 4. Add Your Gemini API Key

Create a `.env` file and add your Google API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

Important: In `main.py` and `Agent.py`, the code currently loads a hard-coded `.env` path:

```python
load_dotenv(r'C:\VKY\02_SKILLS\LANGHAIN\LEVEL-2\.env')
```

If your `.env` file is inside the `RAG` folder, change that line in both files to:

```python
load_dotenv()
```

## 5. Run The CLI RAG App

From inside the `RAG` folder, run:

```powershell
python Agent.py
```

You will see:

```text
=====WELCOME TO CLI RAG AGENT======
Enter the pdf path :
```

Enter the full path to your PDF. Example:

```text
C:\VKY\03_PROJECTS\GIT_PROJECT(new)\RAG\Guidelines.pdf
```

Then ask a question:

```text
Ask you question :
```

Example:

```text
What is this document about?
```

To stop the app, type:

```text
exit
```

## Common Errors

### API Key Error

If you see an error about `GOOGLE_API_KEY`, check that:

- Your `.env` file exists
- Your API key is correct
- `load_dotenv()` is loading the correct `.env` file

### PDF Path Error

If the PDF cannot be loaded, use the full PDF path instead of only the file name.

Example:

```text
C:\VKY\03_PROJECTS\GIT_PROJECT(new)\RAG\Guidelines.pdf
```

### Package Not Found

If you see an error like `ModuleNotFoundError`, install the missing package with `pip install`.

Example:

```powershell
pip install langchain-google-genai
```

## Basic Flow

1. Run `python Agent.py`
2. Enter a PDF path
3. Wait while the vector database is created
4. Ask questions about the PDF
5. Type `exit` to close the app
