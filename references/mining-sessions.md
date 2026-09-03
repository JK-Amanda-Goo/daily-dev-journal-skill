# Mining a day's work for something worth posting

Reference for Step 2 and Step 3 — how to turn "what happened today" into "what's worth a post," especially on days with no dev-journal entry and only transcripts to go on.

## Reading the session digest

`scripts/find_sessions.py` gives you, per session:

- **project / cwd / branch** — which piece of work this was
- **what the user asked** — their prompts, in order; this is the intent
- **files created / edited** — the concrete output
- **actions** — the sequence of tool calls, condensed (commands run, files read, searches)

Read the *user prompts* first. They tell you what the day was trying to do. Then look at where the sequence got long or circled back — repeated edits to the same file, the same command run five times with tweaks, a long run of Reads before a fix. That's usually where the learning is: friction leaves a trace.

Ignore the smooth parts. A task that went straight from ask to done in three steps taught nobody anything.

## What counts as a learning worth posting

In rough order of how well they do as posts:

1. **A gotcha with a cause** — something broke, you found out why, the why is non-obvious. Best material. The post writes itself once you have the real error and the real cause.
2. **A decision where the obvious choice was wrong** — you were going to use X, you used Y instead, here's what tipped it. Useful to anyone facing the same fork.
3. **A tool verdict** — you tried a library / CLI / service and formed an opinion with a reason. "Worked, here's the catch" or "didn't work, here's why" both post well.
4. **A "didn't know that"** — a language feature, an API behavior, a flag that does exactly the thing you'd been working around. Small but real.
5. **A number** — a speedup, a size reduction, a count. Concrete and shareable even when the rest of the story is dull.
6. **A shipped thing** — least interesting on its own ("shipped X"), but fine if paired with one of the above ("shipped X; the hard part was...").

## What doesn't make a post

- Routine CRUD, boilerplate, config that just worked.
- Anything where the honest summary is "I did the thing and it was fine."
- Something the user can't describe without naming a private repo, a client, or an employer's internal system (see Step 7 — genericize it or drop it).
- A learning that's really just "I was tired and made a typo."

## Turning transcript friction into a digest bullet

When the digest shows a struggle, reconstruct it as: **symptom → what you thought → what it was → what fixed it.** You often can't get all four from the transcript alone — that's what Step 3's confirmation is for. Write the bullet with the gaps marked:

> Flaky test in the `orders` suite — passed alone, failed in CI. Transcript shows ~40 min of it. [Cause? Fix? — ask user]

Then the user fills in "shared fixture holding state" and "moved to per-test setup," and you have a post.

## When the day is genuinely quiet

If the digest is mostly Reads, small edits, and things that worked: say so plainly. Offer the user the option to skip the day, or to post something smaller and honest ("quiet day — mostly reading through the $X codebase to understand how $Y works before touching it") rather than manufacturing a lesson. A skipped day is not a failure of the habit.
