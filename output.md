# Example Responses

Two example queries run against the Unofficial Guide (`app.py` → `generate_response`).
Answers are grounded **only** in the retrieved student-discussion and blog chunks, and
the **Sources** list is built programmatically from chunk metadata (it does not depend on
the LLM remembering to cite).

---

## Example 1 — In-scope query (grounded answer with source attribution)

**Query:** What specific reasons do students mention for finding organic chemistry difficult?

**Response:**

According to the passages, students find organic chemistry difficult due to several reasons. One reason is the "High Volume of Memorization—With a Twist" [Blog], which requires students to memorize a large amount of content. Another reason is that organic chemistry demands a "constant integration of knowledge—both old and new—and rewards flexibility in thought over strict rules" [Blog], making it frustrating for students who are used to numeric calculations or rote memorization. Additionally, the jump from being tested on properties/characteristics of atoms/functional groups to having to implicitly use those properties in understanding organic chem concepts is also a hard part for students [Reddit].

---
**Sources** (this answer is grounded only in these):
- **[Blog]** Is Organic Chemistry Really the Hardest College Course? — https://www.novascholar.education/blog-posts/is-organic-chemistry-really-the-hardest-college-course
- **[Reddit]** In your experience, why do undergraduate students find organic chemistry a very hard subject? — https://www.reddit.com/r/OrganicChemistry/comments/1thnyk4/in_your_experience_why_do_undergraduate_students/

> **Note on attribution:** the answer cites sources inline (`[Blog]`, `[Reddit]`) and the
> bracketed labels map 1:1 to the **Sources** list above, which is generated in code from the
> retrieved chunks' metadata.

---

## Example 2 — Out-of-scope query (system refusal)

**Query:** How do I cook pasta?

**Response:**

I don't have enough information on that.

> **Why it refuses:** the retriever finds no chunk above the `MIN_SIMILARITY` (0.35) floor for
> this off-topic question, so the enforcement gate in `generate_response` returns the fixed
> refusal **before** the LLM is ever called — the model gets no chance to answer from its own
> general knowledge.
