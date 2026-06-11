# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
I chose to make a RAG about top 3 NYC parks. The reason for this, is to get hyper specific reviews, insider information, and community events about the most visited green spaces in NYC. This information can help people decide where to escape from the crowds, engage in physical activity inside these parks, and spend less time researching. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | documents/central_park_map.md | Highly structured factual profiles outlining major geographic points of interest, architectural monuments, and lawn entry points. | <https://www.centralparknyc.org/locations> |
| 2 | documents/central_park_calendar.md | Highly structured factual events taking place in June 2026 | <https://www.centralparknyc.org/calendar> |
| 3 | documents/central_park_quiet_zones.md | Factual breakdown of designated quiet zones, including rules, hours, and nearby facilities for peaceful areas like the Ramble and Sheep Meadow. | <https://www.centralparknyc.org/locations> |
| 4 | documents/central_park_reviews.md | Conversational crowd-sourced feedback, sentiment analysis, and practical local advice about Central Park's crowds, loops, and restroom conditions. |Google Maps Reviews |
| 5 | documents/prospect_park_map.md | Structural directory outlining landmarks, points of interest, playgrounds, food carts, and official facilities throughout Prospect Park. | <https://www.prospectpark.org/visit-the-park/park-map/> |
| 6 | documents/prospect_park_calendar.md | Chronological guide to scheduled public events, activities, seasonal food festivals, and venue rentals in Prospect Park for June 2026. | <https://www.prospectpark.org/events/> |
| 7 | documents/prospect_park_reviews.md | Conversational community perspectives, running tips, and blunt visitor reviews regarding Brooklyn’s backyard crowd levels and park upkeep. | Google Maps and TripAdvisor |
| 8 | documents/central_vs_prospect.md | Comparative running log and community dialogue evaluating the loop layout, topography, shade coverage, and athlete subcultures of both parks. | <https://www.reddit.com/r/RunNYC/comments/1dihsy9/running_in_central_park_vs_prospect_park/> |
| 9 | documents/ny_times.md | An archived editorial debate piece featuring deep analysis, historic design context, and contrasting local arguments on the architectural brilliance of both parks. | <https://www.nytimes.com/2010/07/11/nyregion/11parks.html> |
| 10 | documents/prospect_and_central_zoo.md | Focused data compiling information regarding the wildlife facilities and visitor spaces inside the dedicated park zoos. | <https://prospectparkzoo.com/> <https://centralparkzoo.com/> |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->



**Chunk size:** 300 tokens (approximately 1,200 characters)

**Overlap:** 50 tokens (approximately 200 characters)

**Reasoning:** 
Our corpus is highly heterogeneous, split symmetrically between two distinct document structures: highly structured, factual directories (such as `central_park_map.md` and `prospect_park_calendar.md`) and dense, conversational, multi-paragraph human reviews (such as `central_park_reviews.md` and `ny_times.md`). A uniform chunk size of 300 tokens with a 50-token overlap balances the unique retrieval needs of both archetypes.

1. **Handling Conversational Reviews & Narratives:** Public reviews from Reddit and Yelp are deeply contextual and often switch topics rapidly within a single paragraph (e.g., transitioning from a compliment about skyline views immediately into a warning about long restroom lines). A smaller chunk size (like 100 tokens) would sever these complaints from their spatial context, causing the RAG system to lose track of *which* specific park or landmark the user is critiquing. A 300-token window ensures that the entire user thought, sentiment, and specific location markers remain bound together in a single vector embedding.
2. **Preserving Structured Bullet Points:** For the programmatic files containing calendars and facility directories, the layout consists of compact, isolated bulleted blocks detailing event titles, times, and descriptions. A 300-token limit is wide enough to encapsulate 2 to 3 complete, consecutive event blocks or landmark profiles without awkwardly cutting off midway through an operational hours list.
3. **The Importance of the 50-Token Overlap:** The 50-token sliding window acts as a fail-safe against the "edge-case splitting problem." If an important piece of insider advice—such as a specific safety tip or crowd-evasion maneuver—happens to cross the boundary between two chunks, the overlap guarantees that the surrounding context is duplicated across both vectors, ensuring high semantic search relevance no matter where the text-splitter slices the document.

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
