# Retrieval Test Results

These results come from running `test_retrieval.py`, which issues each Evaluation Plan
query (from `planning.md`) against the retriever and prints the top-k chunks with their
cosine **distance** scores.

- **distance** = `1 - similarity` → `0.0` means identical, higher means less related.
- **similarity** = the score stored by `retriever.py` (`1 - distance`).
- Embedding model: `all-MiniLM-L6-v2`.

---

## Query 1: What specific reasons do students mention for finding organic chemistry difficult?

| # | distance | similarity | source | chunk | type |
|---|----------|-----------|--------|-------|------|
| 1 | 0.1753 | 0.8247 | 06_novascholar_hardest_college_course | #99 | blog |
| 2 | 0.1856 | 0.8144 | 06_novascholar_hardest_college_course | #42 | blog |
| 3 | 0.1894 | 0.8106 | 06_novascholar_hardest_college_course | #25 | blog |
| 4 | 0.2084 | 0.7916 | 06_novascholar_hardest_college_course | #49 | blog |
| 5 | 0.2153 | 0.7847 | 01_reddit_why_undergrads_find_orgo_hard | #0 | reddit |

**Top chunk previews**

1. `…demanding study habits, and high expectations. But for many students, its difficulty isn't a deterrent—it's a defining experience. Organic chemistry is not just another science class; it's a milestone in STEM educati…`
2. `…that explains why organic chemistry is considered one of the most difficult courses in undergraduate science education. But here's the good news: these challenges can be met with the right strategies, resources, and mi…`
3. `…to students who excel in other areas of science. Let's take a closer look at the main factors that make organic chemistry uniquely difficult: High Volume of Memorization—With a Twist Organic chemistry is often a studen…`
4. `…find organic chemistry particularly frustrating. Unlike courses that center around numeric calculations or rote memorization, organic chemistry demands a constant integration of knowledge—both old and new—and rewards f…`
5. `…As a tutor for the topic I think the jump from being tested on different properties/characteristics of atoms/functional groups to having to constantly, implicitly use those properties in understanding organic chem concep…`

**Why these chunks are relevant**

This query asks for the *reasons* organic chemistry is hard, and every returned chunk
speaks directly to causes of difficulty rather than tangential topics. Chunk #3 is the
strongest match in content — it literally introduces "the main factors that make organic
chemistry uniquely difficult" and names "High Volume of Memorization—With a Twist," which
is exactly the kind of specific reason the query targets. Chunk #4 adds another concrete
reason (it "demands a constant integration of knowledge—both old and new"), and chunk #5,
the only Reddit result, supplies a student/tutor's first-hand account of the conceptual
jump from memorizing atom properties to *applying* them implicitly. The low distance scores
(all ≤ 0.22) reflect strong semantic overlap, and the mix of one blog source plus a Reddit
voice shows the retriever is pulling both authoritative and lived-experience perspectives on
the same underlying question.

---

## Query 2: What study strategies do successful students recommend to improve performance in organic chemistry?

| # | distance | similarity | source | chunk | type |
|---|----------|-----------|--------|-------|------|
| 1 | 0.2338 | 0.7662 | 06_novascholar_hardest_college_course | #59 | blog |
| 2 | 0.2593 | 0.7407 | 01_reddit_why_undergrads_find_orgo_hard | #240 | reddit |
| 3 | 0.2647 | 0.7353 | 09_collegevine_one_of_hardest_classes | #5 | blog |
| 4 | 0.2712 | 0.7288 | 06_novascholar_hardest_college_course | #56 | blog |
| 5 | 0.2929 | 0.7071 | 06_novascholar_hardest_college_course | #53 | blog |

**Top chunk previews**

