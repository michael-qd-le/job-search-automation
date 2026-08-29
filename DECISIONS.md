# Decisions Log

A running record of significant decisions made while building this project, and the reasoning behind them — kept separate from the README so the README stays a clean current snapshot, while this captures the "why."

## MVP approach: scripts first, not a full web app
Chose plain Python scripts with no database or web framework for the first build, instead of the originally planned Next.js + Postgres stack. Reasoning: lower complexity while learning to code for the first time, faster feedback loop, and defers database/UI design decisions until the real shape of the data is actually known.

## Build order: riskiest integration first
Sequenced the build as environment setup → Gmail integration → AI classification → JobTech API → data layer → dashboard, rather than following a strict "Phase 1/2/3" label order. Reasoning: Gmail OAuth was the most uncertain, highest-risk piece (external API, authentication flow) — proving it works first meant every later step builds on a known-working foundation instead of discovering a blocker deep into the project.

## Job source scope: JobTech API only, LinkedIn and Indeed ruled out
Considered adding LinkedIn and Indeed as additional job sources. Both ruled out: LinkedIn has no viable self-serve API for individual developers (partner-program-only, opaque approval process) and scraping it violates their ToS with real account-ban risk. Indeed's public API was discontinued; remaining access is enterprise-partner-only or paid third-party scrapers. Decision: stay scoped to Arbetsförmedlingen's free, public JobTech API for v1, with paid enrichment sources noted as a possible future addition.

## Gmail scope: read-only access, least privilege
Requested only the `gmail.readonly` scope, not broader mailbox access. Reasoning: the tool only ever needs to read emails, never send/modify/delete — requesting minimum necessary access limits potential damage if credentials were ever compromised, and is easier to justify/explain.

## OAuth app kept in "Testing" mode
Left the Google Cloud OAuth consent screen in Testing status with a single test user (my own account), rather than pursuing Google's formal verification process. Reasoning: this is a single-user personal tool, not a public-facing app — verification is unnecessary overhead with no benefit here.

## Secrets excluded from git via .gitignore
`credentials.json` and `token.json` (both containing real, live credentials) are listed in `.gitignore` and were never committed. Reasoning: this repo is public on GitHub; committing real secrets would expose them permanently in the repo's history.

## Gmail search: broad keyword net, not precise filtering
The keyword search passed to Gmail's API is deliberately broad (many terms, OR'd together) rather than narrow. Reasoning: Gmail's search does literal text matching, not semantic understanding, so it can't reliably distinguish intent on its own. Precision is intentionally deferred to the Phase 2 AI classification step, which will read full context and correctly discard false positives — a broad net here only costs a little extra processing, not accuracy in the final result.

## Captured fields: sender, subject, date, snippet
For each matched email, the script extracts sender, subject, date, and a short snippet — not the full email body. Reasoning: these fields are the minimum needed for Phase 2 classification and a timeline-aware tracker later, without taking on the added complexity of parsing full MIME email bodies at this stage.

## LLM provider: switched to Google Gemini API instead of Anthropic
Originally scoped to use Anthropic's API, but Anthropic requires a payment method on file even to use free credits. Switched to Google's Gemini API (via Google AI Studio), which is genuinely free with no card required. Trade-offs accepted: free-tier prompts/responses may be used by Google to improve their products (relevant since this sends real email content), free-tier limits have been reduced before and aren't guaranteed to stay generous, and current rate limits (~1,000 requests/day) are fine for this project's personal scale but would need reassessing if usage grew significantly.


## Switched Gemini model to flash-lite due to free-tier daily quota
The standard gemini-3.5-flash model hit a hard daily cap of 20 requests on the free tier — enough for light testing but not for realistic use. Switched to gemini-3.5-flash-lite, which has a substantially higher free-tier quota and is still fully capable for a straightforward classification task like this one. Also added a 15-second pause between requests to stay under per-minute limits.


## Switched from email snippet to full email body for classification
Testing revealed the short Gmail snippet sometimes cut off before key classifying language (e.g., a rejection's actual "unfortunately" language appearing after the snippet's truncation point), causing misclassification. Added a get_body function that extracts and base64-decodes the full plain-text email body instead, giving the AI complete context. Confirmed improvement: subsequent test runs correctly caught rejections that snippet-only classification had missed.

## Added graceful fallback for expired OAuth tokens
Testing-mode refresh tokens expire after 7 days (a known Google policy, already noted above), and the original code crashed with an unhandled error when this happened, requiring manual deletion of token.json. Added try/except handling around the refresh call so an expired token automatically triggers a fresh login flow instead of crashing — removes the manual cleanup step, though the user must still complete the browser login roughly every 7 days.


## Data layer: two SQLite tables, database file excluded from git
Chose SQLite over CSV for the tracker — needed reliable "find and update an existing record" behavior (e.g., updating an application's status as new emails arrive), which plain CSV handling makes more manual and error-prone. Split into two tables rather than one: `applications` (from classified Gmail emails) and `opportunities` (from JobTech discovery), reflecting the natural discover-then-apply funnel. The database file itself (tracker.db) is excluded from git, same as credentials.json and token.json — it will contain real personal application data, not just secrets, but the privacy reasoning is the same: never belongs in a public repo.