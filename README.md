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

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | documents/central_park_map.md | Highly structured factual profiles outlining major geographic points of interest, architectural monuments, and lawn entry points. | <https://www.centralparknyc.org/locations> |
| 2 | documents/central_park_calendar.md | Highly structured factual events taking place in June 2026 | <https://www.centralparknyc.org/calendar> |
| 3 | documents/central_park_quiet_zones.md | Factual breakdown of designated quiet zones, including rules, hours, and nearby facilities for peaceful areas like the Ramble and Sheep Meadow. | <https://www.centralparknyc.org/locations?filters=quiet-zone> |
| 4 | documents/central_park_reviews.md | Conversational crowd-sourced feedback, sentiment analysis, and practical local advice about Central Park's crowds, loops, and restroom conditions. |Google Maps Reviews |
| 5 | documents/prospect_park_map.md | Structural directory outlining landmarks, points of interest, playgrounds, food carts, and official facilities throughout Prospect Park. | <https://www.prospectpark.org/visit-the-park/park-map/> |
| 6 | documents/prospect_park_calendar.md | Chronological guide to scheduled public events, activities, seasonal food festivals, and venue rentals in Prospect Park for June 2026. | <https://www.prospectpark.org/events/> |
| 7 | documents/prospect_park_reviews.md | Conversational community perspectives, running tips, and blunt visitor reviews regarding Brooklyn’s backyard crowd levels and park upkeep. | Google Maps and TripAdvisor |
| 8 | documents/central_vs_prospect.md | Comparative running log and community dialogue evaluating the loop layout, topography, shade coverage, and athlete subcultures of both parks. | <https://www.reddit.com/r/RunNYC/comments/1dihsy9/running_in_central_park_vs_prospect_park/> |
| 9 | documents/ny_times.md | An archived editorial debate piece featuring deep analysis, historic design context, and contrasting local arguments on the architectural brilliance of both parks. | <https://www.nytimes.com/2010/07/11/nyregion/11parks.html> |
| 10 | documents/prospect_and_central_zoo.md | Focused data compiling information regarding the wildlife facilities and visitor spaces inside the dedicated park zoos. | <https://prospectparkzoo.com/> <https://centralparkzoo.com/> |
| 11 | documents/zoo_vs_zoo.md | Google reviews 

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 1200

**Overlap:** 200

**Why these choices fit your documents:** I realized that 300 characters completely cut off the long factual history about the two parks. Most of the human reviews were well over 300 characters as well. Because I had long dense paragprahs I decided to make the chunk size 1200 which handeled the mixture of long dense paragraphs better as well as the long narrative reviews. It helped keep relevant information together

**Final chunk count:** 112 Chunks

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:** 7 

**Production tradeoff reflection:**
If we were deploying this application for thousands of real New Yorkers and cost was not a constraint, we would trade our lightweight `all-MiniLM-L6-v2` local model for a commercial, high-dimensional model like OpenAI's `text-embedding-3-large` or Cohere's `embed-english-v3.0`, while weighing four critical engineering dimensions:

