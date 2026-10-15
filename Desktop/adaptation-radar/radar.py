#!/usr/bin/env python3
"""
Adaptation Radar — a scheduled agent that monitors entertainment news for
book-to-screen adaptations and emits a structured digest.

Pipeline (the agentic loop, simplified):
    1. PERCEIVE  - pull fresh items from Google News RSS for each query
    2. REMEMBER  - drop anything already seen (state.json = agent memory)
    3. REASON    - LLM classifies each item: is it adaptation news? extract
                   title / source material / studio / status / date
    4. ACT       - write a grouped Markdown digest + update memory

Run:  python radar.py
"""
import time
import hashlib
import json
import os
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote_plus

import feedparser
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "state.json"
DIGEST_DIR = ROOT / "digests"

# Search queries feeding the radar. Tune these to taste.
QUERIES = [
    "book adaptation TV series announced",
    "novel adapted into film casting news",
    "book adaptation trailer release date",
    "bestselling novel television adaptation Netflix Hulu Amazon Apple",
]

MAX_ITEMS_PER_RUN = 12  # cap LLM calls to control cost


def rss_url(query: str) -> str:
    q = quote_plus(query)
    return f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"


def item_id(entry: dict) -> str:
    raw = entry.get("id") or entry.get("link") or entry.get("title", "")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"seen": []}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))


EXTRACTION_SYSTEM = (
    "You are an entertainment news analyst. Given a news headline and snippet, "
    "determine whether it is about a BOOK being adapted for SCREEN (film or TV). "
    "Respond with JSON only, matching this schema exactly:\n"
    '{"is_adaptation_news": bool, "title": str|null, "source_material": str|null, '
    '"studio_streamer": str|null, '
    '"status": "announced"|"casting"|"filming"|"trailer"|"release_date_set"|"released"|"rumor"|null, '
    '"date": str|null, "summary": str|null, "confidence": "high"|"medium"|"low"}\n'
    "title = the adaptation's title. source_material = book title + author. "
    "If it is not adaptation news, set is_adaptation_news=false and everything else null."
)


def classify(client: OpenAI, model: str, entry: dict) -> dict | None:
    """Ask the LLM to extract structured data from one news item."""
    user_msg = (
        f"Headline: {entry.get('title', '')}\n"
        f"Snippet: {entry.get('summary', '')[:500]}\n"
        f"Link: {entry.get('link', '')}"
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": EXTRACTION_SYSTEM},
                {"role": "user", "content": user_msg},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        data = json.loads(resp.choices[0].message.content)
        data["url"] = entry.get("link", "")
        return data
    except Exception as exc:  # noqa: BLE001 - keep the run alive on one bad item
        print(f"  ! classify failed for {entry.get('title', '')[:60]}: {exc}", file=sys.stderr)
        return None


def main() -> None:
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-your-key"):
        sys.exit("Set OPENAI_API_KEY in .env first (see .env.example).")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_BASE_URL") or None
    client = OpenAI(api_key=api_key, base_url=base_url)

    state = load_state()
    seen = set(state["seen"])

    # 1. PERCEIVE — gather fresh items
    fresh: list[dict] = []
    fresh_ids: set[str] = set()
    for query in QUERIES:
        feed = feedparser.parse(rss_url(query))
        if feed.bozo and not feed.entries:
            print(f"  ! WARNING: feed fetch failed for {query!r}: {feed.get('bozo_exception', 'unknown error')}", file=sys.stderr)
            continue
        for e in feed.entries:
            eid = item_id(e)
            if eid not in seen and eid not in fresh_ids:
                fresh_ids.add(eid)
                fresh.append({"id": eid, "title": e.get("title", ""), "link": e.get("link", ""), "summary": e.get("summary", "")})
    print(f"Fetched {len(fresh)} unseen items.")
    fresh = fresh[:MAX_ITEMS_PER_RUN]

    # 2-3. REASON — classify each item
    kept: list[dict] = []
    for entry in fresh:
        print(f"  … {entry['title'][:70]}")
        time.sleep(13)
        data = classify(client, model, entry)
        if data and data.get("is_adaptation_news") and data.get("confidence") in ("high", "medium"):
            kept.append(data)
    print(f"Kept {len(kept)} adaptation items.")

    # 4. ACT — write digest + persist memory
    state["seen"] = sorted(seen)
    save_state(state)

    DIGEST_DIR.mkdir(exist_ok=True)
    today = date.today().isoformat()
    digest_path = DIGEST_DIR / f"{today}.md"

    groups: dict[str, list[dict]] = {}
    for item in kept:
        groups.setdefault(item.get("status") or "announced", []).append(item)

    lines = [f"# 🎬 Adaptation Radar — {today}", "", f"_{len(kept)} new items_", ""]
    if not kept:
        lines.append("Quiet day — no new adaptation news.")
    for status in ("announced", "casting", "filming", "trailer", "release_date_set", "released", "rumor"):
        for item in groups.get(status, []):
            lines.append(f"## {item.get('title') or 'Untitled'}")
            lines.append(f"- **Source material:** {item.get('source_material') or '—'}")
            lines.append(f"- **Studio/streamer:** {item.get('studio_streamer') or '—'}")
            lines.append(f"- **Status:** {status}")
            lines.append(f"- **Date:** {item.get('date') or '—'}")
            lines.append(f"- **Summary:** {item.get('summary') or '—'}")
            lines.append(f"- **Link:** {item.get('url') or '—'}")
            lines.append("")
    digest_path.write_text("\n".join(lines))
    print(f"Digest written to {digest_path}")


if __name__ == "__main__":
    main()