1. `…in a way that matches the demands of the subject. Because organic chemistry blends memorization, logic, and spatial reasoning, students must approach it differently from other STEM classes. Here are five evidence-based…`
2. `…try looks almost an entirely different discipline. Most general chemistry courses in my opinion do not prepare students well for organic chemistry. Is it also bad studying habits by students? If so what would be good stu…`
3. `…Chemistry largely depends on how you approach it. Successful students typically space out their studying, do a lot of practice problems, and keep up with the material as it's being taught, rather than catching up later.…`
4. `…for any field rooted in science and problem-solving. In the next section, we'll explore the strategies that successful students use to not only survive but thrive in organic chemistry—and how you can develop the habits tha…`
5. `…hybrid challenge that can feel especially intense for students not used to juggling so many ways of thinking in a single class. A Course That Rewards Persistence and Growth…`

**Why these chunks are relevant**

The query is about *recommended study strategies*, and the top results converge on actionable
advice. Chunk #3 (CollegeVine) is the most on-target: it names concrete, recommended habits —
"space out their studying, do a lot of practice problems, and keep up with the material as
it's being taught, rather than catching up later." Chunk #1 sets up "five evidence-based"
strategies and explains *why* the approach must differ ("blends memorization, logic, and
spatial reasoning"), and chunk #4 explicitly previews "the strategies that successful students
use to not only survive but thrive." Chunk #2 (Reddit) is slightly weaker but still relevant
because it frames the question of "good study habits" from a student's discussion thread.
Distances here are a bit higher than Query 1 (0.23–0.29), which is expected: strategy advice
is spread across more sources and phrased more variably than the "why it's hard" content, so
the semantic match is a little looser while still clearly topical.

---

## Query 3: Based on student discussions, what determines how hard organic chemistry feels: the course itself or the instructor?

| # | distance | similarity | source | chunk | type |
|---|----------|-----------|--------|-------|------|
| 1 | 0.1777 | 0.8223 | 06_novascholar_hardest_college_course | #44 | blog |
| 2 | 0.2033 | 0.7967 | 06_novascholar_hardest_college_course | #43 | blog |
| 3 | 0.2130 | 0.7870 | 01_reddit_why_undergrads_find_orgo_hard | #219 | reddit |
| 4 | 0.2256 | 0.7744 | 02_reddit_is_orgo_that_hard | #10 | reddit |
| 5 | 0.2297 | 0.7703 | 01_reddit_why_undergrads_find_orgo_hard | #224 | reddit |

**Top chunk previews**

1. `…Is Organic Chemistry the Hardest Course in College? Whether or not organic chemistry is the "hardest" course in college is subjective—and depends greatly on the individual student's strengths, background, and learning sty…`
2. `…with the right strategies, resources, and mindset. In the next section, we'll explore actionable techniques that students can use to succeed—and even thrive—in organic chemistry, no matter their background or starting po…`
3. `…well, I guess you get dealt a bad hand sometimes. At least you got through it well enough to tutor. I don't think organic is harder than any other chemistry subject for a chemistry major. Maybe for students in other majo…`
4. `…that the topics are just more challenging to grasp. However, organic chemistry is harder in the sense that it is like taking 10 courses at once. I like to describe it as an infinite amount of content that you have to memo…`
5. `…as they want to versus the typical standards for a field. I agree that a lot of it is instructor-dependent. Which was the harder subject for you, organic chemistry or physical chemistry and why? I took a traditional phys…`

**Why these chunks are relevant**

This is a comparative/causal question (course vs. instructor), and the retriever does a good
job surfacing the discussion that distinguishes the two. Chunk #5 is the single most relevant
result for the *instructor* side — it explicitly states "I agree that a lot of it is
instructor-dependent," directly answering one half of the question. On the *course* side,
chunk #1 argues difficulty is "subjective—and depends greatly on the individual student's
strengths, background, and learning style," and chunk #4 characterizes the inherent course
load ("like taking 10 courses at once… an infinite amount of content"). Notably, three of the
five hits are Reddit chunks, which aligns with the phrase "based on student discussions" in
the query — the retriever favored the conversational sources where students actually debate
course-vs-instructor, rather than the more polished blog explainers. The tight distances
(0.18–0.23) confirm strong topical alignment.
