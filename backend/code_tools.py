import subprocess
import sys

def run_flake8(file_path: str) -> str:
    """
    Run Flake8 (linting) on a given Python file.
    Returns the output (errors/warnings) as a string.
    """
    try:
        # subprocess.run lets us call Flake8 as if we typed it in the terminal.
        result = subprocess.run(
            [sys.executable, "-m", "flake8", file_path],
            capture_output=True,  # capture what flake8 prints
            text=True,            # treat output as text (not bytes)
            check=False           # don’t raise an exception if flake8 finds issues
        )
        # If flake8 prints nothing, that means “No linting issues.”
        return result.stdout or "No linting issues found."
    except Exception as e:
        return f"Error running flake8: {e}"

def run_pytest(test_folder: str) -> str:
    """
    Run pytest on a folder (or file) and return the output as a string.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_folder, "--maxfail=1", "--disable-warnings"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout or "No test output."
    except Exception as e:
        return f"Error running pytest: {e}"
