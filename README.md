# docx2latex-ai

A local-first Python project that converts Microsoft Word `.docx` files into clean, Overleaf-ready LaTeX using a user-provided local AI model.

This project is designed to work without paid APIs, without remote AI hosting, and without requiring the developer to install or host an AI model. The user installs only the local model they want to use, such as Ollama, GPT4All, or LM Studio.

## Why this project exists

Many students, researchers, and professionals already have content in Word documents. Converting those documents into polished Overleaf-ready LaTeX by hand is time-consuming. This project automates that process:

1. Read a `.docx` file
2. Extract headings, paragraphs, lists, tables, and image references
3. Send the content to a local AI engine
4. Receive LaTeX output
5. Insert the LaTeX into a chosen Overleaf template
6. Save a final `.tex` file ready for upload

## Features

- Converts `.docx` files into LaTeX output
- Extracts paragraphs, headings, lists, tables, and images
- Uses a plugin-based `AIEngine` architecture
- Supports local engines without paid APIs
- Includes a fallback rule-based converter
- Supports multiple Overleaf-compatible templates

## Supported engines

The project includes these engine implementations:

- `AIEngine` — abstract base interface
- `LocalOllamaEngine` — executes local Ollama models
- `LocalGPT4AllEngine` — uses GPT4All Python bindings
- `LocalLMStudioEngine` — connects to a local LM Studio server
- `BasicEngine` — rule-based fallback without AI

## Supported templates

- `article`
- `report`
- `ieee`
- `acm`
- `resume`

## Repository structure

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

### Windows

```powershell
cd C:\Users\emano\Documents\defender\docx2latex
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux/macOS

```bash
cd /path/to/docx2latex
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Local AI setup

### Option 1: Ollama

1. Install Ollama: https://ollama.com/download
2. Pull a model:

```bash
ollama pull llama3.1
```

3. Run the converter:

```bash
docx2latex examples\sample.docx --template article --engine ollama --model llama3.1 --output examples\output.tex
```

### Option 2: GPT4All

1. Install GPT4All locally.
2. Install the Python package:

```bash
pip install gpt4all
```

3. Run:

```bash
docx2latex examples\sample.docx --template report --engine gpt4all --model mistral-7b-instruct-v0.1.gguf --output examples\output.tex
```

### Option 3: LM Studio

1. Install LM Studio.
2. Start a local model server.
3. Run:

```bash
docx2latex examples\sample.docx --template article --engine lmstudio --model local-model --lmstudio-url http://localhost:1234/v1 --output examples\output.tex
```

### Option 4: No AI installed

Use the built-in fallback engine:

```bash
docx2latex examples\sample.docx --template article --engine basic --output examples\output.tex
```

## Usage

```bash
docx2latex "C:\path\to\document.docx" --template article --engine ollama --model llama3.1 --output "C:\path\to\output.tex"
```

### Supported arguments

- `input`: path to the `.docx` file
- `--template`: `article`, `report`, `ieee`, `acm`, `resume`
- `--engine`: `basic`, `ollama`, `gpt4all`, `lmstudio`
- `--model`: model name used by Ollama or GPT4All
- `--output`: output path for the final `.tex` file
- `--ollama-host`: custom Ollama host URL
- `--lmstudio-url`: custom LM Studio base URL

## Example

```bash
docx2latex examples\sample.docx --template article --engine basic --output examples\output.tex
```

This creates a final Overleaf-ready `.tex` file.

## How the system works internally

1. `extractor.py` reads the `.docx` file and extracts headings, paragraphs, lists, tables, and image references.
2. `Document.to_prompt()` turns the extracted content into a text prompt.
3. The chosen `AIEngine` converts that content into LaTeX.
4. `latex_builder.py` inserts the returned LaTeX into the selected template using the `{{CONTENT}}` placeholder.
5. The result is a final `.tex` file ready for upload to Overleaf.

## Overleaf integration

The template files include `{{CONTENT}}`, making them compatible with Overleaf workflows. Once you generate the `.tex` file, upload it to Overleaf and compile as usual.

## Notes

- No paid API keys are needed
- No remote AI hosting is required
- No AI model is bundled with the repo
- The user installs their own local model and runtime

## Troubleshooting

### `ollama` command not found

Install Ollama and ensure it is on your PATH.

### GPT4All import error

Install it manually:

```bash
pip install gpt4all
```

### LM Studio not responding

Make sure the local server is running and the URL matches the server endpoint.

### Template not found

Use one of these values:

```bash
article
report
ieee
acm
resume
```

## License

MIT License
