from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod

import requests


class AIEngine(ABC):
    """Interface for turning extracted document text into LaTeX."""

    @abstractmethod
    def convert_to_latex(self, text: str) -> str:
        raise NotImplementedError


class LocalOllamaEngine(AIEngine):
    def __init__(self, model: str = 'llama3.1', host: str = 'http://localhost:11434', timeout: int = 180):
        self.model = model
        self.host = host.rstrip('/')
        self.timeout = timeout

    def convert_to_latex(self, text: str) -> str:
        prompt = (
            'Convert the following document content into clean LaTeX for Overleaf. '
            'Return only valid LaTeX code, no markdown fences, no commentary.\n\n'
            'Requirements: use sections, paragraphs, itemize/enumerate for lists, and include tables with tabular when relevant.\n'
            'Keep the output compact but polished.\n\n'
            f'{text}'
        )
        try:
            result = subprocess.run(
                ['ollama', 'generate', self.model, '--prompt', prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )
        except Exception as exc:
            raise RuntimeError(f'Local Ollama conversion failed: {exc}') from exc

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or 'Ollama generation failed.')
        output = result.stdout.strip()
        if not output:
            raise RuntimeError('Ollama returned no content.')
        return output


class LocalGPT4AllEngine(AIEngine):
    def __init__(self, model: str = 'mistral-7b-instruct-v0.1.gguf', model_path: str | None = None):
        self.model = model
        self.model_path = model_path

    def convert_to_latex(self, text: str) -> str:
        try:
            from gpt4all import GPT4All
        except ImportError as exc:
            raise RuntimeError('GPT4All is not installed. Run: pip install gpt4all') from exc

        prompt = (
            'Convert the following document to clean Overleaf LaTeX. '
            'Return only LaTeX, without explanations.\n\n'
            f'{text}'
        )
        model = GPT4All(self.model_path or self.model)
        response = model.generate(prompt, max_tokens=2000)
        return response.strip() if response else ''


class LocalLMStudioEngine(AIEngine):
    def __init__(self, base_url: str = 'http://localhost:1234/v1', model: str = 'local-model'):
        self.base_url = base_url.rstrip('/')
        self.model = model

    def convert_to_latex(self, text: str) -> str:
        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': 'Convert document text to polished LaTeX for Overleaf. Return only valid LaTeX, no markdown fences.'
                },
                {'role': 'user', 'content': text},
            ],
            'temperature': 0.2,
            'max_tokens': 3000,
        }
        response = requests.post(f'{self.base_url}/chat/completions', json=payload, timeout=180)
        response.raise_for_status()
        data = response.json()
        content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        if not content:
            raise RuntimeError('LM Studio returned an empty output.')
        return content.strip()


class BasicEngine(AIEngine):
    """Fallback rule-based converter when no model is available."""

    def convert_to_latex(self, text: str) -> str:
        text = text.strip()
        if not text:
            return '\\section*{Document}\n'

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        latex = ['\\section*{Document}']

        for line in lines:
            if line.lower().startswith('heading:'):
                title = line.split(':', 1)[1].strip()
                latex.append(f'\\section{{{title}}}')
                continue
            if line.lower().startswith('title:'):
                title = line.split(':', 1)[1].strip()
                latex.append(f'\\title{{{title}}}')
                continue
            if line.startswith('- '):
                latex.append(f'\\begin{{itemize}}\\item {line[2:]} \\end{{itemize}}')
                continue
            latex.append(f'{line}\\\\')

        return '\n'.join(latex)


def build_engine(engine_name: str, **kwargs) -> AIEngine:
    engine_name = engine_name.lower()
    if engine_name == 'ollama':
        return LocalOllamaEngine(**kwargs)
    if engine_name == 'gpt4all':
        return LocalGPT4AllEngine(**kwargs)
    if engine_name == 'lmstudio':
        return LocalLMStudioEngine(**kwargs)
    if engine_name == 'basic':
        return BasicEngine()
    raise ValueError(f'Unsupported engine: {engine_name}')
