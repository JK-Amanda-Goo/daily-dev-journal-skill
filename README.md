# Daily Dev Journal (Claude Code skill)

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skill that turns a day of work into one short, honest X/Twitter post about what you actually learned.

It reads your day two ways — a local dev-journal if you keep one, and that day's Claude Code session transcripts as a fallback — builds a plain "what I did / what I learned" digest for you to confirm, then drafts the post in your voice with a de-slop pass and a privacy pass.

**It never posts anything.** You get copy-paste-ready text; publishing is always your move.

## Why two sources

A hand-written dev-journal entry is already thoughtful, but only exists if you wrote one. Session transcripts always exist and capture the things you forgot were interesting, but they're noisy and full of raw paths and names. The skill leans on the journal first and uses the transcripts to fill gaps — or as the only source on days you didn't journal.

## Install

Clone it into your Claude Code skills directory (or symlink it there):

```bash
git clone https://github.com/JK-Amanda-Goo/daily-dev-journal-skill ~/Projects/daily-dev-journal-skill
ln -s ~/Projects/daily-dev-journal-skill ~/.claude/skills/daily-dev-journal
```

On first run the skill creates `~/daily-dev-journal/config.md` from a template and walks you through filling it in — handle, audience, which projects are fair game, a redaction list, and format preferences.

## Use it

At the end of a coding day:

> "write my daily dev post" · "turn today's work into a tweet" · "what did I learn today" · "draft a build-in-public update"

It asks which day, and whether the post should be about one project or the whole day — then works through the digest with you before drafting.

## Requirements

- Claude Code (or another agent that supports skills), with Python 3 for the session-digest script
- Nothing else — no API keys, no X credentials, no external services

## Voice

If you have a personal writing-voice skill (something like `yourname-voice`), name it in `config.md` and this skill drafts through it. Without one, it matches how you write in the conversation.

## What this intentionally doesn't do

- **Post.** It drafts; you publish.
- **Invent a lesson.** A quiet day gets told to you as a quiet day — a forced post is worse than a skipped one.
- **Leak your work.** Employer, client, and private-repo material is flagged and held back until you say otherwise.
- **Replace long-form.** This is for one short post, not a blog entry, newsletter, or tutorial thread. Not for LinkedIn either — different audience, different format.

## Files

- `SKILL.md` — the workflow
- `references/x-post-craft.md` — what makes a dev-learning post land, the anti-patterns, single-post vs. thread, worked examples
- `references/mining-sessions.md` — reading the session digest and deciding what's worth posting
- `assets/config-template.md` — the config scaffold
- `scripts/find_sessions.py` — condenses a day's Claude Code transcripts into a readable digest

## Releasing

Every notable change gets a `CHANGELOG.md` entry (Keep a Changelog format), a matching git tag, and a GitHub Release whose notes are that changelog section:

```bash
# 1. Add a new version section to the top of CHANGELOG.md
# 2. git add -A && git commit -m "..."
git tag -a vX.Y.Z -m "vX.Y.Z - <one-line summary>"
git push origin main --tags
gh release create vX.Y.Z --title "vX.Y.Z" --notes "<paste the CHANGELOG section>"
```

## License

MIT — see `LICENSE`.
