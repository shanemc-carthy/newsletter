# Must Reads in AI — Weekly Newsletter

A Claude Code remote agent that generates and emails a curated AI news digest every Friday morning.

## What it does

Every Friday at 10am Dublin time, a remote Claude agent:

1. Scrapes the [AI Daily Brief](https://aidailybrief.beehiiv.com/) for the week's episodes
2. Web searches across FT, Bloomberg, TechCrunch, The Verge, Axios, Wired, VentureBeat, CNBC, and Euronews
3. Selects 5 stories across technical, business, and regulatory categories (EU/Ireland angle prioritised)
4. Picks a podcast recommendation from AI Daily Brief, Hard Fork, or Lex Fridman
5. Sends a formatted HTML email to shanemccarthy@live.ie via Gmail

## Files

| File | Purpose |
|------|---------|
| `generate_newsletter.py` | HTML builder and shared constants used by the agent |
| `newsletter-droid-prompt.md` | Original prompt spec and Mac Mini scheduling guide |

## Scheduled trigger

- **Platform:** Claude Code remote agents
- **Schedule:** `0 9 * * 5` (Fridays 9am UTC / 10am Dublin BST)
- **Manage:** https://claude.ai/code/scheduled

## Requirements

- Gmail connected as an MCP connector at https://claude.ai/settings/connectors

## Running manually

Paste the prompt from `newsletter-droid-prompt.md` into a Claude Code session with `WebSearch`, `WebFetch`, and Gmail MCP enabled.
