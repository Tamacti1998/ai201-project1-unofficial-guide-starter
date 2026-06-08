# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
**Domain:** College Students' Attitudes Toward Organic Chemistry

**Domain Summary:**

This unofficial guide compiles college students' authentic experiences and attitudes toward organic chemistry, a notoriously difficult course that shapes many students' career decisions. Student perspectives on why organic chemistry is hard, how to succeed, and what to expect are currently scattered across Reddit threads, university blogs, and forums—making it difficult for incoming students to find candid, peer-to-peer advice in one place. This guide consolidates these voices to give prospective and current students a realistic, honest view of the course and practical strategies from those who've lived through it.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->


| # | Title | Source | URL/Path | Description |
|---|-------|-------------|---------|-------------|
| 1 | In your experience, why do undergraduate students find organic chemistry a very hard subject? | Reddit | https://www.reddit.com/r/OrganicChemistry/comments/1thnyk4/in_your_experience_why_do_undergraduate_students/ | Students, instructors, and chemists discuss why organic chemistry is difficult, highlighting issues such as memorization, spatial reasoning, and ineffective teaching methods |
| 2 | Is organic chemistry that hard? | Reddit | https://www.reddit.com/r/ChemicalEngineering/comments/1lz3h9s | Students share whether organic chemistry deserves its reputation as one of the hardest college courses and compare it with other engineering classes |
| 3 | Hardest Chemistry Subjects for Chemistry Grads | Reddit | https://www.reddit.com/r/chemistry/comments/1smu4rj/hardest_chemistry_subjects_for_chemistry_grads/ | Chemistry students and graduates debate whether organic chemistry is the hardest subject in chemistry and compare it with physical and quantum chemistry |
| 4 | SOS: Organic Chemistry! | University of Illinois Student Ambassador Blog | https://scs.illinois.edu/student-ambassadors-blog/sos-organic-chemistry-0 | A student blogger discusses common struggles in organic chemistry and explains why memorization alone is not enough for success |
| 5 | Is Organic Chemistry Really That Hard? | Vanderbilt University Student Blog | https://admissions.vanderbilt.edu/insidedores/2021/02/is-organic-chemistry-really-that-hard/ | A Vanderbilt student reflects on fears surrounding organic chemistry and explains how expectations differed from the actual course experience |
| 6 | Is Organic Chemistry Really the Hardest College Course? | Nova Scholar | https://www.novascholar.education/blog-posts/is-organic-chemistry-really-the-hardest-college-course | Reviews why organic chemistry is viewed as a "weed-out" course and discusses the experiences of students with different learning styles |
| 7 | Is Organic Chemistry Hard? (Beginner Tips!) | WillPeachMD | https://willpeachmd.com/is-organic-chemistry-hard | A medical student and educator discusses failure rates, workload, and strategies students use to succeed in organic chemistry |
| 8 | Is Organic Chemistry Hard? Why Orgo Feels Brutal (and What You Can Do) | Blog article | https://finishmymathclass.com/is-organic-chemistry-hard/ | Compiles common student complaints about exams, labs, and pacing, with examples of students' experiences. |
| 9 | Is Organic Chemistry really one of the hardest college classes? | CollegeVine Forum | https://www.collegevine.com/faq/94111/is-organic-chemistry-really-one-of-the-hardest-college-classes | Students considering pre-med discuss the reputation of organic chemistry and receive advice from those who have completed the course |
| 10 | How hard is Organic Chemistry, really? | Reddit | https://www.reddit.com/r/premed/comments/5hca0e/how_hard_is_organic_chemistry_really/ | Pre-med students share their experiences with organic chemistry, discussing workload, study habits, and the balance between memorization and conceptual understanding |

---
## Source Collection Notes

- **Collection Date:** 7th June 2026
- **Total Sources:** 10
- **Coverage:** Student perceptions of difficulty, reasons why organic chemistry is hard (memorization, spatial reasoning, teaching methods), comparison with other courses, student fears and expectations vs. reality, learning strategies, study habits, lab and exam experiences, the "weed-out" course reputation, diverse learning styles, workload and time management, pre-med student perspectives

---
## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
