# Adaptation Radar — Sample Digest (hand-run reference)

Hand-compiled by Muse on 2026-10-12 (Mon) from fresh news. Use this to
diff against your radar's first real run: same fields (title, source
material, studio/streamer, status, date) your `radar.py` should emit.

| Title | Source material | Studio / Streamer | Status | Date |
|---|---|---|---|---|
| The Trap | Melanie Raabe, *Die Falle* (2015) | Netflix limited series | Confirmed | Premieres Oct 13, 2026 |
| Whalefall | Daniel Kraus, *Whalefall* | Theaters | Confirmed | In theaters Oct 14, 2026 |
| Sense and Sensibility | Jane Austen, *Sense and Sensibility* | Theaters (US) | Confirmed | Releases Oct 16, 2026 |
| Treasure Island (2026) | Robert Louis Stevenson, *Treasure Island* | MGM+ (US) / Paramount+ (UK) | Released | Premiered Oct 11, 2026 (US); Oct 12, 2026 (UK) |
| Klara and the Sun | Kazuo Ishiguro, *Klara and the Sun* (2021) | Theaters | Confirmed | Releases Oct 22, 2026 |
| The Good Daughter | Karin Slaughter, *The Good Daughter* (2017) | Peacock limited series | Confirmed | Trailer Oct 6, 2026; premieres Nov 12, 2026 |
| The Guest | Emma Cline, *The Guest* | A24 / Square Peg (rights negotiating) | Development / rumor | Sadie Sink in talks per Deadline Oct 9 report — NOT confirmed |
| Myron Bolitar | Harlan Coben, *Myron Bolitar* series (12 books) | Netflix series | In production | Casting announced Oct 7, 2026 (Bebe Neuwirth, Griffin Dunne); no premiere date |
| Verity | Colleen Hoover, *Verity* (2018) | Theaters | Released | Released Oct 2, 2026 — box office hit |
| Carrie | Stephen King, *Carrie* (1974) | Prime Video series | Released | Released Oct 7, 2026 (Mike Flanagan) |

Sources:
- https://varietyindia.com/east-of-eden-sense-and-sensibility-book-adaptation-october-2026/
- https://booksofbrilliance.com/2026/10/11/treasure-island-2026-tv-series-cast-premiere-book-changes/
- https://booksofbrilliance.com/2026/10/09/the-guest-movie-sadie-sink-emma-cline/
- https://www.tvinsider.com/gallery/the-good-daughter-cast-premiere-date-trailer-photos/
- https://www.dixie1057.com/2026/10/07/netflixs-myron-bolitar-adaptation-expands-cast-with-the-addition-of-bebe-neuwirth-griffin-dunne-and-more/
- https://luxurylondon.co.uk/culture/entertainment/tv-film-book-adaptations-autumn-2026/
- https://www.imdb.com/list/ls527509021/
- https://www.hercampus.com/culture/book-to-screen-adaptations-fall-2026/

## Test notes for the radar

1. **Rumor vs confirmed.** *The Guest* is the perfect test item: the story
   itself says the rights deal hasn't closed. Your classification prompt
   should emit status=development/rumor, not confirmed. This is the
   verification pass from your sprint plan in real life.
2. **Dedup.** The Myron Bolitar casting story appears republished on at
   least four different outlets (dixie1057, kjwl, joetown1075, jackfmalexandria)
   — all the same Daypop item. Good stress test for `state.json` dedup.
3. **Niche filter (new idea, not in the scaffold).** Not everything the radar
   catches fits @hannahk_reads's clean/closed-door standard. On-brand here:
   *Treasure Island*, *Sense and Sensibility*, *Klara and the Sun*. NOT
   clean-fiction fits for the account: *Verity*, *Carrie*, *Other Mommy*
   (horror). Consider adding a "clean-fiction relevance" tag in the
   classification prompt so the digest splits into feed-worthy vs portfolio-only.
4. **Content windows this week.** The Trap premieres tomorrow (Oct 13),
   Whalefall Oct 14, Sense & Sensibility Oct 16 — all natural
   read-before-you-watch material for this week's posting windows.
