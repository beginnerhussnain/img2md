from lxml import etree
import re as _re
from dataclasses import dataclass, field
from typing import List, Optional
import re


@dataclass
class Line:
    text: str
    x0: int
    y0: int
    x1: int
    y1: int
    height: int
    words: List[dict] = field(default_factory=list)


def _parse_bbox(title: str) -> Optional[tuple]:
    for part in title.split(";"):
        part = part.strip()
        if part.startswith("bbox"):
            _, x0, y0, x1, y1 = part.split()
            return int(x0), int(y0), int(x1), int(y1)
    return None


def parse_hocr(tree: etree._Element) -> List[Line]:
    lines: List[Line] = []
    for line_el in tree.xpath("//*[@class='ocr_line']"):
        bbox = _parse_bbox(line_el.get("title", ""))
        if not bbox:
            continue
        x0, y0, x1, y1 = bbox

        words = []
        for w in line_el.xpath(".//*[@class='ocrx_word']"):
            wbbox = _parse_bbox(w.get("title", ""))
            conf = 0
            for p in (w.get("title", "") or "").split(";"):
                p = p.strip()
                if p.startswith("x_wconf"):
                    try:
                        conf = int(p.split()[1])
                    except Exception:
                        pass
            words.append({"text": w.text or "", "bbox": wbbox, "conf": conf})

        text = " ".join(w["text"] for w in words).strip()
        if not text:
            continue

        lines.append(Line(text=text, x0=x0, y0=y0, x1=x1, y1=y1,
                          height=y1 - y0, words=words))
    return lines


def _median_height(lines: List[Line]) -> int:
    hs = sorted(l.height for l in lines)
    return hs[len(hs) // 2] if hs else 20


def _is_heading(line: Line, median_h: int, next_line: Optional[Line]) -> int:
    if not line.text or len(line.text) > 80:
        return 0
    # Real headings are usually much taller than body text.
    # Requiring an absolute minimum size kills most UI labels.
    if line.height < median_h * 1.4:
        return 0
    ratio = line.height / median_h if median_h else 1
    gap_below = (next_line.y0 - line.y1) if next_line else 999
    # Real headings tend to be short (few words)
    word_count = len(line.text.split())
    if word_count > 12:
        return 0
    # Bigger + more whitespace below = higher-level heading
    if ratio >= 2.0 and gap_below > median_h * 1.2:
        return 1
    if ratio >= 1.7 and gap_below > median_h * 0.8:
        return 2
    if ratio >= 1.4 and gap_below > median_h * 0.5:
        return 3
    return 0


def _is_list_item(line: Line) -> Optional[str]:
    t = line.text.lstrip()
    for marker in ["•", "·", "◦", "▪"]:
        if t.startswith(marker):
            return t[len(marker):].strip()
    m = re.match(r"^(\d+[\.\)]|[-*])\s+(.*)$", t)
    if m:
        return m.group(2)
    return None



_JUNK_LINE = _re.compile(r"^[=\-_\W]{2,}[\w\s]{0,20}$")

def _is_junk(line: Line) -> bool:
    t = line.text.strip()
    if len(t) < 2:
        return True
    # Lines that are mostly punctuation/symbols (icon misreads)
    alpha = sum(c.isalnum() for c in t)
    if alpha / max(len(t), 1) < 0.35:
        return True
    return False

def infer_markdown(lines: List[Line]) -> str:
    if not lines:
        return ""

    median_h = _median_height(lines)
    out: List[str] = []
    prev_y1: Optional[int] = None
    for i, line in enumerate(lines):
        if _is_junk(line):
            prev_y1 = line.y1
            continue

        nxt = lines[i + 1] if i + 1 < len(lines) else None

        if prev_y1 is not None:
            gap = line.y0 - prev_y1
            if gap > median_h * 1.2 and out and out[-1] != "":
                out.append("")

        level = _is_heading(line, median_h, nxt)
        if level:
            out.append(f"{'#' * level} {line.text}")
            prev_y1 = line.y1
            continue

        li = _is_list_item(line)
        if li:
            out.append(f"- {li}")
            prev_y1 = line.y1
            continue

        if (out and out[-1] and not out[-1].startswith(("#", "-"))
                and prev_y1 is not None
                and (line.y0 - prev_y1) < median_h * 0.7):
            out[-1] = out[-1] + " " + line.text
        else:
            out.append(line.text)

        prev_y1 = line.y1

    return "\n".join(out).strip() + "\n"