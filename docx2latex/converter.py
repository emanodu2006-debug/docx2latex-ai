from __future__ import annotations

from pathlib import Path

from .ai_engine import AIEngine, build_engine
from .extractor import extract_docx
from .latex_builder import build_latex_document, write_output_file


class DocxToLatexConverter:
    def __init__(self, engine: AIEngine | str | None = None, template_name: str = 'article'):
        self.template_name = template_name
        if isinstance(engine, str):
            self.engine = build_engine(engine)
        else:
            self.engine = engine or build_engine('basic')

    def convert(self, docx_path: str | Path, output_path: str | Path | None = None) -> str:
        document = extract_docx(docx_path)
        prompt = document.to_prompt()
        latex_content = self.engine.convert_to_latex(prompt)
        final_tex = build_latex_document(self.template_name, latex_content, document.images)
        if output_path:
            write_output_file(output_path, final_tex)
        return final_tex


def convert_docx_to_tex(docx_path: str | Path, template_name: str = 'article', engine: AIEngine | str = 'basic', output_path: str | Path | None = None) -> str:
    converter = DocxToLatexConverter(engine=engine, template_name=template_name)
    return converter.convert(docx_path=docx_path, output_path=output_path)