1. **Semantic Accuracy & Crowding Resistance (Domain Specificity):** 
Our current model outputs 384-dimensional vectors. While blazingly fast, it struggles with "semantic crowding"—meaning it pulls unstructured, highly conversational human reviews (e.g., Yelp/Reddit files mentioning the word "quiet") instead of our hard factual headers from `central_park_quiet_zones.md`. Moving to a 3,072-dimensional model would significantly compress more subtle semantic math nuances, letting the database easily differentiate between someone *wishing* for quiet in a review versus an *officially designated* municipal quiet zone.
2. **Context Window Limitations:** 
`all-MiniLM-L6-v2` is strictly capped at a 256-token context window. Any text chunk sent to it that exceeds this hard limit gets aggressively truncated, losing all subsequent sentences from the vector calculation. In production, upgrading to an embedding model with an 8k or 96k context window would let us capture entire historical park files as unified contextual units without breaking structural tables or calendar blocks at arbitrary character marks.
3. **Latency vs. Resource Overhead:** 
Our current model runs completely locally in-memory, boasting sub-millisecond retrieval latency because it doesn't leave our file system. Moving to a commercial cloud API introduces HTTP network round-trip overhead (potentially adding 50–200ms of latency per user query). For a live chatbot, we would need to decide if the massive leap in search accuracy is worth slowing down the user's instantaneous chat experience.
4. **Multilingual Ingestion Support:** 
Central Park and Prospect Park welcome millions of international tourists annually. Our current English-only model fails completely if a global traveler inputs a query in Spanish, Bengali, or Mandarin. Upgrading to a specialized multilingual embedding model would map cross-lingual queries to our English Markdown documents flawlessly, ensuring equal accessibility for non-native English speakers.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** "role": "system",
            "content": """
            ASK: Using only the grounded information provided in the information below, answer the user's question and cite the source.
            RULES: {retrieved_chunks}
            CONSTRAINTS: If the provided rules do not contain enough information to answer the user's question confidently, do not attempt to guess or answer. Instead, state that you do not know and ask the user a clarifying question.
            EXAMPLE OUTPUT: "According to the Central Park Location Directory there are 8 official quiet zones... [Source: Cental_Park_Quiet_Zones.md]"""

