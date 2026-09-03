---
name: daily-dev-journal
description: Turns a day of work done with Claude Code into a short, honest X/Twitter post about what was actually learned — pulling from a local dev-journal first and falling back to that day's Claude Code session transcripts, building a learning digest you confirm, then drafting the post in your voice with a de-slop pass and a privacy pass before it reaches you. It never posts anything. Use this skill whenever someone wants to write their daily dev post, "build in public" update, "today I learned" tweet, or a short post about what they shipped or figured out in a coding session — whether they say "write my daily dev journal post," "turn today's work into a tweet," "what did I learn today," "draft a build-in-public update," or just "post about this" at the end of a session. Also use it when they want to review or rewrite a dev-post draft they already have, or set up the daily habit. Not for long-form blog posts or newsletters, LinkedIn posts (that audience and format differ), release notes or changelogs, threads teaching a full tutorial, or marketing copy for a product launch.
---

# Daily Dev Journal

Turn a day of building into one short post that's worth someone's attention — because it says something specific and true, not because it performs productivity.

The trap this skill exists to avoid: most daily dev posts are either a bare activity log ("today I set up auth, fixed two bugs, refactored the API") that tells the reader nothing they can use, or a small thing inflated into a fake milestone with LinkedIn energy ("Incredible progress today! 🚀 Grateful for this journey."). What people actually stop for is a concrete learning — a gotcha with the real error, a decision and why the obvious choice was wrong, a tool that did or didn't work and the specific reason. That material is already in the day's work; the skill's job is to find it, let the user confirm what's real and shareable, and shape one honest post out of it.

Two hard rules:
- **This skill never posts.** It hands the user copy-paste-ready text. Posting is always a human action.
- **Nothing from a private or work context goes out without the user saying yes.** See Step 7.

## The workspace

All user data lives outside this skill directory:

```
~/daily-dev-journal/
├── config.md      # handle, voice, audience, redaction list, format prefs
└── posts/         # archive of digests + drafts, one file per day: YYYY-MM-DD.md
```

Create `posts/` on first use. Never commit anything from the workspace into this skill's repo — it can contain private repo names, client names, and unpublished work.

## Step 0 — Config (first run only)

Check for `~/daily-dev-journal/config.md`. If it's missing, copy `assets/config-template.md` there, then fill it in with the user — ask briefly for:

