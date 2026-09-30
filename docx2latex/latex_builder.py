from __future__ import annotations

from pathlib import Path


def load_template(template_name: str) -> str:
    template_map = {
        'article': 'article.tex',
        'report': 'report.tex',
        'ieee': 'ieee.tex',
        'acm': 'acm.tex',
        'resume': 'resume.tex',
    }
    template_file = template_map.get(template_name.lower())
    if not template_file:
        raise ValueError(f'Unsupported template: {template_name}')

    package_dir = Path(__file__).resolve().parent
    template_path = package_dir / 'templates' / template_file
    return template_path.read_text(encoding='utf-8')


def build_latex_document(template_name: str, latex_content: str, images: list | None = None) -> str:
    content = latex_content.strip()
    template = load_template(template_name)
    if '{{CONTENT}}' not in template:
        raise ValueError(f'Template {template_name} does not include the {{CONTENT}} placeholder.')

    render = template.replace('{{CONTENT}}', content)
    if images:
        image_entries = []
        for image in images:
            image_entries.append(f'\\includegraphics[width=\\linewidth]{{{image.filename}}}')
        render = render.replace('{{IMAGES}}', '\n'.join(image_entries))
    return render


def write_output_file(output_path: str | Path, content: str) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding='utf-8')
    return output
