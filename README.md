# AI Developer Productivity Agent (Overview)

A lightweight full‐stack tool that lets you click a button to:
1. Lint and analyze Python code.
2. Generate pytest templates.
3. Append human‐readable documentation.

Under the hood:
- **Frontend:** React + Tailwind dashboard (three buttons + output panel).
- **Backend:** FastAPI server exposing three POST endpoints.
- **Agent Logic:** Uses LangChain/OpenAI to suggest improvements, create tests, or update docs.
- **Code Tools:** Flake8 for linting, pytest for test scaffolding.