- **Handle / name** — how they sign or who they are, only if it matters for voice.
- **Voice** — if a personal writing-voice skill exists (something like `yourname-voice`), record its name here and use it when drafting. Otherwise the skill takes cues from how the user writes in the conversation.
- **Audience & angle** — who they're posting for (other engineers? founders? people learning to code? build-in-public followers?) and the through-line of what they post about. This is what separates a post that lands from one that's just noise.
- **dev-journal location** — default `~/dev-journal/<project>/`. This is the primary source in Step 2. If they don't keep one, that's fine — the skill falls back to transcripts.
- **Always-share / never-share** — topics or projects that are fair game, and ones that are off-limits (a client engagement, an employer's internal work, a stealth project).
- **Redaction list** — names to strip or mask on the way out: current/past employers, clients, private repo names, internal URLs, teammates' names, unreleased product names.
- **Format prefs** — single post vs. thread by default; max length (280, or longer if they have a subscription that allows it — ask); hashtags yes/no; emoji yes/no; whether they want 1 draft or a few variants.

Tell the user they can edit `config.md` directly anytime. Re-read it at the start of every run.

## Step 1 — Intake

Two things to establish:

1. **Which day?** Default to today. Accept "yesterday," a date, or "the session we just did."
2. **Scope — always ask, never assume:** does the user want the post to be about **one specific project** from that day, or **the whole day across everything they touched**? A day often has one clear story and several forgettable errands; the user knows which. If they made only one thing that day, still confirm rather than skipping the question — sometimes the small side-thing is the better post.

## Step 2 — Gather the raw material (journal first, transcripts to fill gaps)

The point of pulling from two sources is that they fail in opposite ways. A dev-journal entry is already curated and reflective but only exists if the user wrote one, and it may not be framed as a *learning*. Session transcripts always exist and capture everything — including the things the user forgot were interesting — but they're noisy, full of dead ends and tool spam, and carry raw paths and names.

**First, the dev-journal.** Look for entries for that date at the location in `config.md` (default `~/dev-journal/`):

```bash
ls ~/dev-journal/*/$(date +%Y-%m-%d)-*.md 2>/dev/null    # adjust date as needed
```

If entries exist, read them. They're the strongest signal — the user already decided this was worth recording.

**Then, the transcripts — to backfill.** Run the bundled script to get a condensed digest of that day's Claude Code sessions without drowning in JSONL:

```bash
python3 scripts/find_sessions.py --date YYYY-MM-DD [--project SUBSTRING] [--exclude-session THIS_SESSION_ID]
```

It prints, per session: the project directory, git branch, what the user asked for, files created/edited, and the sequence of actions. Use it to (a) catch learnings that never made it into the journal, (b) jog the user's memory, and (c) be the *only* source when there's no journal entry for that day.

`references/mining-sessions.md` covers what counts as a learning and how to read the digest without getting lost in it.

If both sources are thin — a quiet day, mostly reading and small edits — say so. Not every day has a post in it, and a forced one is worse than none.

## Step 3 — Build the learning digest and confirm it

From both sources, write a short digest — plain bullets, no polish:

- **What got done** (2–4 lines, factual)
- **What was learned** (the candidates — gotchas, decisions, tool verdicts, things that surprised the user)
- **What's shareable** (your first pass at which of those is both interesting to an outsider and safe to post)

Show it to the user. This is the editorial checkpoint — they confirm what's accurate, cut what's private, and often add the detail that makes it real ("the actual error was X," "the reason the obvious fix didn't work was Y"). Don't move on until they've reacted to it.

If the user keeps a dev-journal and there's no entry for that day yet, offer to write one from the confirmed digest — it closes the loop and means the raw material exists next time regardless.

## Step 4 — Pick the angle

A good short post makes **one** point. From the confirmed digest, identify the single most postworthy learning (or, for a whole-day post, the through-line that connects what they did). Surface the candidates and let the user choose — it's their call which learning they want their name on.

What makes a learning postworthy:
- It has a **specific, checkable detail** — a real error message, a real number, a named tool, a concrete before/after. Vague posts ("learned a lot about caching today") are skippable.
- An outsider can **take something from it** — a warning, a technique, a "huh, didn't know that."
- It's **honest about difficulty**. "This took me four hours because I misread the docs" is a better post than "shipped caching ✅".

## Step 5 — Draft the post

Draft in the user's voice (use their `-voice` skill if `config.md` names one). Follow `references/x-post-craft.md` for structure and length.

Defaults, unless `config.md` or the user says otherwise:
- **One post**, not a thread. Only go to a thread when the learning genuinely needs steps or a sequence — and then keep it to 3–4 posts, each able to stand alone.
- Open with the **substance**, not a throat-clear. "Here's what I learned today:" and "Quick update:" are wasted lines.
- Fit real content in ~280 characters. If it won't fit, the point isn't sharp enough yet — tighten the claim, don't spill to a thread.
- Produce the number of variants `config.md` asks for (default 2), each taking a different angle or opening — not the same post reworded.

## Step 6 — De-slop pass

Read every draft back and cut the tells. X has its own slop dialect, distinct from LinkedIn's:

- **Engagement bait** — "Am I the only one?", "Thoughts?", "RT if you agree", a question the user doesn't actually want answered.
- **Fake stakes** — "game-changer," "mind blown," "this changes everything" for a normal day's work.
- **LinkedIn bleed** — "Excited to share," "Grateful," "Big learnings," "Let's connect."
- **Listicle throat-clearing** — "Here's what I learned:", "A thread 🧵", "5 things that..." when there aren't five things.
- **Hashtag stuffing** — one is usually plenty; often zero. `#coding #dev #buildinpublic #100DaysOfCode` reads as reach-seeking.
- **Em-dash pile-up and tricolons** — the "not just X, but Y" and "X. Y. Z." rhythms that mark generated text.
- **Vague flexing** — a claim of progress with no detail attached. If you can't name the specific thing, there's no post.

The test: could this post have been written by someone who wasn't actually there that day? If yes, it's missing the detail.

## Step 7 — Privacy pass

Before anything is handed over, check the draft against the `config.md` redaction list and the day's context:

- **Employer / client work** — if the day's work was for a job or a client, flag it. Ask before any of it goes out, even genericized.
- **Private repo names, internal URLs, service names, teammates' names** — mask or cut.
- **Unreleased products or features** — confirm it's OK to reveal that this exists.
- **Security-sensitive detail** — an error message or config snippet that leaks an internal architecture, a path, a key format.

When in doubt, show the user exactly what's identifying and let them decide. Offer a genericized version alongside ("a client project" / "a data pipeline I work on") so they have a safe option ready.

## Step 8 — Deliver and archive

Present the final draft(s) as clean copy-paste blocks — just the post text, nothing to trim. State the character count for each. **Do not post, and don't offer to** — the user copies it out themselves.

Then archive to `~/daily-dev-journal/posts/YYYY-MM-DD.md`:

```markdown
# YYYY-MM-DD

## Digest
<the confirmed digest from Step 3>

## Angle
<the learning this post is built on>

## Posted / drafted
<the variant the user picked, or all variants if they didn't say>

## Other variants
<the rest>
```

Before finalizing, skim the last ~2 weeks of `posts/` — if this learning or framing is a near-repeat of a recent one, tell the user. A build-in-public feed that keeps making the same observation loses people.

## Reference files

- `references/x-post-craft.md` — what makes a dev-learning post land on X, the anti-patterns in detail, single-post vs. thread, and worked before/after examples.
- `references/mining-sessions.md` — how to read the session digest, what counts as a "learning" worth posting, and how to pull signal out of a noisy transcript day.
- `assets/config-template.md` — the config scaffold copied to `~/daily-dev-journal/config.md` on first run.
- `scripts/find_sessions.py` — condenses a day's Claude Code session transcripts into a readable digest. `--help` for options.
