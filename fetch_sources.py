"""
One-time fetcher: download the 10 sources and save each as a .txt file in documents/.

Run once to populate documents/. After that, ingest.py loads from disk instead of
hitting the network, so the corpus is reproducible and Reddit's JS wall is avoided.
"""

import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DOCS_DIR = Path(__file__).parent / "documents"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

# (filename, title, url) — order matches planning.md / README source table.
SOURCES = [
    ("01_reddit_why_undergrads_find_orgo_hard", "In your experience, why do undergraduate students find organic chemistry a very hard subject?", "https://www.reddit.com/r/OrganicChemistry/comments/1thnyk4/in_your_experience_why_do_undergraduate_students/"),
    ("02_reddit_is_orgo_that_hard", "Is organic chemistry that hard?", "https://www.reddit.com/r/ChemicalEngineering/comments/1lz3h9s"),
    ("03_reddit_hardest_chemistry_subjects", "Hardest Chemistry Subjects for Chemistry Grads", "https://www.reddit.com/r/chemistry/comments/1smu4rj/hardest_chemistry_subjects_for_chemistry_grads/"),
    ("04_illinois_sos_organic_chemistry", "SOS: Organic Chemistry!", "https://scs.illinois.edu/student-ambassadors-blog/sos-organic-chemistry-0"),
    ("05_vanderbilt_is_orgo_really_that_hard", "Is Organic Chemistry Really That Hard?", "https://admissions.vanderbilt.edu/insidedores/2021/02/is-organic-chemistry-really-that-hard/"),
    ("06_novascholar_hardest_college_course", "Is Organic Chemistry Really the Hardest College Course?", "https://www.novascholar.education/blog-posts/is-organic-chemistry-really-the-hardest-college-course"),
    ("07_willpeachmd_is_orgo_hard", "Is Organic Chemistry Hard? (Beginner Tips!)", "https://willpeachmd.com/is-organic-chemistry-hard"),
    ("08_finishmymathclass_why_orgo_feels_brutal", "Is Organic Chemistry Hard? Why Orgo Feels Brutal (and What You Can Do)", "https://finishmymathclass.com/is-organic-chemistry-hard/"),
    ("09_collegevine_one_of_hardest_classes", "Is Organic Chemistry really one of the hardest college classes?", "https://www.collegevine.com/faq/94111/is-organic-chemistry-really-one-of-the-hardest-college-classes"),
    ("10_reddit_how_hard_is_orgo_really", "How hard is Organic Chemistry, really?", "https://www.reddit.com/r/premed/comments/5hca0e/how_hard_is_organic_chemistry_really/"),
]


def fetch(url: str) -> BeautifulSoup:
    # Reddit's modern site is JS-only; old.reddit.com still serves static HTML.
    if "reddit.com" in url:
        url = url.replace("www.reddit.com", "old.reddit.com").replace("//reddit.com", "//old.reddit.com")
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.content, "html.parser")


def extract_reddit(soup: BeautifulSoup) -> str:
    # Drop the sidebar so its FAQ/rules boilerplate doesn't get scraped as content.
    for side in soup.find_all("div", class_="side"):
        side.decompose()

    parts = []
    # The original post body and every comment live in div.md blocks within the
    # main listing (sitetable) and the comment area.
    scopes = soup.find_all("div", class_="commentarea") + soup.find_all("div", id="siteTable")
    seen = set()
    for scope in scopes:
        for md in scope.find_all("div", class_="md"):
            text = md.get_text(separator=" ", strip=True)
            if text and text not in seen:
                seen.add(text)
                parts.append(text)
    return "\n\n".join(parts)


def extract_blog(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "meta", "noscript", "header", "footer", "nav", "form"]):
        tag.decompose()
    main = soup.find("article") or soup.find("main") or soup.find("div", class_="content")
    node = main or soup.body
    return node.get_text(separator="\n", strip=True) if node else ""


def main() -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    print(f"Saving {len(SOURCES)} sources to {DOCS_DIR}\n")

    for fname, title, url in SOURCES:
        try:
            soup = fetch(url)
            text = extract_reddit(soup) if "reddit.com" in url else extract_blog(soup)
            text = re.sub(r"\n{3,}", "\n\n", text).strip()

            if len(text) < 100:
                print(f"⚠ {fname}: only {len(text)} chars extracted — check selectors")
                continue

            out = DOCS_DIR / f"{fname}.txt"
            # Header preserves attribution; ingest.py strips the URL line during cleaning.
            out.write_text(f"Title: {title}\nSource: {url}\n\n{text}\n", encoding="utf-8")
            print(f"✓ {out.name} ({len(text)} chars)")
        except Exception as e:
            print(f"✗ {fname}: {e}")

        time.sleep(2)  # be polite to the servers


if __name__ == "__main__":
    main()
