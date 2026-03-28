"""
Newsletter generator for "Must Reads in AI This Week".

This script is invoked by the Claude Code remote agent every Friday at 10am Dublin time.
The agent uses WebSearch and WebFetch to gather stories, then calls send_email() to
deliver the formatted HTML newsletter via Gmail.

Usage (local/manual):
    python3 generate_newsletter.py

Environment variables (for local use):
    SENDGRID_API_KEY  — optional, if sending via SendGrid instead of Gmail MCP
    TO_EMAIL          — recipient address (default: shanemccarthy@live.ie)
"""

import datetime
import os

TO_EMAIL = os.getenv("TO_EMAIL", "shanemccarthy@live.ie")

SOURCES = [
    "https://aidailybrief.beehiiv.com/",
    "Financial Times",
    "Bloomberg",
    "TechCrunch",
    "The Verge",
    "Axios",
    "Wired",
    "The Information",
    "VentureBeat",
    "CNBC",
    "Euronews",
]

STORY_CATEGORIES = [
    "Technical — model releases, feature launches, research breakthroughs",
    "Business — funding, M&A, enterprise strategy, earnings",
    "Political/Regulatory — EU AI Act, Ireland-relevant policy, global AI regulation",
]

PODCAST_SOURCES = ["AI Daily Brief", "Hard Fork", "Lex Fridman"]

STYLE = {
    "font": "Arial, Calibri, sans-serif",
    "heading_color": "#1A1A2E",
    "body_color": "#333333",
    "for_us_color": "#555555",
}


def week_range() -> str:
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)
    return f"{monday.strftime('%-d %B')} – {friday.strftime('%-d %B %Y')}"


def build_html(stories: list[dict], podcast: dict) -> str:
    """
    Build the newsletter HTML from a list of story dicts and a podcast dict.

    story = {
        "headline": str,
        "source": str,
        "source_url": str,
        "summary": str,       # 3-4 sentences
        "for_us": str,        # one-liner on relevance
    }

    podcast = {
        "title": str,
        "url": str,           # Spotify or podcast link
        "summary": str,       # 2-3 sentences
    }
    """
    week = week_range()
    font = STYLE["font"]
    h_color = STYLE["heading_color"]
    body_color = STYLE["body_color"]
    for_us_color = STYLE["for_us_color"]

    stories_html = ""
    for i, s in enumerate(stories, 1):
        stories_html += f"""
        <h2 style="color:{h_color}; font-family:{font}; font-size:14pt; margin-bottom:4px;">
            {i}. {s['headline']}
        </h2>
        <p style="font-family:{font}; font-size:10pt; color:#888; margin-top:0;">
            <a href="{s['source_url']}" style="color:#1A1A2E;">{s['source']}</a>
        </p>
        <p style="font-family:{font}; font-size:11pt; color:{body_color};">{s['summary']}</p>
        <p style="font-family:{font}; font-size:11pt; color:{for_us_color};">
            <b>For us:</b> <i>{s['for_us']}</i>
        </p>
        <hr style="border:none; border-top:1px solid #eee; margin:16px 0;">
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <body style="max-width:680px; margin:auto; padding:24px;">
        <h1 style="color:{h_color}; font-family:{font}; font-size:20pt;">
            Must Reads in AI This Week
        </h1>
        <p style="font-family:{font}; font-size:11pt; color:#888;">Week of {week}</p>
        <p style="font-family:{font}; font-size:11pt; color:{body_color};">
            Your weekly briefing on AI — curated for the AI &amp; Data team.
        </p>
        <hr style="border:none; border-top:2px solid {h_color}; margin:16px 0;">

        {stories_html}

        <h2 style="color:{h_color}; font-family:{font}; font-size:14pt;">
            Podcast of the Week
        </h2>
        <p style="font-family:{font}; font-size:11pt; color:{body_color};">
            <a href="{podcast['url']}" style="color:{h_color};"><b>{podcast['title']}</b></a>
        </p>
        <p style="font-family:{font}; font-size:11pt; color:{body_color};">{podcast['summary']}</p>

        <hr style="border:none; border-top:2px solid {h_color}; margin:24px 0;">
        <p style="font-family:{font}; font-size:11pt; color:#888;">
            That's your week in AI. See you next Friday.
        </p>
    </body>
    </html>
    """


def subject() -> str:
    return f"Must Reads in AI — Week of {week_range()}"
