from __future__ import annotations

import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'rel': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


@dataclass
class DocumentImage:
    filename: str
    alt_text: str = ''
    binary: bytes | None = None


@dataclass
class Document:
    title: str = ''
    paragraphs: list[str] = field(default_factory=list)
    headings: list[str] = field(default_factory=list)
    lists: list[str] = field(default_factory=list)
    tables: list[list[list[str]]] = field(default_factory=list)
    images: list[DocumentImage] = field(default_factory=list)

    def to_prompt(self) -> str:
        sections = [f'Title: {self.title}' if self.title else '']
        for heading in self.headings:
            sections.append(f'Heading: {heading}')
        for paragraph in self.paragraphs:
            sections.append(paragraph)
        for item in self.lists:
            sections.append(f'- {item}')
        for table in self.tables:
            rows = [' | '.join(row) for row in table]
            sections.append('Table: ' + ' ; '.join(rows))
        for image in self.images:
            sections.append(f'Image: {image.filename} ({image.alt_text})')
        return '\n\n'.join(part for part in sections if part).strip()


def _find_text(node: ET.Element) -> str:
    return ''.join(text.text or '' for text in node.findall('.//w:t', NS))


def _parse_style(paragraph: ET.Element) -> str:
    style_el = paragraph.find('w:pPr/w:pStyle', NS)
    return style_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '') if style_el is not None else ''


def _parse_table(table: ET.Element) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in table.findall('.//w:tr', NS):
        cells: list[str] = []
        for cell in row.findall('./w:tc', NS):
            text = _find_text(cell)
            cells.append(text.strip())
        if cells:
            rows.append(cells)
    return rows


def _load_relationships(docx_path: Path) -> dict[str, str]:
    with zipfile.ZipFile(docx_path) as zf:
        rels_path = 'word/_rels/document.xml.rels'
        if rels_path not in zf.namelist():
            return {}
        rels_xml = zf.read(rels_path)
    root = ET.fromstring(rels_xml)
    rels: dict[str, str] = {}
    for rel in root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
        rels[rel.attrib.get('Id', '')] = rel.attrib.get('Target', '')
    return rels


def _extract_images(docx_path: Path, document_root: ET.Element) -> list[DocumentImage]:
    relationship_map = _load_relationships(docx_path)
    images: list[DocumentImage] = []
    for drawing in document_root.findall('.//w:drawing', NS):
        for blip in drawing.findall('.//a:blip', NS):
            rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            if not rid:
                continue
            target = relationship_map.get(rid, '')
            if not target:
                continue
            if target.startswith('/'):
                target = target.lstrip('/')
            image_path = 'word/' + target.replace('\\', '/')
            with zipfile.ZipFile(docx_path) as zf:
                if image_path not in zf.namelist():
                    continue
                binary = zf.read(image_path)
            filename = target.rsplit('/', 1)[-1]
            images.append(DocumentImage(filename=filename, alt_text=filename, binary=binary))
    return images


def extract_docx(docx_path: str | Path) -> Document:
    path = Path(docx_path)
    with zipfile.ZipFile(path) as zf:
        xml_bytes = zf.read('word/document.xml')

    root = ET.fromstring(xml_bytes)
    body = root.find('w:body', NS)
    if body is None:
        return Document()

    document = Document()
    paragraphs: list[str] = []
    headings: list[str] = []
    lists: list[str] = []
    tables: list[list[list[str]]] = []

    for child in body:
        tag = child.tag
        if tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
            text = _find_text(child).strip()
            if not text:
                continue
            style = _parse_style(child)
            if style.startswith('Heading'):
                headings.append(text)
            elif child.find('w:pPr/w:numPr', NS) is not None:
                lists.append(text)
            else:
                paragraphs.append(text)
        elif tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl':
            table_data = _parse_table(child)
            if table_data:
                tables.append(table_data)

    document.paragraphs = paragraphs
    document.headings = headings
    document.lists = lists
    document.tables = tables
    document.images = _extract_images(path, root)
    document.title = headings[0] if headings else ''
    return document


if __name__ == '__main__':
    sample = extract_docx(Path(__file__).resolve().parent.parent / 'examples' / 'sample.docx')
    print(sample.to_prompt())