**How source attribution is surfaced in the response:** It is pulled from the metadata and appended to each chunk.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| ID | Question | Expected Answer / Context | Chatbot Response | Relevance | Accuracy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Is Prospect Park or Central Park better to run in? | Depending on views and more shade, central park ranks higher early in the morning. If you want peace and quiet without crowds to worry about people prefer Prospect Park. | According to the Reddit Review Conglomeration, Prospect Park is considered a more chill environment for runners, with minimal tourists and no horse carriages or poo to worry about, making it a potentially better option for running, especially during early evening hours [Source: Reddit Review Conglomeration, https://www.reddit.com/r/RunNYC/comments/1dihsy9/running_in_central_park_vs_prospect_park/]. However, it's also stated that neither park is better than the other for running. To provide a more definitive answer, could you please clarify what specific factors you consider most important when choosing a park for running (e.g. scenery, safety, crowd level)? | Relevant | Accurate |
| **2** | What can I do in Prospect Park? | The park has a number of destinations that will appeal to all ages and interests. Explore the menu for some of the most popular places to go in Prospect Park.<br>Carousel<br>LeFrak Center at Lakeside<br>Lefferts Historic House<br>Parade Ground<br>Playgrounds<br>Prospect Park Zoo<br>Park Drive<br>Tennis Center | According to the Yelp, Google Maps, and TripAdvisor Review Conglomeration, in Prospect Park, you can walk on scenic paths, rent boats on the lake, visit playgrounds and open spaces for kids, have a picnic, and use the dog runs as it is very dog-friendly [Source: Yelp, Google Maps, and TripAdvisor Review Conglomeration]. Additionally, according to Prospect Park Events + Activities, the park offers party rooms, picnic tables, and a splash pad [Source: Prospect Park Events + Activities]. | Relevant | Accurate |
| **3** | How many quiet zones are there in Central Park? | 8 according to central_park_quiet_zones.md | *[Blank or Flawed Initial Retrieval Step Output]* | Relevant | Partially accurate |
| **4** | What are the ticket prices for the Central Park Zoo? | Adult (13 & over): $22.95<br>Senior (65 & over): $18.95<br>Child (3 - 12): $16.95<br>Child (2 & under): FREE | The provided information does not contain the ticket prices for the Central Park Zoo. However, it does mention the ticket prices for the Prospect Park Zoo and a price of $22.95 for adults at one of the zoos in 2026, but it is not specified which zoo. [Source: Prospect Park Zoo vs Central Park Zoo]<br><br>To answer your question accurately, I would need more information about the ticket prices at the Central Park Zoo. Can you please provide more context or clarify which specific information you are looking for regarding the Central Park Zoo ticket prices? | Relevant | Partially Accurate |
| **5** | What are the ticket prices for the Prospect Park Zoo? | br><br>Adult (13 & over): $10.95<br>Senior (65 & over): $8.95<br>Child (3 - 12): $7.95<br>Child (2 & under): FREE<br> | According to the provided text, the ticket prices for the Prospect Park Zoo are as follows:<br><br>Adult (13 & over): $10.95<br>Senior (65 & over): $8.95<br>Child (3 - 12): $7.95<br>Child (2 & under): FREE<br>[Source: Prospect Park Zoo and Central Park Zoo] | Relevant | Accurate |

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

**Question that failed:** How many quiet zones are there in central park?

**What the system returned:** According to the provided information, there is only one officially mentioned quiet zone in Central Park, which is Sheep Meadow [Source: Central Park Quiet Zones]. However, the information does not provide a comprehensive list of all quiet zones in the park. Therefore, I do not know the total number of quiet zones in Central Park. Can you please provide more context or clarify what you are looking for?

**Root cause (tied to a specific pipeline stage):**  It has to be with the ingestion and retrieval step. I realized the issue is the embedding is storing irrelevant review documents that are associated with the word "quiet", such as "crowd", "peace" etc, higher up in n_results and because of that the rest of the actual relevant data in central_park_quiet_zones.md gets burried underneath a lot of ranks.

**What you would change to fix it:** The document was long which is why I changed the chunking strategy to 1200 chars and overlap to 200. However, I realized that's not the issue and more about words associated with "quiet".

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The spec helped me plan out the documents and chunking strategy. It established a clear, symmetrical blueprint for the datasets across both Central Park and Prospect Park, which kept the project structured from the start. Having this layout predefined allowed me to build out the database collections quickly without guessing how files would relate to one another.

**One way your implementation diverged from the spec, and why:** I ended up changing my chunking strategy from what was taught in the lab because my paragraphs of information were a lot more dense. So I increased the char count from 300 to 1200. The smaller 300-character window was aggressively fracturing factual lists, structured tables, and event calendars mid-sentence, which caused the system to completely lose its core context. Moving to 1200 characters with a 200-character overlap kept these high-density blocks unified, preventing data loss and providing a much more accurate retrieval pool for the language model.


---
## DEMO 
<img src="/rag.gif" width="600" alt="Project Demo">
---

## AI Usage

**Instance 1**

- *What I gave the AI:* I provided the initial code snippet of my `embed_and_store(chunks)` function alongside an error log showing that my test query in `retriever.py` was returning an empty list (`[]`). I asked the AI to identify what was wrong with my parallel dictionary setup and why my retrieval was failing.
- *What it produced:* The AI pointed out that my vector database was functionally empty because I hadn't run the full ingestion pipeline yet.
- *What I changed or overrode:* I followed the AI's diagnostic advice to fix the startup issue.

**Instance 2**

- *What I gave the AI:* I provided a raw Markdown block containing the ticket price tables for both the Central Park and Prospect Park Zoos, along with a failing chatbot response. The chatbot was hallucinating that Central Park's prices "were not explicitly stated" because it got confused by the nearby Prospect Park Zoo numbers. 
- *What it produced:* The AI diagnosed the error as "Context Pollution" caused by my sliding-window text splitter slicing the loosely spaced Markdown text in half. This separated the "Central Park Zoo" heading into one chunk and the raw price values into a completely different chunk. It suggested a tightly packed bulleted list layout to keep the labels and values locked together inside a single vector window.
- *What I changed or overrode:* I accepted the structural markdown layout changes for both zoo files to ensure clean data binding. However, instead of just fixing the text documents as suggested, I implemented an architectural override in my pipeline's configuration settings. I increased my `N_RESULTS` retrieval threshold from `5` to `7` to expand the LLM's context window. This forced the system to pull deeper sections of my documents concurrently, ensuring that list-based queries could access all relevant location data without being choked out by shorter conversational review files. Still did not fix the issue completely, but I got a grounded and highly relevant response that still points the user to official URL.
