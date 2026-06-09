# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

**Domain:** College Students' Attitudes Toward Organic Chemistry

**Domain Summary:**

This guide consolidates authentic student experiences and attitudes about organic chemistry from scattered Reddit threads, blogs, and forums into one resource. Student perspectives on why the course is difficult, how to succeed, and what to realistically expect are currently hard for incoming students to find, making this peer-to-peer knowledge valuable and otherwise inaccessible.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Title | Source | URL/Path |
|---|-------|-------------|---------|
| 1 | In your experience, why do undergraduate students find organic chemistry a very hard subject? | Reddit | https://www.reddit.com/r/OrganicChemistry/comments/1thnyk4/in_your_experience_why_do_undergraduate_students/ |
| 2 | Is organic chemistry that hard? | Reddit | https://www.reddit.com/r/ChemicalEngineering/comments/1lz3h9s |
| 3 | Hardest Chemistry Subjects for Chemistry Grads | Reddit | https://www.reddit.com/r/chemistry/comments/1smu4rj/hardest_chemistry_subjects_for_chemistry_grads/ |
| 4 | SOS: Organic Chemistry! | University of Illinois Student Ambassador Blog | https://scs.illinois.edu/student-ambassadors-blog/sos-organic-chemistry-0 |
| 5 | Is Organic Chemistry Really That Hard? | Vanderbilt University Student Blog | https://admissions.vanderbilt.edu/insidedores/2021/02/is-organic-chemistry-really-that-hard/ |
| 6 | Is Organic Chemistry Really the Hardest College Course? | Nova Scholar | https://www.novascholar.education/blog-posts/is-organic-chemistry-really-the-hardest-college-course |
| 7 | Is Organic Chemistry Hard? (Beginner Tips!) | WillPeachMD | https://willpeachmd.com/is-organic-chemistry-hard |
| 8 | Is Organic Chemistry Hard? Why Orgo Feels Brutal (and What You Can Do) | Blog article | https://finishmymathclass.com/is-organic-chemistry-hard/ |
| 9 | Is Organic Chemistry really one of the hardest college classes? | CollegeVine Forum | https://www.collegevine.com/faq/94111/is-organic-chemistry-really-one-of-the-hardest-college-classes |
| 10 | How hard is Organic Chemistry, really? | Reddit | https://www.reddit.com/r/premed/comments/5hca0e/how_hard_is_organic_chemistry_really/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
300 characters

**Overlap:**
50 characters

**Why these choices fit your documents:**
Reddit comments and blog paragraphs naturally fit this range. Large enough to capture a complete thought, small enough that one chunk = one student voice. Low overlap — unlike technical docs, student opinions don't need repetition at boundaries. Overlap just prevents semantic breaks.

**Final chunk count:**
799 chunks across 10 cleaned documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 (via sentence-transformers), 384-dim. Fast and lightweight (~80MB), with strong general-purpose semantic quality that handles short student opinions well — most of my chunks are ~270 characters, comfortably under the model's 256-token window, so its shorter context length isn't a constraint here.

**Production tradeoff reflection:**
If cost weren't a constraint, I'd move to all-mpnet-base-v2 (768-dim) or a domain-specialized model fine-tuned on education forums + Reddit discussions. Tradeoffs I'd weigh: accuracy on domain-specific text (mpnet captures more nuance — "hard," "struggle," "stressful" carry specific meaning in a chemistry context that a general model can blur) and context length (for embedding longer Reddit comments intact), against latency (mpnet is meaningfully slower) and download/serving cost. Multilingual support isn't needed for US college students. For this corpus of short, English opinions, MiniLM's speed/size win out; for a production system, I'd accept the latency hit for mpnet's accuracy.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
