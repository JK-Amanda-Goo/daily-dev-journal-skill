# Changelog

All notable changes to this skill are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions are tagged in git and published as GitHub Releases.

## [0.1.0] - 2026-09-02

Initial release.

- 8-step workflow: config setup → intake (day + project-vs-whole-day scope, always asked) → gather raw material (dev-journal first, session transcripts as backfill) → confirm a learning digest → pick one angle → draft in the user's voice → X-specific de-slop pass → privacy/redaction pass → deliver as copy-paste text and archive.
- Never posts; publishing is always a human action.
- `references/x-post-craft.md` — post structure, anti-patterns, single-post vs. thread, worked before/after examples.
- `references/mining-sessions.md` — reading the session digest and deciding what's worth posting.
- `assets/config-template.md` — config scaffold (handle, audience, sources, always/never-share, redaction list, format prefs).
- `scripts/find_sessions.py` — condenses a day's Claude Code session transcripts (`~/.claude/projects/*/*.jsonl`) into a per-session Markdown digest: prompts, files touched, condensed action sequence.

[0.1.0]: https://github.com/JK-Amanda-Goo/daily-dev-journal-skill/releases/tag/v0.1.0
