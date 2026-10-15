# 🎬 Adaptation Radar

A scheduled agent that monitors entertainment news for **book-to-screen adaptations** — new announcements, casting news, trailers, release dates — and emits a structured digest.

Built as a portfolio project: a real agentic loop (perceive → remember → reason → act) in ~150 lines of Python.

## How it works

1. **Perceive** — pulls fresh items from Google News RSS across 4 adaptation-focused queries (free, no API key needed).
2. **Remember** — `state.json` tracks every item already seen, so each run only surfaces *new* news (dedupe = agent memory).
3. **Reason** — an LLM classifies each item: is it actually adaptation news? Extracts title, source material, studio/streamer, status (`announced` → `casting` → `filming` → `trailer` → `release_date_set` → `released`), and date. Low-confidence items are dropped.
4. **Act** — writes a grouped Markdown digest to `digests/YYYY-MM-DD.md` and persists memory.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then put your API key in .env
python radar.py
```

Any OpenAI-compatible API works — set `OPENAI_BASE_URL` and `OPENAI_MODEL` in `.env` if you use another provider. Cost is tiny: max 12 short LLM calls per run.

## Scheduling (GitHub Actions, free)

1. Push this repo to GitHub.
2. Add your key as a repo secret: **Settings → Secrets → Actions → `OPENAI_API_KEY`**.
3. Done — `.github/workflows/radar.yml` runs it Mon/Wed/Fri ~7am PT and commits each digest back to the repo. Manual runs work from the Actions tab too.

Prefer local? Add a cron line instead:
```
0 7 * * 1,3,5  cd /path/to/adaptation-radar && .venv/bin/python radar.py
```

## Sample digest

```markdown
# 🎬 Adaptation Radar — 2026-10-12

## Things We Never Got Over (TV)
- **Source material:** Things We Never Got Over by Lucy Score
- **Studio/streamer:** —
- **Status:** announced
- **Date:** —
- **Summary:** TV adaptation news and updates via Deadline
- **Link:** https://...
```

## Ideas to extend (good interview talking points)

- **Rumor vs. confirmed:** add a verification pass that requires 2+ independent sources before `announced`.
- **Watchlist alerts:** let the agent track a personal list and ping you on status changes.
- **Content pipeline:** feed the digest into a second "writer" agent that drafts social posts — a two-agent system.
- **Evaluation:** keep a spreadsheet of 20 outputs scored for accuracy; report your hit rate.

## Files

| File | What |
|---|---|
| `radar.py` | The agent |
| `requirements.txt` | `feedparser`, `openai`, `python-dotenv`, `requests` |
| `.github/workflows/radar.yml` | Free scheduled runs |
| `state.json` | Agent memory — created on first run and committed so scheduled runs share it |
| `digests/` | One Markdown digest per run |
