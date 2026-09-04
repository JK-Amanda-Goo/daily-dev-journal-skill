# Writing a dev-learning post that lands on X

This is the craft reference for Step 5 and Step 6. The goal is one post that a stranger scrolling past would stop for — not because it's loud, but because it hands them something.

## The shape of a good one

Most strong dev-learning posts have three moves, often in 2–3 sentences total:

1. **The claim / the surprise** — what you now know that you didn't this morning. Lead with it. No "Today I learned" preamble; just say the thing.
2. **The specific** — the error message, the number, the tool name, the before/after. This is the part that proves you were actually there. A post without it is indistinguishable from a guess.
3. **The takeaway or the twist** — why it matters, what you'd tell someone else, or the part that's still annoying. Optional but it's what makes the post feel finished rather than dropped.

You do not need a call to action. You do not need a question. The post can just end.

## Length

Aim to land the whole thing in ~280 characters even if the user's account allows more. The discipline of fitting it forces the claim to be sharp. If it genuinely won't fit — there's a sequence the reader needs — go to a short thread (Step 5 rules), but check first that you're not just padding.

## Single post vs. thread

**Single post** is the default. Use it for: one gotcha, one decision, one tool verdict, one "didn't know that."

**Thread (3–4 posts)** only when the learning is inherently sequential — "here's the bug, here's what I thought it was, here's what it actually was, here's the fix" — and each post can stand on its own if it's the only one someone sees. A thread where post 2 is meaningless without post 1 is a blog paragraph cut with newlines.

Never open with "🧵" or "A thread:". Start with the substance of post 1; people can tell it's a thread.

## Anti-patterns, with the fix

**Activity log**
> Today: set up Postgres, wrote the migration, fixed the seed script, added an index. Good day.
The reader gets nothing. Which of those taught you something? Post that.
> The seed script was slow because it was doing 400 individual INSERTs. Batched them into one and it went from 12s to 0.3s. I keep forgetting bulk insert exists.

**Inflated milestone**
> 🚀 Huge progress today!! The auth system is really coming together. Grateful for the grind. #buildinpublic
No detail, borrowed hype. What was hard about auth?
> Spent an hour confused why my JWT middleware wasn't running — turns out route order matters and I'd registered it after the routes it was supposed to protect.

**Vague flex**
> Learned a ton about React rendering today.
Learned what, specifically?
> `useMemo` doesn't help if the parent re-creates the object you're passing in every render. The memo was comparing a fresh reference every time. Obvious in hindsight.

**Engagement bait**
> Is it just me or is CSS grid still confusing after all these years? 😅 Thoughts?
Say your actual thing.
> Finally understood grid `minmax()` — `minmax(0, 1fr)` instead of `1fr` is what stops a grid item from overflowing its track. That one keeps getting me.

## Voice

If `config.md` names a `-voice` skill, draft through it. Otherwise, match how the user writes in the conversation — sentence length, whether they swear, whether they use lowercase, how much they hedge. A dev post should sound like a person talking to peers, not like documentation and not like a press release.

## Community tags (when Step 7 applies)

Only relevant when `config.md` asks for researched tags. The failure mode to avoid is the same one Step 6 already names — `#coding #dev #buildinpublic #100DaysOfCode` reads as reach-seeking because those tags describe the *account*, not this specific post. A tag that's actually good does the opposite: it tells a reader already following that exact niche "this is for you."

**What a good one looks like:** names the specific tool, language, framework, or community the post's learning is about. `#ClaudeCode`, `#SwiftUI`, `#LocalLLM`, `#Rust` — each narrows the audience to people who'd genuinely care. Confirm via `WebSearch` that real, recent posts use it; a tag nobody active uses is dead weight even if it sounds plausible.

**What kills it:** a tag broad enough to fit any dev post (`#tech`, `#software`, `#100DaysOfCode`), a tag that's technically related but not what today's post is actually about (tagging `#AI` on a post about a CSS bug because the project happens to be AI-related), or padding to 3 when only 1 or 2 real ones exist.

**Placement:** together, on their own last line, after the post's substance — not woven into the sentence itself. `Finally understood grid minmax() — minmax(0, 1fr) instead of 1fr is what stops overflow.\n\n#CSS #Frontend` not `Finally understood #CSS grid's #minmax()...`.

## Worked examples

**From a digest bullet:** "spent ages on flaky test — was a shared module-level fixture holding state between tests"
> Lost most of the afternoon to a test that passed alone and failed in the suite. It was a module-level fixture holding state across tests — first test mutated it, second test inherited the mess. Moved it into a per-test setup and it went green. Global state in tests always gets me eventually.
(283 chars — trim "always" or "eventually" to fit.)

**From a digest bullet:** "tried the new X library for Y, went back to doing it by hand"
> Tried $LIBRARY to replace ~30 lines of hand-rolled $THING. It works, but the config to make it do what those 30 lines already did was longer than the 30 lines. Kept the hand-rolled version. Not every dependency is a win.

**From a digest bullet:** "figured out the deploy was failing because of node version mismatch between local and CI"
> Deploy kept failing on a step that worked locally. It was Node 20 locally vs 18 in CI — a syntax feature I used didn't exist in 18. Pinned the version in the CI config and in `.nvmrc` so they can't drift again.
