import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from backend.code_tools import run_flake8, run_pytest

# 1. Load our secret API key from the .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. Prepare the LLM client (the “brain” that talks to OpenAI)
llm = ChatOpenAI(
    model_name="gpt-4o-mini",  # a smaller, faster model good for code tasks
    temperature=0.2,            # low “temperature” means more focused answers
    openai_api_key=OPENAI_API_KEY
)

def analyze_code_and_suggest(file_path: str) -> str:
    """
    Read a Python file, run Flake8, and then ask the LLM to suggest improvements.
    Returns a combined text of lint output + AI suggestions.
    """
    # 1️⃣ Read the code file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
    except FileNotFoundError:
        return "File not found."

    # 2️⃣ Run Flake8 to catch style issues
    lint_output = run_flake8(file_path)

    # 3️⃣ Build a prompt to ask the LLM
    prompt = [
        SystemMessage(content="You are a friendly code helper."),
        HumanMessage(content=f"Here is some Python code:\n\n{code_content}\n\n"
                             "Please suggest improvements or point out logical issues.")
    ]

    # 4️⃣ Send the prompt to the LLM and get a response
    try:
        response = llm(prompt)
        ai_suggestions = response.content
    except Exception as e:
        ai_suggestions = f"Error calling OpenAI (could be quota or network issue): {e}"

    # 5️⃣ Combine lint results and AI suggestions into one text block
    return f"=== Linting Output ===\n{lint_output}\n\n=== LLM Suggestions ===\n{ai_suggestions}"


def generate_test_template(file_path: str) -> str:
    """
    Ask the LLM to create a basic pytest file for a given Python file.
    Saves the new test file under tests/test_<filename>.py.
    """
    # 1️⃣ Read the code file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
    except FileNotFoundError:
        return "File not found."

    # 2️⃣ Build a prompt asking the LLM to generate tests
    prompt = [
        SystemMessage(content="You are an expert at writing pytest tests."),
        HumanMessage(content=f"Given this Python code:\n\n{code_content}\n\n"
                             "Generate a basic pytest file with test functions for each function in the code.")
    ]

    # 3️⃣ Get the AI’s response (the test code)
    try:
        response = llm(prompt)
        test_code = response.content
    except Exception as e:
        return f"Error calling OpenAI (could be quota or network issue): {e}"

    # 4️⃣ Determine the new test file’s name, e.g., tests/test_sample.py
    test_filename = f"tests/test_{os.path.basename(file_path)}"

    # 5️⃣ Make sure the tests/ folder exists, then write the test file
    os.makedirs("tests", exist_ok=True)
    with open(test_filename, "w", encoding="utf-8") as tf:
        tf.write(test_code)

    return f"Test file created: {test_filename}"


def update_documentation(file_path: str, doc_file: str = "README.md") -> str:
    """
    Ask the LLM to write or update documentation for a code file.
    Appends the generated docs to README.md (or another doc file).
    """
    # 1️⃣ Read the code file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
    except FileNotFoundError:
        return "Code file not found."

    # 2️⃣ Build a prompt asking the LLM to explain the code
    prompt = [
        SystemMessage(content="You are a clear technical writer."),
        HumanMessage(content=f"Write a short documentation section that explains what this Python code does. "
                             f"Code:\n\n{code_content}")
    ]

    # 3️⃣ Get the AI’s explanation
    try:
        response = llm(prompt)
        doc_text = response.content
    except Exception as e:
        return f"Error calling OpenAI (could be quota or network issue): {e}"

    # 4️⃣ Append that explanation to the chosen doc file (default is README.md)
    with open(doc_file, "a", encoding="utf-8") as df:
        df.write("\n\n---\n")
        df.write(f"### Documentation for {os.path.basename(file_path)}\n\n")
        df.write(doc_text + "\n")

    return f"Documentation updated in {doc_file}"
