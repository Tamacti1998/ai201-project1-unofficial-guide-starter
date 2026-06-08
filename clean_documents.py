"""
Clean the saved source .txt files in place: strip everything that isn't
substantive content (nav menus, cookie/brochure banners, author bios, tables of
contents, footers, related-article cards, share/CTA buttons), while keeping the
actual article text, opinions, and student discussion.

The Title:/Source: header on each file is always preserved. Reddit files are
already clean (pure comment text) and pass through almost untouched.

Run after fetch_sources.py:  python3 clean_documents.py
"""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "documents"

# --- Shared filters applied to every document body --------------------------

# A line is junk if, after stripping, it is empty or only punctuation/symbols
# (e.g. ".", "|", ",", zero-width joiners) ...
_ONLY_SYMBOLS = re.compile(r"^[\s\W_‍]*$")
# ... or a lone number / table-of-contents section number ("1", "6.1", "10.1.1") ...
_SECTION_NUM = re.compile(r"^\d+(\.\d+)*\.?$")
# ... or a relative timestamp ("2 years ago", "5 months ago").
_TIMESTAMP = re.compile(r"(?i)^\d+\s+(year|month|week|day|hour|minute)s?\s+ago$")

# Exact boilerplate lines (compared case-insensitively after stripping).
JUNK_LINES = {
    "image", "show", "contents", "table of contents", "back to top",
    "read now", "read more", "minute read", "about the author",
    "related articles", "browse all posts", "related", "tags:",
    "privacy policy", "terms and conditions", "skip to main content",
    "my feed", "meet a mentor", "download the programs brochure",
    "get our programs brochure", "begin your journey to exceptional projects",
    "schedule a consultation call", "schedule a consulattion call",
    "students@novascholar.org", "our services", "pricing", "contact",
    "homework help", "exam help", "exam support", "full-class support",
    "full class management", "homework & lab help", "homework & labs",
    "full-class management", "homework & labs help", "additional resources:",
}

# Promotional CTA phrases (mostly the essay-mill page, doc 08). A line containing
# any of these is dropped as advertising rather than substantive content.
PROMO_SUBSTRINGS = [
    "homework help", "exam help", "exam support", "full-class support",
    "full class support", "class-wide support", "organic chemistry help",
    "targeted orgo help", "get chemistry homework help", "pay someone to take",
    "a/b guarantee", "request a quote", "custom quote", "our team can take",
    "we handle platforms", "we absorb the grind", "we can handle the routine",
    "trust human experts", "strategic help", "outsource", "outsourcing",
    "protect your gpa", "protecting your gpa", "protecting gpa",
    "is biology hard?",
]

# --- Per-file positional trims ----------------------------------------------
# trim_start: drop every line before the first line containing this substring.
# trim_end:   drop every line after the first line containing this substring.
# cuts:       list of (start, end) -> drop each block from the line containing
#             `start` up to (not including) the next line containing `end`.
# Markers are matched case-sensitively to stay precise.
PER_FILE = {
    "04_illinois_sos_organic_chemistry": {
        "trim_start": "As an avid reddit user",
        "trim_end": "To find out more, visit",
    },
    "05_vanderbilt_is_orgo_really_that_hard": {
        "trim_start": "I was nervous for organic chemistry",
        "trim_end": "you get out of it what you put into it",
    },
    "06_novascholar_hardest_college_course": {
        "trim_start": "Mention",
        "trim_end": "your place in it",
    },
    "07_willpeachmd_is_orgo_hard": {
        "trim_end": "Work hard and you can definitely get there!",
        "cuts": [("Contents", "a brief rundown of why organic chemistry")],
    },
    "08_finishmymathclass_why_orgo_feels_brutal": {
        "trim_start": "Organic Chemistry has the highest failure rates",
        "trim_end": "Additional Resources",
        "cuts": [
            ("Table of Contents", "has a reputation that precedes it"),
            ("Should You Pay Someone for Help with Organic Chemistry?",
             "FAQs: Organic Chemistry Difficulty"),
        ],
    },
    "09_collegevine_one_of_hardest_classes": {
        "trim_start": "As I'm considering a pre-med track",
        "trim_end": "how well you adapt your study habits to the demands of the class",
    },
}


def _apply_positional(lines, cfg):
    for start_sub, end_sub in cfg.get("cuts", []):
        start = next((i for i, l in enumerate(lines) if start_sub in l), None)
        if start is not None:
            end = next((i for i in range(start + 1, len(lines))
                        if end_sub in lines[i]), len(lines))
            lines = lines[:start] + lines[end:]
    if "trim_start" in cfg:
        i = next((i for i, l in enumerate(lines) if cfg["trim_start"] in l), None)
        if i is not None:
            lines = lines[i:]
    if "trim_end" in cfg:
        i = next((i for i, l in enumerate(lines) if cfg["trim_end"] in l), None)
        if i is not None:
            lines = lines[: i + 1]
    return lines


def _is_junk(line: str, drop_promo: bool) -> bool:
    s = line.strip()
    if _ONLY_SYMBOLS.match(s) or _SECTION_NUM.match(s) or _TIMESTAMP.match(s):
        return True
    low = s.lower()
    if low in JUNK_LINES:
        return True
    return drop_promo and any(p in low for p in PROMO_SUBSTRINGS)


def clean_file(path: Path) -> tuple:
    raw = path.read_text(encoding="utf-8")
    header, _, body = raw.partition("\n\n")
    if not (header.startswith("Title:") or header.startswith("Source:")):
        header, body = "", raw

    lines = body.splitlines()
    before = len([l for l in lines if l.strip()])

    cfg = PER_FILE.get(path.stem)
    if cfg:
        lines = _apply_positional(lines, cfg)

    # Promo-CTA filtering targets the marketing-heavy blogs only; Reddit comment
    # text is left alone so a comment that happens to say "exam help" survives.
    drop_promo = "reddit" not in path.stem
    kept = [l for l in lines if l.strip() and not _is_junk(l, drop_promo)]
    after = len(kept)

    cleaned = (header + "\n\n" if header else "") + "\n".join(kept) + "\n"
    path.write_text(cleaned, encoding="utf-8")
    return before, after


def main() -> None:
    print(f"Cleaning .txt files in {DOCS_DIR}\n")
    for path in sorted(DOCS_DIR.glob("*.txt")):
        before, after = clean_file(path)
        removed = before - after
        flag = "" if removed else "  (already clean)"
        print(f"  {path.name}: {before} -> {after} lines  (-{removed}){flag}")


if __name__ == "__main__":
    main()
