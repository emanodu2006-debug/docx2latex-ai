from __future__ import annotations

import argparse
from pathlib import Path

from .converter import convert_docx_to_tex


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Convert a .docx document to Overleaf-ready LaTeX using a local AI engine.')
    parser.add_argument('input', help='Path to the input .docx file')
    parser.add_argument('--template', choices=['article', 'report', 'ieee', 'acm', 'resume'], default='article', help='LaTeX template to use')
    parser.add_argument('--engine', choices=['basic', 'ollama', 'gpt4all', 'lmstudio'], default='basic', help='Local AI engine to use')
    parser.add_argument('--model', default='llama3.1', help='Model name for Ollama or GPT4All')
    parser.add_argument('--output', default='output.tex', help='Path to the final .tex output file')
    parser.add_argument('--ollama-host', default='http://localhost:11434', help='Ollama host URL')
    parser.add_argument('--lmstudio-url', default='http://localhost:1234/v1', help='LM Studio base URL')
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.engine == 'basic':
        engine = 'basic'
    elif args.engine == 'ollama':
        from .ai_engine import LocalOllamaEngine
        engine = LocalOllamaEngine(model=args.model, host=args.ollama_host)
    elif args.engine == 'gpt4all':
        from .ai_engine import LocalGPT4AllEngine
        engine = LocalGPT4AllEngine(model=args.model)
    elif args.engine == 'lmstudio':
        from .ai_engine import LocalLMStudioEngine
        engine = LocalLMStudioEngine(base_url=args.lmstudio_url, model=args.model)
    else:
        raise ValueError(f'Unknown engine: {args.engine}')

    output_path = Path(args.output)
    result = convert_docx_to_tex(args.input, template_name=args.template, engine=engine, output_path=output_path)
    print(f'LaTeX written to: {output_path}')
    print(result[:300])


if __name__ == '__main__':
    main()
