# Changelog

All notable changes to this skill are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions are tagged in git and published as GitHub Releases.

## [0.1.1] - 2026-09-04

### Added
- Step 7 (optional): researched community hashtags. Off by default (`config.md`'s `Hashtags: research 3 community tags` opts in, or the user can ask for it on a given run); finds up to 3 tags actually live in the post's specific niche via `WebSearch`, never padded with filler, shown with a one-line reason each, placed together on the post's last line. Runs before the privacy pass so a tag's own identifying risk (a small niche community, an employer's product tag) gets checked too.
- `references/x-post-craft.md`: "Community tags" section — what makes a tag specific vs. reach-seeking, and placement.
- `assets/config-template.md`: `Hashtags` option documents the new "research 3 community tags" setting.

## [0.1.0] - 2026-09-02

Initial release.

- 8-step workflow: config setup → intake (day + project-vs-whole-day scope, always asked) → gather raw material (dev-journal first, session transcripts as backfill) → confirm a learning digest → pick one angle → draft in the user's voice → X-specific de-slop pass → privacy/redaction pass → deliver as copy-paste text and archive.
- Never posts; publishing is always a human action.
- `references/x-post-craft.md` — post structure, anti-patterns, single-post vs. thread, worked before/after examples.
- `references/mining-sessions.md` — reading the session digest and deciding what's worth posting.
- `assets/config-template.md` — config scaffold (handle, audience, sources, always/never-share, redaction list, format prefs).
- `scripts/find_sessions.py` — condenses a day's Claude Code session transcripts (`~/.claude/projects/*/*.jsonl`) into a per-session Markdown digest: prompts, files touched, condensed action sequence.

[0.1.0]: https://github.com/JK-Amanda-Goo/daily-dev-journal-skill/releases/tag/v0.1.0
