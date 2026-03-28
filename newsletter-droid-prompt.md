# Newsletter — Claude Code on Mac Mini

Use this prompt with Claude Code on your always-on Mac Mini to generate the weekly newsletter every Friday morning.

---

## 1. Claude Code Prompt (copy-paste into a session)

```
Generate my weekly "Must Reads in AI This Week" newsletter as a Word doc (.docx) saved to ~/newsletter/.

WHAT TO DO:
1. Fetch the AI Daily Brief archive at https://aidailybrief.beehiiv.com/ and scrape each article from THIS WEEK (Monday-Friday).
2. Web search for additional AI news this week from sources including: Financial Times, Bloomberg, TechCrunch, The Verge, Axios, Wired, The Information, VentureBeat, CNBC, and Euronews.
3. Select 5 stories that cover a MIX of:
   - Technical (model releases, feature launches, research breakthroughs)
   - Business (funding, M&A, enterprise strategy, earnings)
   - Political/Regulatory (EU AI Act enforcement, Ireland-relevant policy, global AI regulation)
4. Find 1 podcast recommendation from this week (AI Daily Brief, Hard Fork, Lex Fridman, or similar).
5. First install python-docx if needed (pip3 install python-docx), then generate and run a Python script to produce the Word doc.

NEWSLETTER FORMAT:
- Title: "Must Reads in AI This Week"
- Subtitle: "Week of [date range]"
- One-line intro sentence
- 5 numbered stories, each with:
  - Headline (as heading)
  - Source links (clickable hyperlinks)
  - 3-4 sentence summary (concise, no waffle)
  - "For us:" one-liner on why it matters
- Divider
- "Podcast of the Week" section with title, Spotify link, and 2-3 sentence summary
- FT paywall note if applicable
- Sign-off: "That's your week in AI. See you next Friday."

AUDIENCE:
- An AI & Data team based in Ireland with mixed technical skills
- Political stories should prioritise EU/Ireland relevance over US domestic politics
- Tone: informed, direct, no hype. Write like a smart colleague, not a journalist.

STYLING:
- Font: Calibri 11pt
- Headings: dark navy (#1A1A2E)
- "For us:" lines: bold label, italic text
- Clickable hyperlinks on all source references

FILENAME: "Must Reads in AI - YYYY-MM-DD.docx" (use today's date)

Clean up the Python script after generating the doc.
```

---

## 2. Schedule it on your Mac Mini (every Friday 8am)

### Option A: cron + Claude Code CLI (simplest)

```bash
# Create the output directory
mkdir -p ~/newsletter

# Save the prompt to a file
cat > ~/newsletter/prompt.txt << 'EOF'
Generate my weekly "Must Reads in AI This Week" newsletter as a Word doc (.docx) saved to ~/newsletter/.

... (paste the full prompt from section 1 above)
EOF

# Edit crontab
crontab -e

# Add this line (Friday 8:00 AM):
0 8 * * 5 cd ~/newsletter && claude -p "$(cat ~/newsletter/prompt.txt)" --allowedTools "Bash,WebSearch,FetchUrl,Read,Write" 2>&1 >> ~/newsletter/run.log
```

> `claude -p` runs Claude Code in non-interactive (headless/print) mode — it takes the prompt, executes, and exits. No terminal session needed.

### Option B: launchd (macOS native, survives reboots)

Save this as `~/Library/LaunchAgents/com.newsletter.weekly.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.newsletter.weekly</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd ~/newsletter &amp;&amp; claude -p "$(cat ~/newsletter/prompt.txt)" --allowedTools "Bash,WebSearch,FetchUrl,Read,Write" 2>&amp;1 >> ~/newsletter/run.log</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>5</integer>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/newsletter-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/newsletter-stderr.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

Then load it:

```bash
launchctl load ~/Library/LaunchAgents/com.newsletter.weekly.plist
```

> launchd is preferred over cron on macOS — it runs even if the Mac was asleep at the scheduled time (it catches up).

### Option C: Claude Code scheduled tasks (if available)

Claude Code has a built-in scheduled tasks feature. From a Claude Code session on your Mac Mini:

```
/schedule create --cron "0 8 * * 5" --prompt "$(cat ~/newsletter/prompt.txt)"
```

This runs in Claude Code's cloud infrastructure so the Mac Mini doesn't even need to be awake.

---

## 3. Getting the doc to your laptop

After generation, the .docx will be at `~/newsletter/Must Reads in AI - YYYY-MM-DD.docx` on the Mac Mini. Options to get it:

- **iCloud Drive**: Change the output path to `~/Library/Mobile Documents/com~apple~CloudDocs/newsletter/` and it syncs automatically.
- **Shared folder**: Enable File Sharing in System Settings on the Mac Mini, access from your Windows laptop via `\\macmini.local\`.
- **Email to yourself**: Add a line to the prompt: "After generating the doc, email it to shanemccarthy@live.ie using the `mail` command."

---

## 4. Checking logs

```bash
# See the last run output
tail -50 ~/newsletter/run.log

# List generated newsletters
ls -la ~/newsletter/*.docx
```
