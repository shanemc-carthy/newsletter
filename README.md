# Must Reads in AI — Weekly Newsletter

A Claude Code remote agent that generates and emails a curated AI news digest every Friday morning to EY's AI & Data team in Ireland.

## What It Does

Every Friday at 8am (Irish time), a scheduled Claude agent:

1. **Reads `story-log.json`** from this repo to know what's already been covered
2. **Checks Gmail** for articles forwarded during the week (subject: `News`) — these get priority placement
3. **Researches this week's AI news** across FT, Bloomberg, TechCrunch, The Verge, Axios, Wired, VentureBeat, CNBC, Euronews, and the AI Daily Brief
4. **Selects 5 stories** with strict constraints: this week only, max 1 competitor story, at least 1 FT story
5. **Picks a podcast** of the week, rotating shows so it never repeats back-to-back
6. **Creates a Gmail draft** addressed to the team — ready to review and send
7. **Commits updated `story-log.json`** back to this repo so stories are never repeated

## Forwarding Stories During the Week

Forward any article to yourself with **subject: `News`** at any point during the week. The agent picks these up on Friday and treats them as priority inclusions — no other action needed.

If you forward more than 5 stories, the agent ranks them by relevance, picks the top 4 (reserving 1 slot for its own best research find), and holds the rest for the following week.

## Story Rules

| Rule | Detail |
|------|--------|
| Recency | This week only (Mon–Fri). Undated or older stories are discarded. |
| De-duplication | `story-log.json` tracks every published story. No repeats ever. |
| Follow-ups | If a story evolves, it can run again with a "Previously covered:" citation. |
| Competitor cap | Max 1 story featuring KPMG, PwC, Deloitte, or Accenture per issue. |
| FT requirement | At least 1 story must be sourced from the Financial Times each week. |
| Held stories | Displaced stories carry over to next week via `held_stories` in the log. |

## Tone & Voice

Written for a mixed-level AI & Data team. Tone is informed and direct — smart colleague, not journalist. Competitor news is reported with scepticism (announcement vs. delivery gap). EY initiatives are framed as leadership moves. "For us:" lines never create anxiety.

## Files

| File | Purpose |
|------|---------|
| `newsletter-droid-prompt.md` | Full agent prompt and workflow documentation |
| `story-log.json` | Running log of all published stories and podcasts (maintained by the agent) |
| `generate_newsletter.py` | HTML builder utilities |

## Requirements

- **Gmail MCP** connected at [claude.ai/settings/connectors](https://claude.ai/settings/connectors)
- **This repo** connected as a source in the scheduled trigger

## Managing the Schedule

View, edit, or disable the trigger: [claude.ai/code/scheduled](https://claude.ai/code/scheduled)

After each Friday run, check:
- Your **Gmail drafts folder** for the newsletter draft
- **`story-log.json`** in this repo — the agent commits an update with message `story log: week of ...`
