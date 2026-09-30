# docx2latex

A local-first Python project that turns Microsoft Word `.docx` files into clean, Overleaf-ready LaTeX using a user-provided local AI model.

This project is designed to work without paid APIs, without remote AI hosting, and without requiring the developer to install or host an AI model. The only requirement is that the user installs a model locally using tools like Ollama, GPT4All, or LM Studio.

## Why this project exists

Many researchers, students, and professionals already have content in Microsoft Word, but exporting that content cleanly into LaTeX for Overleaf is tedious. This project automates the workflow:

1. Read a `.docx` file
2. Extract structured content
3. Send the extracted content to a local AI engine
4. Receive LaTeX back
5. Insert the LaTeX into a template
6. Save a final `.tex` file ready for Overleaf

## Features

- Converts `.docx` files into LaTeX output
- Extracts headings, paragraphs, lists, tables, and image references
- Supports multiple local AI backends via a plugin system
- Supports Overleaf templates via `{{CONTENT}}` placeholders
- Includes a rule-based fallback engine for offline use
- Works without paid AI APIs or secret keys

## Supported engines

The project uses a plugin-based `AIEngine` interface with these implementations:

- `BasicEngine` — rule-based fallback for local use when no AI is installed
- `LocalOllamaEngine` — uses Ollama locally
- `LocalGPT4AllEngine` — uses GPT4All Python bindings
- `LocalLMStudioEngine` — uses a local LM Studio server

## Supported templates

- `article`
- `report`
- `ieee`
- `acm`
- `resume`

## Repository layout

```text
docx2latex/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── setup.cfg
├── docx2latex/
│   ├── __init__.py
│   ├── __main__.py
│   ├── ai_engine.py
│   ├── cli.py
│   ├── converter.py
│   ├── extractor.py
│   ├── latex_builder.py
│   ├── utils.py
│   └── templates/
│       ├── article.tex
│       ├── report.tex
│       ├── ieee.tex
│       ├── acm.tex
│       └── resume.tex
├── examples/
│   ├── sample.docx
│   └── output.tex
└── .gitignore
```

## Installation

From a terminal:

```bash
cd C:\Users\emano\Documents\defender\docx2latex
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If you are on Linux or macOS:

```bash
cd /path/to/docx2latex
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Local AI setup

### Option 1: Ollama

1. Install Ollama from https://ollama.com/download
2. Pull a model:

```bash
ollama pull llama3.1
```

3. Run the converter:

```bash
docx2latex examples\sample.docx --template article --engine ollama --model llama3.1 --output examples\output.tex
```

### Option 2: GPT4All

1. Install GPT4All locally
2. Install the Python package:

```bash
pip install gpt4all
```

3. Use the local model engine:

```bash
docx2latex examples\sample.docx --template report --engine gpt4all --model mistral-7b-instruct-v0.1.gguf --output examples\output.tex
```

### Option 3: LM Studio

1. Install LM Studio
2. Run a local model server
3. Use:

```bash
docx2latex examples\sample.docx --template article --engine lmstudio --model local-model --lmstudio-url http://localhost:1234/v1 --output examples\output.tex
```

### Option 4: Basic fallback

No local AI required:

```bash
docx2latex examples\sample.docx --template article --engine basic --output examples\output.tex
```

## Usage

The CLI is the main interface:

```bash
docx2latex path\to\your\document.docx --template article --engine ollama --model llama3.1 --output output.tex
```

### Supported arguments

- `input`: path to the `.docx` file
- `--template`: `article`, `report`, `ieee`, `acm`, or `resume`
- `--engine`: `basic`, `ollama`, `gpt4all`, or `lmstudio`
- `--model`: model name for Ollama or GPT4All
- `--output`: path for the final `.tex` file
- `--ollama-host`: custom Ollama host URL
- `--lmstudio-url`: custom local LM Studio API URL

## Example conversion

```bash
docx2latex examples\sample.docx --template article --engine basic --output examples\output.tex
```

This creates a final Overleaf-ready LaTeX document in the target folder.

## How it works internally

1. `extractor.py` reads the Word document and pulls out document content.
2. `Document.to_prompt()` turns the extracted content into a prompt.
3. The selected `AIEngine` converts the prompt to LaTeX.
4. `latex_builder.py` inserts the generated LaTeX into a selected template via the `{{CONTENT}}` placeholder.
5. The final `.tex` file is saved and is ready to upload to Overleaf.

## Overleaf integration

The templates use the placeholder `{{CONTENT}}` so the generated LaTeX can be dropped into a standard Overleaf project.

Upload the output `.tex` file to Overleaf, and compile normally.

## Important notes

- No paid API keys are needed
- No remote AI hosting is required
- No big infrastructure is required
- The user must install their own local model on their machine

## Troubleshooting

### `ollama` command not found

Install Ollama and ensure it is on your PATH.

### `GPT4All` import error

Run:

```bash
pip install gpt4all
```

### LM Studio not responding

Make sure the local server is running and that the URL matches the server endpoint.

### Template not found

Use only one of these values:

```bash
article
report
ieee
acm
resume
```

## License

This project is distributed under the MIT License.

## Project status

This repo is a local-first prototype and is ready to be pushed to GitHub.
