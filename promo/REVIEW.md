# Khalas promo, vertical: review notes

1080×1920 · 30 fps · 45 s · silent · rendered to `../renders/khalas-promo-vertical.mp4`

## Build

The film is built from the brief's storyboard as written, so no alternative storylines were made. Each scene is its own file in `compositions/`:

| Time | File | Ground |
| --- | --- | --- |
| 0–4 s | hook.html | ink + blue glow |
| 4–10 s | problem.html | ink + blue glow (red accents) |
| 10–13 s | turn.html | cobalt (white flash in) |
| 13–20 s | chat2order.html | paper |
| 20–27 s | nightbot.html | ink (night) |
| 27–34 s | board.html | paper |
| 34–38 s | solution.html | cobalt |
| 38–45 s | cta.html | cobalt |

## Creative calls

- **Logo.** There's no `logo.png`, so the mark is a white SVG chat bubble with a yellow tick that draws itself.
- **Wordmark.** "khalas" is cut out of the supplied brand image as a transparent PNG (`assets/brand/khalas-wordmark-white.png`).
- **Scene wipes.** Each wipe is a full-frame panel in the next scene's ground colour, moving right to left to match Arabic reading order:
  - The hook→problem wipe is red.
  - Problem→turn is a white flash.
- **Fonts.** Bricolage Grotesque, IBM Plex Sans Arabic and Instrument Serif Italic are bundled locally from @fontsource. GSAP is also bundled locally, so a render needs no network.
- **Example data.** Every name, order number, phone number (`٠١٠٠٠٠٠…`) and price is made up.
- **Layout.** All copy stays inside the TikTok/Reels/Shorts safe area (y 288–1248, x 120–780 lower down). That leaves the lower third of every frame empty on purpose.

## Checked

- `hyperframes check`: 0 errors.
- Contact sheets at 13 moments. Fixed after looking:
  - "99+" was rendering as "+99" (bidi).
  - English lines with periods were flipping in the right-to-left layout.
  - Headings overlapped the YouTube Shorts top bar.

## Warnings kept on purpose

- `film_silent`: there's no music source here (no HeyGen sign-in, no music provided). Add an `<audio id="music">` to `index.html` to give it a bed.
- `line_unread` on the 99+ badge and the ٤٠٠ counter steps: those are counters, and only the final number has to be read.
- `container_overflow` / `escaped_container`: the bubble flood and ring bursts spill past their boxes by design.

## Weakest shot and next steps

- The order board (27–34 s) has tall, mostly empty columns once the cards spread out. Shortening them and enlarging the cards would read better.
- With more time: a music bed with pops on the bubbles and the Done pill, plus a riser into the logo at 10 s.
